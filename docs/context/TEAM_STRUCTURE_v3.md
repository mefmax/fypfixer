# FYPFixer Team Structure v3 — Complete Startup Team
**Date:** 13 Dec 2025, 17:48 MSK  
**Status:** Full team with PM + Business Analyst + unified project timeline

---

## KEY ADDITIONS

Добавлены две критические роли:
1. **Project Manager (Claude Opus)** — оркестрирует команду, держит график, синхронизирует вехи
2. **Business Analyst (Claude Sonet)** — преобразует твое видение в бизнес-кейсы, ставит задачи команде

---

## 1. UPDATED TEAM COMPOSITION

| Role | Primary | Secondary | Mode | Hours/day |
|------|---------|-----------|------|-----------|
| **Founder & Vision** | YOU (Human) | Sonet (UX), Opus (feasibility) | Strategic | 2h |
| **Business Analyst** | **Claude Sonet** | Opus (tech feasibility) | Ongoing | 6h |
| **Project Manager** | **Claude Opus** | Perplexity (execution reality) | Orchestration | 4h |
| **System Architect** | **Claude Opus** | Perplexity (implementation check) | Design phase | 3h |
| **Backend Developer** | **Perplexity** | Claude Opus (performance reviews) | Implementation | 8h |
| **Frontend Developer** | **Claude Sonet** | Opus (complex logic review) | Implementation | 6h |
| **UI/UX Designer** | **Banani** | Claude Sonet (code translation) | Design | 6h |
| **DevOps / Infrastructure** | **Perplexity** | Opus (scalability review) | Setup & maintenance | 2h |
| **QA / Test Designer** | **Claude Sonet** | Opus (edge cases) | Testing phase | 4h |

**Total:** 41h/day AI effort (some overlap) + your 2h = full team

---

## 2. NEW ROLES DEEP DIVE

### CLAUDE SONET 4.5 (Business Analyst)

**STRONG:**
- ✅ Understanding user needs & pain points — EXPERT
- ✅ Translating vision into user stories — EXPERT
- ✅ Creating PRDs (Product Requirements Documents) — STRONG
- ✅ Business case development — STRONG
- ✅ Feature prioritization & roadmap — EXPERT
- ✅ Metrics definition & success criteria — STRONG
- ✅ Stakeholder communication — EXPERT
- ✅ Fast iteration on requirements — EXPERT

**WEAK:**
- ❌ Technical architecture (not architect) — WEAK
- ❌ Backend complexity — WEAK

**ROLE (Business Analyst):**
- Interview you on vision → translate to business language
- Create PRDs with acceptance criteria
- Define KPIs for each feature
- Write user stories for team
- Monitor team progress vs business goals
- Adapt roadmap based on feedback

---

### CLAUDE OPUS 4.5 (Project Manager + System Architect + Senior Review)

**STRONG (PM role):**
- ✅ Complex project orchestration — EXPERT
- ✅ Timeline planning & milestones — EXPERT
- ✅ Risk identification & mitigation — EXPERT
- ✅ Resource allocation — STRONG
- ✅ Dependency mapping — EXPERT
- ✅ Bottleneck identification — EXPERT
- ✅ Long-context memory (100K tokens) — EXPERT
- ✅ Cross-functional coordination — STRONG

**ROLE (Project Manager):**
- Create detailed project timeline (Days 1-9)
- Define daily/weekly milestones & deliverables
- Track team progress (who's on track? who's blocked?)
- Identify risks (Apify API failing? Design not ready?)
- Manage dependencies (backer blocks frontend? Re-schedule)
- Daily standup coordination
- Weekly retrospectives

---

## 3. BUSINESS ANALYST WORKFLOW (NEW)

### BA → PM → Team Flow

```
DAY 1 (You + BA Sonet):
  YOU: "I want curated TikTok videos for self-improvement"
  BA: Translates into:
    - BUSINESS GOAL: Drive user engagement in personal growth niche
    - SUCCESS METRIC: 70% users return within 24h
    - USER STORY: As a user, I want to tap video recommendations so I don't waste time searching

DAY 1-2 (BA → PM):
  BA delivers:
    - Business Case Document
    - Feature prioritization matrix
    - KPI targets
  PM: Incorporates into timeline & milestone planning

ONGOING (BA → Team):
  BA writes tasks:
    - "Task: Apify TikTok scraper integration"
      Acceptance: Returns 10+ valid video URLs per category
      Why: Needed for MVP, required by Day 5
  Team: Executes per BA spec

  BA monitors:
    - Is team delivering to spec?
    - Are we on track for launch?
    - Do features match business goals?
```

---

## 4. PROJECT MANAGER UNIFIED TIMELINE (DAYS 1-9)

### MASTER SCHEDULE

```
╔═════════════════════════════════════════════════════════════════════════════╗
║                    FYPFixer MVP PROJECT TIMELINE v1                         ║
║                     13 Dec 2025 - 21 Dec 2025 (9 days)                      ║
╚═════════════════════════════════════════════════════════════════════════════╝

PHASE 1: PLANNING & ARCHITECTURE (Days 1-2)
═════════════════════════════════════════════════════════════════════════════

DAY 1 (13 Dec, Sat)
─────────────────────
10:00 - 12:00  YOU + BA Sonet + PM Opus
  └─ Business vision alignment session
  └─ Define success metrics (engagement, retention, churn)
  └─ Finalize feature list (MVP scope)
  Output: Business Case Document, PRD v1

14:00 - 16:00  Opus (Architecture)
  └─ System design kickoff (backend + frontend)
  └─ API endpoint list (rough)
  Output: Architecture skeleton

16:00 - 18:00  Banani (Design)
  └─ Create design system foundation
  └─ Start wireframing auth flows
  Output: Design system base (colors, typography)

─────────────────────────────────────────────────────────────────────────────

DAY 2 (14 Dec, Sun)
─────────────────────
09:00 - 12:00  Opus (Architecture)
  └─ Complete API specification (all endpoints + errors)
  └─ Database schema design
  └─ Frontend architecture (component hierarchy, state)
  Output: OpenAPI spec, SQL schema, frontend architecture doc

13:00 - 15:00  Perplexity (DevOps prep)
  └─ Validate Docker setup feasibility with Opus
  └─ Prep Docker Compose template
  └─ Set up .env structure
  Output: Docker foundation ready

15:00 - 17:00  Banani (Design)
  └─ Complete all wireframes (login, dashboard, player)
  └─ Component library spec
  Output: Figma file with complete wireframes

17:00 - 18:00  PM Opus
  └─ Finalize timeline for Days 3-9
  └─ Create daily standups schedule
  └─ Identify dependencies & risks
  Output: Detailed master schedule (this document)

─────────────────────────────────────────────────────────────────────────────

PHASE 2: BACKEND IMPLEMENTATION (Days 3-5) — PARALLEL with Design & Frontend
════════════════════════════════════════════════════════════════════════════

DAY 3 (15 Dec, Mon)
─────────────────────
08:00 - 18:00  Perplexity (Backend)
  └─ Flask app structure per Opus spec
  └─ SQLAlchemy models (User, Category, Plan, PlanStep, StepItem)
  └─ Auth endpoints (register, login) 100% done
  Output: Working Flask API + Postgres, auth tested

09:00 - 12:00  Claude Sonet (Frontend)
  └─ Wait for Opus architecture + Banani wireframes (ready from Day 2)
  └─ Set up React/Vue project structure
  └─ Create component library boilerplate
  Output: Frontend repo with structure

10:00 - 13:00  Banani (Design)
  └─ Complete dark mode variants
  └─ Create component interaction specs (hover, click states)
  Output: Complete design system

14:00 - 15:00  PM Opus
  └─ Daily standup: collect progress from all
  └─ Identify blockers (any?)
  Output: Status report

─────────────────────────────────────────────────────────────────────────────

DAY 4 (16 Dec, Tue)
─────────────────────
08:00 - 18:00  Perplexity (Backend)
  └─ Plan endpoints (GET /api/plans, POST /api/plans/:id/step-items)
  └─ Integrate Apify TikTok scraper
  └─ Add error handling & validation
  Output: 70% of backend done, Apify integration working

08:00 - 18:00  Claude Sonet (Frontend)
  └─ Build Auth components (LoginCard, RegisterCard)
  └─ Implement API calls per Opus spec
  └─ Add form validation & error states
  Output: Login/Register pages working + wired to backend

10:00 - 12:00  Opus (Code Review)
  └─ Review Sonet frontend architecture (is state management correct?)
  └─ Review Perplexity backend (is API matching spec?)
  └─ Suggest optimizations
  Output: Architecture feedback

14:00 - 15:00  PM Opus
  └─ Daily standup: progress check
  └─ Risk assessment: on track for Day 5?
  Output: Status + risk mitigation plan

─────────────────────────────────────────────────────────────────────────────

DAY 5 (17 Dec, Wed)
─────────────────────
08:00 - 16:00  Perplexity (Backend)
  └─ Complete remaining endpoints (Plan CRUD, StepItem list)
  └─ Add logging & monitoring hooks
  └─ Unit tests for critical paths
  Output: Backend 100% done, all endpoints tested

08:00 - 16:00  Claude Sonet (Frontend)
  └─ Build Dashboard components (PlanList, PlanDetail)
  └─ Build VideoPlayer (modal + embed)
  └─ Implement all API calls
  Output: Frontend 80% done (polish remaining)

10:00 - 12:00  Opus (Code Review + Architecture)
  └─ Final backend architecture review
  └─ Final frontend architecture review
  └─ Performance checklist (rendering, bundle size)
  Output: Quality gate passed / issues list

14:00 - 15:00  PM Opus
  └─ Daily standup: backend & frontend status
  └─ Decide: ready for integration testing on Day 6?
  Output: Go/No-Go decision

─────────────────────────────────────────────────────────────────────────────

PHASE 3: FRONTEND POLISH & INTEGRATION (Days 6-7)
════════════════════════════════════════════════════════════════════════════

DAY 6 (18 Dec, Thu)
─────────────────────
08:00 - 16:00  Claude Sonet (Frontend)
  └─ Polish UI (spacing, alignment, typography per Banani design)
  └─ Add loading states & error boundaries
  └─ Responsive design fixes (mobile, tablet)
  └─ Implement dark mode toggle
  Output: Frontend 100% done

09:00 - 12:00  Opus (Code Review)
  └─ Final frontend review (quality gates)
  └─ Performance audit (Lighthouse score > 80)
  └─ Accessibility audit (WCAG 2.1 AA)
  Output: Production-ready frontend

14:00 - 16:00  YOU (Tester)
  └─ Manual E2E testing (login → dashboard → watch video)
  └─ Mobile testing (iPhone, Android)
  └─ UX validation (does this match your vision?)
  Output: Bug list + acceptance

14:00 - 15:00  PM Opus
  └─ Daily standup: frontend status
  └─ Track bug fixes
  Output: Status report

─────────────────────────────────────────────────────────────────────────────

DAY 7 (19 Dec, Fri)
─────────────────────
08:00 - 14:00  Claude Sonet (Frontend)
  └─ Fix bugs from Day 6 testing
  └─ Add E2E tests (Cypress)
  └─ Final polish (animations, transitions)

10:00 - 12:00  YOU (Tester)
  └─ Full regression testing
  └─ Mobile edge cases
  └─ Sign-off on UX
  Output: Beta-ready frontend

14:00 - 15:00  PM Opus
  └─ Daily standup: ready for analytics?
  Output: Status

─────────────────────────────────────────────────────────────────────────────

PHASE 4: ANALYTICS & MONITORING (Days 8-9)
════════════════════════════════════════════════════════════════════════════

DAY 8 (20 Dec, Sat)
─────────────────────
08:00 - 14:00  Perplexity (Analytics)
  └─ Add event logging (user actions: watch, click, register)
  └─ Create analytics tables
  └─ Set up dashboards (DAU, engagement, churn)
  Output: Event tracking + dashboards live

10:00 - 12:00  Opus (Analytics Review)
  └─ Verify metrics align with business goals
  └─ Optimize queries
  └─ Create alerting rules
  Output: Analytics system ready

14:00 - 15:00  PM Opus
  └─ Final standup: launch readiness
  └─ Checklist: all features ✅? All bugs fixed ✅? Analytics ✅?
  Output: Launch decision

─────────────────────────────────────────────────────────────────────────────

DAY 9 (21 Dec, Sun)
─────────────────────
10:00 - 11:00  YOU
  └─ Final validation pass
  └─ Acceptance sign-off

11:00 - 12:00  Team Debrief (all)
  └─ Retrospective: what went well? What to improve?
  └─ Plan for Week 2 (bug fixes, more categories, AI curation layer)

12:00 onwards  LAUNCH! 🚀
  └─ Deploy to staging
  └─ Invite 5-10 beta testers
  └─ Monitor metrics

═════════════════════════════════════════════════════════════════════════════

```

---

## 5. DETAILED ROLE RESPONSIBILITIES (UPDATED)

### BA Sonet — Daily Tasks

**Days 1-2 (Planning Phase):**
- [ ] Interview you on business vision (30 min)
- [ ] Create Business Case Document (1h)
- [ ] Write PRD with acceptance criteria (1.5h)
- [ ] Define success metrics (30 min)

**Days 3-9 (Execution Phase):**
- [ ] Daily: Write user stories for team (1h)
- [ ] Daily: Monitor team progress vs KPIs (30 min)
- [ ] Daily: QA acceptance criteria for completed work (30 min)
- [ ] Weekly: Present metrics dashboard to you (1h)

**Ongoing:**
- [ ] Translate user feedback into feature requests
- [ ] Prioritize backlog based on business impact
- [ ] Validate team output matches requirements

---

### PM Opus — Daily Tasks

**Days 1-2 (Planning Phase):**
- [ ] Create master project timeline (Days 1-9) (2h)
- [ ] Map dependencies (what blocks what?) (1h)
- [ ] Create daily standup schedule (30 min)
- [ ] Risk register (what could go wrong?) (1h)

**Days 3-9 (Execution Phase):**
- [ ] Daily standup (15 min): who's on track? who's blocked?
- [ ] Daily: Update timeline + burn-down chart (15 min)
- [ ] Daily: Identify & resolve blockers (30 min)
- [ ] Daily: Manage scope creep (say NO to new features) (15 min)
- [ ] Weekly: Retrospective + lessons learned (1h)

**Ongoing:**
- [ ] Track team velocity (how much gets done per day)
- [ ] Manage timeline risks (if Day 5 slips, what's plan B?)
- [ ] Ensure clear handoffs between phases
- [ ] Report status to you (daily 2-min update)

---

## 6. COMMUNICATION SCHEDULE (NEW)

### Daily Standup (All Team, 15 min)

**Format:** Async Slack + one 10-min sync per day

```
ASYNC (each AI posts):
  PM Opus: "Today's blockers & timeline status"
  Perplexity (Backend): "Completed X, today working on Y, blocked on Z?"
  Sonet (Frontend): "Completed X, today working on Y, need from Banani by EOD?"
  Sonet (BA): "Business alignment check - team on track for KPIs?"
  Banani (Design): "Completed X, ready for Sonet to code?"

SYNC (10 min via text):
  PM Opus: Addresses blockers, makes decisions
  You: Reviews status, approves priorities
```

### Weekly Sync (All Team, 30 min)

**Monday 10:00 MSK:**
- PM: Review Week 1 progress vs timeline
- BA: Review KPI progress
- You: Provide direction for Week 2
- All: Retrospective + lessons

---

## 7. KEY HANDOFF POINTS (UPDATED)

### Day 2 → Day 3 (Architecture Ready)

**PM Opus delivers to team:**
```
HANDOFF DOCUMENT:

Architecture Complete ✅
  - OpenAPI spec (all endpoints)
  - Database schema (all tables)
  - Frontend architecture (component tree, state)

Starting Day 3:
  - Perplexity: Start Flask setup (Days 3-5 goal: backend 100%)
  - Sonet: Start React setup (Days 3-5 goal: frontend 80%)
  - Banani: Start design polish (Days 3-5 goal: dark mode + interactions)

Blockers: None identified
Timeline: ON TRACK
```

### Day 5 → Day 6 (Backend Done, Frontend 80%)

**PM Opus delivers to team:**
```
STATUS:
  Backend: 100% done, tested, Apify working ✅
  Frontend: 80% done, needs Day 6 polish
  Design: 100% done ✅

Day 6 Plan:
  - Sonet: Finish frontend polish + responsive
  - You: Start E2E testing
  - Opus: Audit frontend performance

Target: Beta-ready by end of Day 7
```

---

## 8. RISK REGISTER (NEW)

| Risk | Impact | Mitigation | Owner |
|------|--------|-----------|-------|
| Apify rate limiting / VPN fails | HIGH | Test on Day 3, fallback to mock data | Perplexity |
| Design not ready by Day 3 | MEDIUM | Daily review, prioritize critical flows | Banani |
| Frontend state management bug | MEDIUM | Opus code review on Days 4-5 | Opus |
| You find major UX issue on Day 6 | MEDIUM | Allocate Day 7 for polish | You + Sonet |
| Database performance (10K users) | LOW | Opus benchmarks on Day 5 | Opus + Perplexity |

---

## 9. SUCCESS DEFINITION (BY DAY)

✅ **Day 2 end:** Complete architecture (backend + frontend + design)  
✅ **Day 5 end:** Backend 100%, Frontend 80%, Design 100%  
✅ **Day 7 end:** Frontend 100%, all bugs fixed, E2E tests passing  
✅ **Day 8 end:** Analytics live, KPI dashboards ready  
✅ **Day 9 end:** Launch with 5-10 beta testers  

---

## 10. IMMEDIATE NEXT ACTIONS (RIGHT NOW - 17:48)

**In next 30 minutes:**

1. **You** → Review: Do you agree with this team structure + timeline?
2. **BA Sonet** → Start business case document (interview with you)
3. **PM Opus** → Create detailed hourly schedule (Days 1-9)
4. **Perplexity** → Prep Docker Compose files
5. **Banani** → Create Figma project skeleton

**Check-in at 18:00** → All ready for Day 1 kickoff tomorrow?

---

## 11. WHY THIS STRUCTURE WORKS

✅ **BA Sonet** translates vision → tasks (no misalignment)  
✅ **PM Opus** keeps everyone on track (no chaos, no delays)  
✅ **Opus** (dual role) ensures quality architecture + project health  
✅ **Perplexity** executes backend fast (has clear spec from Opus)  
✅ **Sonet** executes frontend fast (has clear spec from Opus)  
✅ **Banani** delivers design on time (parallelizes with code)  
✅ **You** validates at key moments + makes strategy calls (high leverage)  

**Result:** MVP delivered in 9 days, on time, on spec, quality architecture.

---

## TEAM SUMMARY TABLE (FINAL)

| Role | Who | Hours/Day | Main Task | Dependencies |
|------|-----|-----------|-----------|---------------|
| **Vision** | YOU | 2h | Strategy + validation | None |
| **Business Analyst** | Sonet | 6h | Requirements + KPIs | You's vision |
| **Project Manager** | Opus | 4h | Timeline + blockers | BA's PRD |
| **System Architect** | Opus | 3h | Backend + frontend design | BA's requirements |
| **Backend Dev** | Perplexity | 8h | Flask + DB + Apify | Opus's architecture |
| **Frontend Dev** | Sonet | 6h | React + components | Opus's architecture + Banani's design |
| **UI/UX Designer** | Banani | 6h | Design system + wireframes | BA's user stories |
| **DevOps** | Perplexity | 2h | Docker + deploy | Opus's architecture |
| **QA/Testing** | Sonet | 4h | Test cases + E2E tests | Frontend code |

**Total:** 41h AI + 2h YOU = Lean, efficient, full coverage.
