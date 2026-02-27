#!/usr/bin/env python3
"""
serpapi-pro — Advanced SerpAPI wrapper for OpenClaw
Supports: Google (multi-page), LinkedIn, Google Maps, Google Jobs
Export: JSON, CSV
"""

import os
import sys
import json
import csv
import argparse
import urllib.request
import urllib.parse
import urllib.error
from typing import List, Dict, Any, Optional

# ── Config ────────────────────────────────────────────────────────────────────
BASE_URL = "https://serpapi.com/search.json"
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")
NUM_PER_PAGE = int(os.environ.get("SERPAPI_NUM_PER_PAGE", "20"))
PAGES_PER_SOURCE = int(os.environ.get("SERPAPI_PAGES_PER_SOURCE", "3"))
TOTAL_LIMIT = int(os.environ.get("SERPAPI_TOTAL_LIMIT", "100"))


def fetch(params: Dict[str, Any]) -> Dict:
    """Make a GET request to SerpAPI and return JSON."""
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"[ERROR] HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[ERROR] Network error: {e.reason}", file=sys.stderr)
        sys.exit(1)


# ── Google Search (multi-page) ────────────────────────────────────────────────
def search_google(query: str, pages: int = PAGES_PER_SOURCE, num: int = NUM_PER_PAGE,
                  limit: int = TOTAL_LIMIT, api_key: str = SERPAPI_KEY) -> List[Dict]:
    results = []
    for page in range(pages):
        start = page * num
        params = {
            "engine": "google",
            "q": query,
            "num": num,
            "start": start,
            "api_key": api_key,
        }
        data = fetch(params)
        organic = data.get("organic_results", [])
        if not organic:
            break
        for r in organic:
            results.append({
                "title": r.get("title", ""),
                "link": r.get("link", ""),
                "snippet": r.get("snippet", ""),
                "source": r.get("source", ""),
                "engine": "google",
                "page": page + 1,
            })
        if len(results) >= limit:
            results = results[:limit]
            break
        # Stop if fewer results than requested (last page)
        if len(organic) < num:
            break
    print(f"[INFO] Google: {len(results)} results for '{query}'", file=sys.stderr)
    return results


# ── LinkedIn Search (via Google) ──────────────────────────────────────────────
def search_linkedin(query: str, pages: int = PAGES_PER_SOURCE, num: int = NUM_PER_PAGE,
                    limit: int = TOTAL_LIMIT, api_key: str = SERPAPI_KEY) -> List[Dict]:
    linkedin_query = f"site:linkedin.com/in/ {query}"
    raw = search_google(linkedin_query, pages=pages, num=num, limit=limit, api_key=api_key)
    results = []
    for r in raw:
        results.append({
            "title": r["title"],
            "link": r["link"],
            "snippet": r["snippet"],
            "engine": "linkedin",
            "page": r["page"],
        })
    print(f"[INFO] LinkedIn: {len(results)} profiles for '{query}'", file=sys.stderr)
    return results


# ── Google Maps ───────────────────────────────────────────────────────────────
def search_maps(query: str, pages: int = PAGES_PER_SOURCE,
                limit: int = TOTAL_LIMIT, api_key: str = SERPAPI_KEY) -> List[Dict]:
    results = []
    next_page_token = None

    for page in range(pages):
        params: Dict[str, Any] = {
            "engine": "google_maps",
            "q": query,
            "type": "search",
            "api_key": api_key,
        }
        if next_page_token:
            params["next_page_token"] = next_page_token

        data = fetch(params)
        places = data.get("local_results", [])
        if not places:
            break

        for r in places:
            results.append({
                "title": r.get("title", ""),
                "link": r.get("website", ""),
                "address": r.get("address", ""),
                "phone": r.get("phone", ""),
                "rating": r.get("rating", ""),
                "reviews": r.get("reviews", ""),
                "type": ", ".join(r.get("type", [])) if isinstance(r.get("type"), list) else r.get("type", ""),
                "snippet": r.get("description", ""),
                "engine": "google_maps",
                "page": page + 1,
            })

        if len(results) >= limit:
            results = results[:limit]
            break

        next_page_token = data.get("serpapi_pagination", {}).get("next_page_token")
        if not next_page_token:
            break

    print(f"[INFO] Maps: {len(results)} results for '{query}'", file=sys.stderr)
    return results


# ── Google Jobs ───────────────────────────────────────────────────────────────
def search_jobs(query: str, pages: int = PAGES_PER_SOURCE,
                limit: int = TOTAL_LIMIT, api_key: str = SERPAPI_KEY) -> List[Dict]:
    results = []
    next_page_token = None

    for page in range(pages):
        params: Dict[str, Any] = {
            "engine": "google_jobs",
            "q": query,
            "api_key": api_key,
        }
        if next_page_token:
            params["next_page_token"] = next_page_token

        data = fetch(params)
        jobs = data.get("jobs_results", [])
        if not jobs:
            break

        for r in jobs:
            results.append({
                "title": r.get("title", ""),
                "company": r.get("company_name", ""),
                "location": r.get("location", ""),
                "link": r.get("related_links", [{}])[0].get("link", "") if r.get("related_links") else "",
                "snippet": r.get("description", "")[:300] if r.get("description") else "",
                "posted": r.get("detected_extensions", {}).get("posted_at", ""),
                "salary": r.get("detected_extensions", {}).get("salary", ""),
                "engine": "google_jobs",
                "page": page + 1,
            })

        if len(results) >= limit:
            results = results[:limit]
            break

        next_page_token = data.get("serpapi_pagination", {}).get("next_page_token")
        if not next_page_token:
            break

    print(f"[INFO] Jobs: {len(results)} results for '{query}'", file=sys.stderr)
    return results


# ── Export ────────────────────────────────────────────────────────────────────
def export_json(results: List[Dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[INFO] Exported {len(results)} results → {path}", file=sys.stderr)


def export_csv(results: List[Dict], path: str):
    if not results:
        print("[WARN] No results to export.", file=sys.stderr)
        return
    keys = list(results[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)
    print(f"[INFO] Exported {len(results)} results → {path}", file=sys.stderr)


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="serpapi-pro — Advanced SerpAPI CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 serpapi.py google "OpenAI GPT" --pages 3
  python3 serpapi.py linkedin "CEO Maroc tech" --pages 2
  python3 serpapi.py maps "restaurants Casablanca"
  python3 serpapi.py jobs "Python developer remote"
  python3 serpapi.py google "AI startup" --output results.csv
  python3 serpapi.py linkedin "CTO Paris" --output leads.json
        """,
    )
    parser.add_argument("engine", choices=["google", "linkedin", "maps", "jobs"],
                        help="Search engine to use")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--pages", type=int, default=PAGES_PER_SOURCE,
                        help=f"Number of pages to fetch (default: {PAGES_PER_SOURCE})")
    parser.add_argument("--num", type=int, default=NUM_PER_PAGE,
                        help=f"Results per page for Google (default: {NUM_PER_PAGE})")
    parser.add_argument("--limit", type=int, default=TOTAL_LIMIT,
                        help=f"Max total results (default: {TOTAL_LIMIT})")
    parser.add_argument("--output", type=str, default=None,
                        help="Output file path (.json or .csv)")
    parser.add_argument("--key", type=str, default=SERPAPI_KEY,
                        help="SerpAPI key (overrides SERPAPI_KEY env var)")
    parser.add_argument("--pretty", action="store_true",
                        help="Pretty-print JSON to stdout even when exporting")

    args = parser.parse_args()

    if not args.key:
        print("[ERROR] No SERPAPI_KEY found. Set env var or use --key.", file=sys.stderr)
        sys.exit(1)

    # Dispatch
    if args.engine == "google":
        results = search_google(args.query, pages=args.pages, num=args.num,
                                limit=args.limit, api_key=args.key)
    elif args.engine == "linkedin":
        results = search_linkedin(args.query, pages=args.pages, num=args.num,
                                  limit=args.limit, api_key=args.key)
    elif args.engine == "maps":
        results = search_maps(args.query, pages=args.pages,
                              limit=args.limit, api_key=args.key)
    elif args.engine == "jobs":
        results = search_jobs(args.query, pages=args.pages,
                              limit=args.limit, api_key=args.key)
    else:
        print(f"[ERROR] Unknown engine: {args.engine}", file=sys.stderr)
        sys.exit(1)

    # Export
    if args.output:
        if args.output.endswith(".csv"):
            export_csv(results, args.output)
        else:
            export_json(results, args.output)
        if args.pretty:
            print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
