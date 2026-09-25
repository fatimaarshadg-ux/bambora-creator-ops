#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { execSync, execFileSync } from "node:child_process";
import { mkdirSync, writeFileSync, readFileSync, readdirSync, existsSync } from "node:fs";
import { join, dirname, basename } from "node:path";
import os from "node:os";

const BASE_URL = "https://api.jointrybe.com/v1";
const WORKDIR = join(os.homedir(), "Bombara", "trybe-review", "tmp");
const WHISPER_MODEL = join(os.homedir(), "whisper-models", "ggml-base.en.bin");
mkdirSync(WORKDIR, { recursive: true });

// Windows handover: the key comes from TRYBE_API_KEY, else Windows DPAPI
// (%USERPROFILE%\.claude\secrets\trybe_api_key.dpapi, written by install.ps1), else the macOS Keychain.
let CACHED_KEY = "";
function getApiKey() {
  if (CACHED_KEY) return CACHED_KEY;
  if (process.env.TRYBE_API_KEY) return (CACHED_KEY = process.env.TRYBE_API_KEY.trim());
  if (process.platform === "win32") {
    const file = join(os.homedir(), ".claude", "secrets", "trybe_api_key.dpapi");
    const ps =
      `$s = Get-Content -LiteralPath '${file}' | ConvertTo-SecureString; ` +
      "$b = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($s); " +
      "[System.Runtime.InteropServices.Marshal]::PtrToStringAuto($b)";
    CACHED_KEY = execFileSync("powershell", ["-NoProfile", "-Command", ps]).toString().trim();
    return CACHED_KEY;
  }
  const user = process.env.USER || execSync("whoami").toString().trim();
  CACHED_KEY = execSync(`security find-generic-password -a "${user}" -s "trybe-api-key" -w`).toString().trim();
  return CACHED_KEY;
}
const FFMPEG = process.platform === "win32" ? "ffmpeg" : (existsSync("/opt/homebrew/bin/ffmpeg") ? "/opt/homebrew/bin/ffmpeg" : "ffmpeg");
// Speech to text: whisper.cpp on Fatima's Mac; elsewhere the media-watcher's private Python (faster-whisper).
const MW_PY = join(os.homedir(), "claude-media-watcher", ".venv", process.platform === "win32" ? "Scripts\\python.exe" : "bin/python");
function transcribeWav(audioPath, txtBase) {
  if (process.platform !== "win32" && existsSync("/opt/homebrew/bin/whisper-cli") && existsSync(WHISPER_MODEL)) {
    execSync(`/opt/homebrew/bin/whisper-cli -m "${WHISPER_MODEL}" -f "${audioPath}" -otxt -of "${txtBase}" --no-timestamps`);
    return readFileSync(`${txtBase}.txt`, "utf-8").trim();
  }
  const code = "import sys\nfrom faster_whisper import WhisperModel\nm = WhisperModel('small', device='cpu', compute_type='int8')\nsegs, _ = m.transcribe(sys.argv[1])\nprint(' '.join(s.text.strip() for s in segs))";
  const text = execFileSync(MW_PY, ["-c", code, audioPath], { encoding: "utf-8", maxBuffer: 1 << 26 }).trim();
  writeFileSync(`${txtBase}.txt`, text);
  return text;
}

async function trybeFetch(path, opts = {}, attempt = 0) {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...opts,
    headers: {
      Authorization: `Bearer ${getApiKey()}`,
      "Content-Type": "application/json",
      ...(opts.headers || {}),
    },
  });

  if (res.status === 429 && attempt < 5) {
    const wait = Number(res.headers.get("retry-after") ?? 1);
    await new Promise((r) => setTimeout(r, wait * 1000));
    return trybeFetch(path, opts, attempt + 1);
  }

  const text = await res.text();
  let body;
  try {
    body = JSON.parse(text);
  } catch {
    body = text;
  }
  if (!res.ok) {
    throw new Error(`Trybe API ${res.status}: ${JSON.stringify(body)}`);
  }
  return body;
}

const server = new McpServer({ name: "trybe", version: "1.0.0" });

server.registerTool(
  "trybe_list_submissions",
  {
    title: "List Trybe submissions",
    description:
      "List your brand's submissions, newest first, cursor-paginated. `query` is the powerful one: " +
      "it substring-matches the transcript, THE ON-SCREEN TEXT, and the creator's note - so it finds " +
      "burned-in captions that never appear in the transcript (e.g. query:'sale' surfaces sale-led ads). " +
      "Case-insensitive, one phrase of 2-100 chars, not semantic. Page with `after` = the previous " +
      "response's next_cursor.",
    inputSchema: {
      status: z
        .enum(["pending", "approved", "rejected", "revision_requested"])
        .optional(),
      creator_id: z.string().optional().describe("creator_<uuid>"),
      group_id: z.string().optional().describe("subgroup_<uuid>"),
      program_id: z.string().optional().describe("creator_program_<uuid>"),
      product_id: z.string().optional().describe("product_<uuid>"),
      angle: z.string().optional().describe("angle name, case-insensitive"),
      transcript_language: z.string().optional().describe("ISO 639-1, e.g. en"),
      query: z
        .string()
        .min(2)
        .max(100)
        .optional()
        .describe("matches transcript + on-screen text + creator note"),
      limit: z.number().int().min(1).max(100).default(20),
      after: z.string().optional().describe("next_cursor from a previous page"),
      before: z.string().optional().describe("mutually exclusive with after"),
    },
  },
  async (args) => {
    if (args.after && args.before)
      throw new Error("Pass only one of `after` / `before`");
    const params = new URLSearchParams();
    for (const k of [
      "status", "creator_id", "group_id", "program_id", "product_id",
      "angle", "transcript_language", "query", "after", "before",
    ]) {
      if (args[k]) params.set(k, args[k]);
    }
    params.set("limit", String(args.limit ?? 20));
    const data = await trybeFetch(`/submissions?${params.toString()}`);
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
);

server.registerTool(
  "trybe_creator_performance",
  {
    title: "Bulk creator performance",
    description:
      "One row per active creator: earnings, Trybe conversions + GMV, submission and ad counts, " +
      "ad spend, provider-reported purchases and ROAS, over a UTC date range. This is the endpoint " +
      "behind the analytics page's creator leaderboard - use it instead of scraping the UI. " +
      "Set sort_by to a metric to rank the whole roster by it. Defaults to the last 30 complete days, " +
      "so pass start_date explicitly for lifetime figures. Max range 365 days (90 when sort_by is a " +
      "metric or active_only is set).",
    inputSchema: {
      start_date: z
        .string()
        .regex(/^\d{4}-\d{2}-\d{2}$/)
        .optional()
        .describe("YYYY-MM-DD, inclusive. Default: 30 complete days ago"),
      end_date: z
        .string()
        .regex(/^\d{4}-\d{2}-\d{2}$/)
        .optional()
        .describe("YYYY-MM-DD, inclusive. Default: yesterday UTC. No future dates"),
      creator_id: z.string().optional(),
      program_id: z.string().optional(),
      managed_by: z.enum(["partner", "brand"]).optional(),
      sort_by: z
        .enum([
          "joined_at", "earnings", "trybe_gmv", "trybe_conversions",
          "new_submissions", "active_submissions", "ads", "spend",
          "purchase_value", "purchases",
        ])
        .optional()
        .describe("joined_at = roster newest-first; any metric = ranked highest first"),
      active_only: z.boolean().optional().describe("drop creators with an all-zero window"),
      limit: z.number().int().min(1).max(100).default(20),
      after: z.string().optional(),
      before: z.string().optional(),
    },
  },
  async (args) => {
    if (args.after && args.before)
      throw new Error("Pass only one of `after` / `before`");
    const params = new URLSearchParams();
    for (const k of [
      "start_date", "end_date", "creator_id", "program_id",
      "managed_by", "sort_by", "after", "before",
    ]) {
      if (args[k]) params.set(k, args[k]);
    }
    if (args.active_only) params.set("active_only", "true");
    params.set("limit", String(args.limit ?? 20));
    const data = await trybeFetch(`/creator-performance?${params.toString()}`);
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
);

server.registerTool(
  "trybe_get_submission",
  {
    title: "Get a Trybe submission",
    description:
      "Get full detail for one submission by id, including transcript, creator comment, products, and a short-lived signed asset download URL.",
    inputSchema: { submission_id: z.string() },
  },
  async ({ submission_id }) => {
    const data = await trybeFetch(`/submissions/${submission_id}`);
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
);

server.registerTool(
  "trybe_download_asset",
  {
    title: "Download a submission's video/image asset",
    description:
      "Fetches a submission, follows its signed asset URL, and downloads the raw file into the local working directory. Returns the local file path.",
    inputSchema: { submission_id: z.string() },
  },
  async ({ submission_id }) => {
    const sub = await trybeFetch(`/submissions/${submission_id}`);
    const url = sub.asset?.url;
    if (!url) throw new Error("Submission has no asset.url");
    const ext = sub.media_type === "video" ? "mov" : "jpg";
    const filePath = join(WORKDIR, `${submission_id}.${ext}`);
    const res = await fetch(url);
    const buf = Buffer.from(await res.arrayBuffer());
    writeFileSync(filePath, buf);
    return {
      content: [
        {
          type: "text",
          text: `Downloaded ${buf.length} bytes to ${filePath}`,
        },
      ],
    };
  }
);

server.registerTool(
  "trybe_extract_frames",
  {
    title: "Extract still frames from a downloaded video",
    description:
      "Runs ffmpeg on a local video file (from trybe_download_asset) and extracts still frames at a given interval. Returns the list of frame file paths.",
    inputSchema: {
      video_path: z.string(),
      interval_seconds: z.number().default(3),
    },
  },
  async ({ video_path, interval_seconds }) => {
    const base = video_path.replace(/\.[^/.]+$/, "");
    const pattern = `${base}_frame_%03d.jpg`;
    execFileSync(FFMPEG, ["-y", "-i", video_path, "-vf", `fps=1/${interval_seconds}`, pattern, "-loglevel", "error"]);
    const dir = dirname(base);
    const prefix = basename(base);
    const files = readdirSync(dir)
      .filter((f) => f.startsWith(`${prefix}_frame_`))
      .sort()
      .map((f) => join(dir, f));
    return { content: [{ type: "text", text: JSON.stringify(files, null, 2) }] };
  }
);

server.registerTool(
  "trybe_transcribe",
  {
    title: "Transcribe a submission's audio",
    description:
      "Extracts the audio track from a local video file and transcribes it with whisper.cpp. Returns the transcript text.",
    inputSchema: { video_path: z.string() },
  },
  async ({ video_path }) => {
    const base = video_path.replace(/\.[^/.]+$/, "");
    const audioPath = `${base}_audio.wav`;
    const txtBase = `${base}_transcript`;
    execFileSync(FFMPEG, ["-y", "-i", video_path, "-ar", "16000", "-ac", "1", "-vn", audioPath, "-loglevel", "error"]);
    const text = transcribeWav(audioPath, txtBase);
    return { content: [{ type: "text", text }] };
  }
);

// --- Consequential actions: real side effects (creator payout / notification). ---
// These are exposed so they CAN be invoked, but the calling agent must only ever
// call them after explicit, per-instance confirmation from the account owner in
// chat — never automatically or in a batch. This mirrors Trybe's own API note
// that these only work while a submission is "pending".

server.registerTool(
  "trybe_approve_submission",
  {
    title: "Approve a submission (triggers creator payout)",
    description:
      "Approves a pending submission. This has a REAL side effect: it triggers the creator's payout and notifies them. Only call this after the human user has explicitly confirmed, in this exact instance, that they want to approve this specific submission.",
    inputSchema: { submission_id: z.string(), note: z.string().optional() },
  },
  async ({ submission_id, note }) => {
    const data = await trybeFetch(`/submissions/${submission_id}/approve`, {
      method: "POST",
      body: JSON.stringify(note ? { note } : {}),
    });
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
);

server.registerTool(
  "trybe_reject_submission",
  {
    title: "Reject a submission",
    description:
      "Rejects a pending submission and notifies the creator. Only call this after the human user has explicitly confirmed, in this exact instance, that they want to reject this specific submission.",
    inputSchema: { submission_id: z.string(), reason: z.string() },
  },
  async ({ submission_id, reason }) => {
    const data = await trybeFetch(`/submissions/${submission_id}/reject`, {
      method: "POST",
      body: JSON.stringify({ reason }),
    });
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
);

server.registerTool(
  "trybe_request_revision",
  {
    title: "Request a revision on a submission",
    description:
      "Requests a revision on a pending submission and notifies the creator with instructions. Only call this after the human user has explicitly confirmed, in this exact instance, that they want to request revision on this specific submission.",
    inputSchema: { submission_id: z.string(), instructions: z.string() },
  },
  async ({ submission_id, instructions }) => {
    const data = await trybeFetch(`/submissions/${submission_id}/request-revision`, {
      method: "POST",
      body: JSON.stringify({ comment: instructions }),
    });
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
