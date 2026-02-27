# SerpAPI Engines Reference

Full docs: https://serpapi.com/search-api

## Supported Engines & Key Parameters

### `google` — Google Search
| Param | Description | Default |
|---|---|---|
| `q` | Search query | required |
| `num` | Results per page | 10 (max 100) |
| `start` | Offset (pagination) | 0 |
| `gl` | Country code | us |
| `hl` | Language | en |
| `safe` | Safe search | off |
| `tbm` | Search type: `nws` (news), `isch` (images), `vid` (videos) | — |

**Pagination:** increment `start` by `num` for each page.

---

### `google_maps` — Google Maps
| Param | Description |
|---|---|
| `q` | Business/place query |
| `ll` | GPS coordinates `@lat,lng,zoom` |
| `type` | `search` or `place` |
| `next_page_token` | Pagination token from previous result |

---

### `google_jobs` — Google Jobs
| Param | Description |
|---|---|
| `q` | Job title + keywords |
| `location` | Location filter |
| `chips` | Filters (e.g. `date_posted:week`) |
| `next_page_token` | Pagination token |

---

### `google_local` — Google Local Results
| Param | Description |
|---|---|
| `q` | Business query |
| `location` | City/region |
| `num` | Number of results |

---

### `linkedin` (via Google)
Searches `site:linkedin.com/in/ <query>` using Google engine.

---

### `bing` — Bing Search
| Param | Description |
|---|---|
| `q` | Query |
| `count` | Results per page (max 50) |
| `offset` | Pagination offset |
| `mkt` | Market (e.g. `en-US`) |

---

### `duckduckgo` — DuckDuckGo
| Param | Description |
|---|---|
| `q` | Query |
| `kl` | Region (e.g. `fr-fr`) |

---

### `youtube` — YouTube Search
| Param | Description |
|---|---|
| `search_query` | Search query |
| `sp` | Filter code |

---

## Base URL
```
https://serpapi.com/search.json
```

All requests require `api_key` parameter.
