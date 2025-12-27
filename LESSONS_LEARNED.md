# FYPGlow Lessons Learned

## Project Overview
- Duration: 10 days (Day 1-10)
- Team: Multi-Claude workflow (Architect, DEV, PROD)
- Result: Production-ready MVP deployed

## What Worked Well

### 1. Multi-Claude Workflow
- **Architect Claude**: High-level design, task breakdown, TXT prompt generation
- **DEV Claude**: Code implementation, testing, documentation
- **PROD Claude**: Deployment, infrastructure, security hardening
- Clear separation of concerns prevented conflicts

### 2. TXT Prompt Files
- Each task had a dedicated `.txt` file with:
  - Clear context and goals
  - Step-by-step instructions
  - Expected outputs
- Easy handoff between Claude instances
- Reproducible task execution

### 3. Parallel Workstreams
- DEV and PROD could work simultaneously on different tasks
- Daily sync points to merge changes
- Reduced overall development time

### 4. Incremental Commits
- Small, focused commits (feat/fix/refactor/docs)
- Easy to track progress and rollback if needed
- Clear git history for future reference

### 5. Code Review Cycle
- R2.1: Backend code review (23 issues found)
- R2.2: Frontend code review (18 issues found)
- Critical issues fixed immediately
- Major/minor issues documented for v2.1

## Challenges Encountered

### 1. TikTok OAuth + PKCE Complexity
- **Problem**: Different encoding requirements for desktop vs web
  - Desktop: HEX-encoded code_challenge
  - Web: Base64URL-encoded code_challenge
- **Solution**: Auto-detect platform in pkce.ts, use appropriate encoding
- **Lesson**: Read OAuth provider docs carefully, test both flows

### 2. Database Migration Dependency Chains
- **Problem**: Migrations referencing non-existent tables
- **Solution**: Careful ordering with `depends_on` in Alembic
- **Lesson**: Test migrations on fresh database before PROD

### 3. DEV/PROD Branch Sync
- **Problem**: Divergent commits causing merge conflicts
- **Solution**: Frequent pulls, rebase workflow
- **Lesson**: Sync at least twice daily during parallel work

### 4. Environment Secrets Management
- **Problem**: Accidentally committing .env files
- **Solution**: .gitignore, .env.example template
- **Lesson**: Never put real secrets in code, use environment variables

### 5. TypeScript Strict Mode
- **Problem**: Legacy `any` types causing runtime errors
- **Solution**: Replace with `unknown` + type narrowing
- **Lesson**: Enable strict mode from day 1

## Technical Debt for v2.1

### Backend (21 issues)
| Priority | Count | Examples |
|----------|-------|----------|
| Critical | 2 | Business logic in routes (FIXED) |
| Major | 8 | Missing input validation, error handling |
| Minor | 11 | Magic numbers, missing docstrings |

### Frontend (11 issues)
| Priority | Count | Examples |
|----------|-------|----------|
| Critical | 1 | Missing ErrorBoundary (FIXED) |
| Major | 6 | `any` types, missing alt tags (FIXED) |
| Minor | 4 | Unused imports, console.log (FIXED) |

### Security
- CSP `unsafe-inline` for styles (Tailwind requirement)
- Missing rate limit on some endpoints
- No CAPTCHA on registration

### Testing
- No unit tests for services
- No integration tests for OAuth flow
- No E2E tests

## Recommendations for Future Projects

### 1. Start with Strict TypeScript
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true
  }
}
```

### 2. Service Layer from Day 1
```
Routes -> Services -> Models
(thin)    (logic)    (data)
```

### 3. Automated Testing Pipeline
```yaml
# CI/CD
- lint
- type-check
- unit-tests
- integration-tests
- deploy (if all pass)
```

### 4. Daily Sync Protocol
1. Morning: Pull latest from main
2. Work on isolated feature branch
3. Evening: Rebase, resolve conflicts, push

### 5. Documentation as Code
- Keep docs in repo (not external)
- Update docs with each feature
- Architecture diagrams in Markdown

## Metrics

### Lines of Code
- Backend: ~3,500 lines (Python)
- Frontend: ~5,000 lines (TypeScript)
- Config/Docker: ~500 lines

### Commits
- Total: ~50 commits
- Average: 5 commits/day

### Issues Found in Review
- Backend: 23 issues
- Frontend: 18 issues
- Fixed before release: 10 (critical + some major)

## Conclusion

The multi-Claude workflow proved effective for rapid MVP development. Clear task definitions, parallel workstreams, and incremental commits enabled delivery in 10 days. Main areas for improvement: testing coverage, stricter TypeScript from start, and earlier security hardening.
