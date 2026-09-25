# Copycat findings, first manual review (2026-09-22)

Source: 829 Meta Ads Library ads pulled on 2026-09-22 (brand, copy and category searches, 90-day window). 478 were Bambora's own or creator ads (they link to bamboraco.com). The other 351 were reviewed by eye as contact sheets, and every sling-looking ad was fingerprint-checked against Bambora's 310 ad creatives and 23 product photos.

## 1. Confirmed theft: explicitn.com (DMCA-ready)

- Ad: https://www.facebook.com/ads/library/?id=2128834464362109 (page "Explicitn-ea", started 2026-08-07, active on Facebook, Instagram, Messenger, Audience Network, Threads)
- The ad is Bambora's own 56-second UGC video (woman in glasses, brown sling, backyard). Frame-identical to Bambora ad https://www.facebook.com/ads/library/?id=1835818061100628 (Bambora page, started 2026-08-24). Side by side: `2026-09-22-evidence/explicitn_ad_vs_bambora_ad.jpg`
- Store: https://www.explicitn.com/products/toddler-sling-carrier is a clone of the Bambora product page: same 13 colour options in the same order (Black, Checkered, Houndstooth - Limited Edition, Light Palms, Blue Sailboat, Black Sailboat, Floral, Cotton Candy, Leopard, Carnival, Blue, Brown, Green), and 21 of its 25 images are Bambora's product photos, including the "Don't fall for Amazon knock offs" graphic, the testimonial collages and the "Loved by 150,000+ parents" image. Side by side: `2026-09-22-evidence/explicitn_store_vs_bambora.jpg`
- Price shown: about £29.99, listed as "Save 48%". Copy: "No more sore arms or bulky carriers... This sling is a total lifesaver for busy parents!"
- Hosting: site and image CDN (cdn.cloudfastin.top) both sit behind Cloudflare (IP 104.18.3.157). Not a Shopify store. Claims PayPal and card checkout.
- Ownership proof: Bambora ran the same video earlier, in ad https://www.facebook.com/ads/library/?id=1343534694113082 (Bambora page, started 2026-07-31), a week before the Explicitn ad. Cite that ad ID as the original.

Where to file:
1. Meta: report the ad and the page through the Intellectual Property Report form (Help Centre, "Report copyright infringement"), citing ad ID 2128834464362109 and the original ad IDs 1343534694113082 (31 Jul) and 1835818061100628 (24 Aug).
2. Cloudflare: abuse.cloudflare.com, DMCA category, listing the product URL and the 21 image URLs (in `explicitn_match.json` and the side-by-side). Cloudflare forwards to the origin host.
3. PayPal: report the merchant for selling with stolen brand assets, which can cut off their checkout.

## 2. Same design, own or AI images (lookalikes, not a copyright case)

These sell a crescent hip sling like Bambora's but used their own or AI-generated pictures. Nothing to DMCA. Worth watching because their ad copy and store templates are near-identical to each other, which is typical of one dropship operator running many storefronts.

- Zenovap Baby Co. / Movexas SnugNest (shopzenovap.com, windlore.com, shopwindlore.com): one kitchen video reused across three store names. Product images on shopzenovap.com are ChatGPT-generated (the file names say so). Ads: 879349015237004, 1643626853409013, 1724320778569294.
- "Lightweight Baby Carrier Sling" mesh cluster (eigoods.com funnels, luckinwish.co.uk, outrerbuy.shop, pagemindvibe.com, fluxraa.com, munichsunny.com, skiip.in, G-Shopping.lk): the generic mesh one-shoulder sling. Ads: 932209959363562, 1589802162766456, 1994469337717765, 1112739058076870, 2509368192878071, 1395664061969443, 3101237180062326, 1091294146620398, 1855634978452929.

## 3. Real competitors with a similar design (no action)

Mabē Carriers (Monarch Toddler Sling), Qookie Go, Lune & Littles, Senarah, Wildride. Own branding and photography.

## 4. Not copycats, flagged only by a word

Green Brands Chile (bambora.cl, bamboo towels). Now on the ignore list.

## What the tool does with this

Exact creative theft (case 1) is what the automatic visual fingerprint catches: it flagged Explicitn at distance 0 without any keyword. Lookalikes (case 2) need a human eye, which is the planned weekly picture digest.
