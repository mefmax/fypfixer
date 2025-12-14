# FYPFixer Project Context — Session 2 (Perplexity TikTok Script Focus)
**Updated:** 2025-12-09, 2300 MSK  
**Status:** Script in development (fixing syntax errors and JSON parsing)

---

## 0. Quick Summary

**FYPFixer** = AI-powered daily checklists with real TikTok video links for personal growth/self-improvement.  
**Current Focus:** Fix and finalize `generate_videos_with_perplexity.py` script that:
- Fetches real TikTok videos from Perplexity API via 3 fallback levels
- Parses JSON from markdown-wrapped responses
- Saves video metadata to DB (StepItem table)
- Runs via Docker: `docker compose exec web python generate_videos_with_perplexity.py`

---

## 1. Development Environment (CRITICAL — Do Not Vary)

- **OS:** Windows 11
- **IDE:** VS Code (PowerShell terminal, no bash)
- **Framework:** Python 3.11 + Flask + SQLAlchemy
- **Deployment:** Docker Compose (web, postgres, redis)
- **Execution:** Commands like `docker compose exec web python script.py` (NOT bash cat/EOF)

**Remember:** Always suggest VS Code file edits, PowerShell/terminal commands. No bash constructs.

---

## 2. What `generate_videos_with_perplexity.py` Does

**Goal:** For each DB category (fitness, creative, travel, etc.), generate a Plan with video recommendations.

**Flow:**
1. Connect to Perplexity API (`sonar-pro` model) via OpenAI SDK
2. Ask for REAL TikTok videos in 3 levels (stop at first success):
   - **Level 1:** Direct search → "Search for 10 REAL trending TikTok videos about [category]"
   - **Level 2:** Hashtag discovery → "Find REAL videos using trending hashtags"
   - **Level 3:** Creator search → "Find creators in [category] and their viral videos"
3. Validate URLs strictly (must start with `https://www.tiktok.com/@`, have `/video/7` pattern)
4. Save to DB: Plan → PlanStep → StepItem (video metadata)
5. Only update old videos if new ones found (don't pollute DB)

---

## 3. Critical Problems from Today

### Problem A: API Returns JSON in Markdown Blocks
Perplexity often wraps JSON in:
```
```json
{"videos": [...]}
```
```
Not as raw JSON. **Solution:** Function `extract_json_from_response()` parses this.

### Problem B: Triple Backticks in Python Code
When copying code from chat markdown, ``` characters were entering the `.py` file as literals.
**Solution:** Rewrote code WITHOUT any literal ``` in strings — use `marker = "```"` as string literal instead.

### Problem C: Syntax Errors Around Line 38
Code sections with multi-line docstrings or missing function definitions were causing parse errors.
**Solution:** Ensure all functions properly indented, all docstrings closed with `"""`.

### Problem D: Mock Videos Not Needed (Removed)
Previously tried to add fallback mock videos dict — user rejected. Now: **3 levels only, fail gracefully if no videos found.**

---

## 4. Current Script Architecture

```
extract_json_from_response(content: str) → str
  ↓ Strips ```json...``` markers, returns clean JSON string
  
try_direct_tiktok_search() → list
try_hashtag_discovery() → list  
try_creator_search() → list
  ↓ Each calls OpenAI/Perplexity, validates URLs, returns real_videos
  
fetch_videos_from_perplexity() → list
  ↓ Tries Level 1 → sleep(1) → Level 2 → sleep(1) → Level 3 → return []
  
save_videos_to_db() → int
  ↓ Validates each video URL, adds StepItem records, commits
  
main()
  ↓ Iterates all categories, creates/gets Plan/PlanStep, calls fetch + save
```

**Key Logic:**
- Stop at first level that returns videos (don't waste API calls)
- Only delete old videos if new ones found
- Skip category if no videos (no DB pollution)
- Print debug info: which level succeeded, how many videos

---

## 5. Known Current Issues

1. **Syntax error near line 38** — Last run showed:  
   ```
   File "/app/generate_videos_with_perplexity.py", line 38
   ```
   Likely: Unclosed docstring in `extract_json_from_response()` or indentation issue.

2. **JSON parsing errors** — Some Perplexity responses still return empty arrays after successful extraction.

3. **No real videos found** — API may be rate-limited or not returning TikTok URLs in expected format.

---

## 6. Database Relevant to Script

**Tables involved:**
- `categories` (id, code, name_en, name_ru, name_es, is_premium)
- `plans` (id, user_id, category_id, plan_date, language, title)
- `plansteps` (id, plan_id, step_order, action_type, text_en, text_ru, text_es)
- **`stepitems`** (id, plan_step_id, video_id, creator_username, title, thumbnail_url, **video_url**, engagement_score, reason_text)

**The script populates `stepitems` with real TikTok video data.**

---

## 7. Next Steps (Priority Order)

1. **Fix syntax error** — Paste clean code into VS Code, verify line 30–50 (docstring, function defs)
2. **Test locally** — `docker compose exec web python generate_videos_with_perplexity.py` on first category only
3. **Debug JSON extraction** — Add print statements to see raw API response
4. **Validate URLs** — Ensure Perplexity returns `https://www.tiktok.com/@...` links
5. **Scale to all categories** — Once working for `personal_growth`, run full script

---

## 8. Files & Paths

```
FYPFixer/
├── generate_videos_with_perplexity.py  ← FOCUS (in /app or root)
├── app/
│   ├── __init__.py (Flask app factory)
│   ├── models.py (Category, Plan, PlanStep, StepItem)
│   └── routes/
│       ├── plan.py (GET /api/plan)
│       └── health.py (GET /api/health)
├── docker-compose.yml
├── .env (PERPLEXITY_API_KEY, DATABASE_URL, etc.)
└── requirements.txt
```

---

## 9. API Key & Config

```
.env:
PERPLEXITY_API_KEY=pplx-<KEY>
DATABASE_URL=postgresql://...
FLASK_ENV=development
```

The script reads `PERPLEXITY_API_KEY` from `.env`.

---

## 10. Communication Protocol

- **This file is source of truth** — Update it after each session
- **Before each chat:** Read latest version to avoid repeating context
- **One session = one script issue** — Focus on get-and-save flow, then move to UI/analytics
- **Git discipline:** Commit working versions to main with clear messages

---

## 11. Last Session Summary (Today)

**What We Tried:**
- Started with broken script that returned `{"videos": []}`
- Identified: Perplexity wraps JSON in markdown code blocks
- Added `extract_json_from_response()` to parse it
- Removed mock video fallback (user rejected)
- Rewrote entire script WITHOUT triple-backticks as literals

**What Broke:**
- Syntax error on line 38 (possible unclosed docstring or indentation)
- JSON parsing still timing out or returning empty on Level 2

**What's Next:**
- Fix syntax error and test first 3 categories
- Debug raw API responses to confirm JSON structure
- Get 1 working category, then scale

---

## 12. Command Reference

```powershell
# Check script syntax
python -m py_compile generate_videos_with_perplexity.py

# Run script in container
docker compose exec web python generate_videos_with_perplexity.py

# View last 50 lines of logs
docker compose logs -f web | head -50

# Fresh start (clear DB)
docker compose down -v
docker compose build web
docker compose up -d

# Check if service is running
docker compose ps

# Access container shell
docker compose exec web bash
```

---

## 13. Debugging Checklist

- [ ] Script imports all modules (openai, json, dotenv, sqlalchemy)
- [ ] API key loaded from .env without errors
- [ ] First function defined with proper docstring `"""..."""`
- [ ] All `if/for/try` blocks have matching `:` and indentation
- [ ] No triple-backticks ``` in any string literals (only as `marker = "..."`)
- [ ] DB session commits after each batch of saves
- [ ] Category loop prints progress for each category

---

**Status:** WIP — Awaiting syntax fix and first successful test run.  
**Owner:** You (founder/tester), AI (debug/refactor).
