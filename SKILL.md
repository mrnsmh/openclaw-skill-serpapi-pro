---
name: serpapi-pro
description: Advanced SerpAPI wrapper — Google multi-page search, LinkedIn, Google Maps, Google Jobs, with automatic pagination and CSV/JSON export.
license: MIT
metadata:
  version: 1.0.0
  author: Jack2
  tags: serpapi, google, search, linkedin, maps, jobs, contacts
---

# serpapi-pro

Advanced SerpAPI wrapper for OpenClaw. Supports Google search with automatic pagination, LinkedIn profile search, Google Maps business search, Google Jobs, and exports to CSV/JSON.

## Setup

Set your SerpAPI key as an environment variable:

```bash
export SERPAPI_KEY=your_key_here
```

Or pass it via `--key` flag.

**Default config:**
- `SERPAPI_NUM_PER_PAGE=20` — results per page
- `SERPAPI_PAGES_PER_SOURCE=3` — default pages to fetch
- `SERPAPI_TOTAL_LIMIT=100` — max total results

## Usage

```bash
# Google search with pagination
python3 scripts/serpapi.py google "OpenAI GPT" --pages 3

# LinkedIn people search
python3 scripts/serpapi.py linkedin "CEO Maroc tech"

# Google Maps local businesses
python3 scripts/serpapi.py maps "restaurants Casablanca"

# Google Jobs
python3 scripts/serpapi.py jobs "Python developer remote"

# Export to JSON or CSV
python3 scripts/serpapi.py google "AI startup" --output results.json
python3 scripts/serpapi.py linkedin "CTO Paris" --output leads.csv

# Limit results
python3 scripts/serpapi.py google "machine learning" --pages 5 --limit 50
```

## Engines Reference

See `references/engines.md` for all supported SerpAPI engines and their parameters.

## Output

Results are printed as JSON to stdout by default. Use `--output file.csv` or `--output file.json` to export.

Each result includes: `title`, `link`, `snippet`, `source`, `engine`, `page` (for Google), plus engine-specific fields.
