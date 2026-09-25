#!/usr/bin/env bash
# Offline self-test: scores a fixture dataset with a fixture reference set. No Apify token needed.
cd "$(dirname "$0")/.." || exit 1
rm -rf tests/state tests/reports && mkdir -p tests/state && cp tests/reference_hashes.json tests/state/
python monitor.py --from-json tests/fixture_dataset.json --state-dir tests/state --report-dir tests/reports --no-slack
