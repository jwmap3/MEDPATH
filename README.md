# MEDPATH

A personal field reference: Chief Complaint → Demographic → Vitals/Weight → matched standing order with auto-calculated dosing. Built from the Toledo Fire & Rescue Bureau of EMS Patient Care Protocols (Responsoft, reviewed 04/22/2026).

Static site, no backend, installable as an offline-capable PWA. Currently covers an 18-protocol / 33-drug MVP subset — see **Status** below.

**This is a personal reference aid, not a substitute for the official protocol book, training, or medical direction. Always verify against the current department protocols.**

## Run it locally

No build step. From this folder:

```
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Deploy

### 1. Push to GitHub

```
cd medpath
git init
git add .
git commit -m "MEDPATH v1 - MVP protocol set"
git branch -M main
git remote add origin https://github.com/<your-username>/medpath.git
git push -u origin main
```

(Create the empty repo on github.com first — no README/license, since this folder already has one.)

### 2. Deploy on Vercel

1. Go to vercel.com, sign in with your GitHub account.
2. "Add New… → Project", select the `medpath` repo.
3. Framework preset: **Other** (it's a static site — no build command, no output directory override needed).
4. Deploy. Vercel will auto-redeploy on every push to `main`.

Once live, open the Vercel URL on your phone and use the browser's "Add to Home Screen" (iOS Safari) or the install prompt (Android Chrome) to install it as an app — it'll work fully offline after the first load.

## Status

- **33/33 drug monographs** converted (`data/drugs.json`).
- **18 protocols** converted (`data/protocols.json`): Universal Patient Care (adult + peds), Asystole, PEA, V-Fib/Pulseless V-Tach, Chest Pain (ACS), Hypotension/Shock Non-Trauma, Altered Mental Status (adult + peds), Seizure (adult + peds), Suspected Stroke, Respiratory Distress (adult + peds), Overdose/Toxic Exposure, Allergic Reaction (adult + peds).
- **241 entries remaining** from the source book (full adult/peds sections, procedures, guidelines, reference tables) — raw verbatim text for all 259 source entries is already extracted in `source/raw/` with a page-mapped index in `source/manifest.json`, ready to convert in batches the same way the current set was built (see `source/build_protocols.py` for the pattern).

## How the data is structured

- `data/drugs.json` — one entry per medication: certification level, onset/peak/half-life, adult + pediatric dosing (verbatim text + structured per-kg/max fields where applicable), contraindications, adverse reactions, precautions, mechanism of action.
- `data/protocols.json` — one entry per protocol: chief-complaint search tags, demographic, the "Medical Reference" page content (history/signs/differential/pearls), and one or more **branches** (the protocol's clinical decision points, e.g. "Hives only" vs "Impending Arrest/Shock") each with an ordered list of **steps**. Steps can reference a `drug_id` (links to the drug database) or a `goto_protocol` (links to another protocol).
- The app's dose calculator (`js/app.js` → `computeDose`) scans step text for `mg/kg`, `mcg/kg`, `mL/kg` etc. patterns and multiplies by the entered weight, capping at any stated maximum — this works automatically for any future protocol you add, no extra tagging needed.

## Adding more protocols

1. Raw verbatim text for every remaining section is in `source/raw/###_slug.txt`, indexed in `source/manifest.json`.
2. Follow the pattern in `source/build_protocols.py` — each protocol becomes a Python dict with `id`, `title`, `demographic`, `chief_complaint_tags`, `reference`, and `branches` (each branch = a list of verbatim `steps`).
3. Re-run the script, copy the resulting `protocols.json` into `data/`.
4. Double-check every dose against `source/raw/` before trusting it in the field — this is the one step worth never skipping.

## Design

Soft Japanese color-art palette (sakura pink, washi cream, sumi ink, moss green) — calm rather than alarm-red, since this is meant to be usable under stress without adding to it. Dose numbers are always bolded on a high-contrast callout regardless of the palette, since that's the one thing that must never be skimmed past.
