# Backend Code Review Report
## Date: 2025-12-27

### Summary
- Files reviewed: 45+
- Issues found: 23
- Critical: 2
- Major: 8
- Minor: 13

---

## Critical Issues

### CRIT-1: Business Logic in Routes (admin_metrics.py)
- **File**: `app/routes/admin_metrics.py`
- **Lines**: 74-340
- **Problem**: Heavy database queries and business logic directly in route handlers instead of services. 14+ `db.session.query()` calls.
- **Impact**: Violates separation of concerns, makes testing harder, code duplication risk.
- **Fix**: Extract to `AdminMetricsService` with methods like `get_overview()`, `get_challenge_funnel()`, `get_plan_metrics()`, `get_system_health()`.

### CRIT-2: Business Logic in Routes (oauth.py)
- **File**: `app/routes/oauth.py`
- **Lines**: 122-144
- **Problem**: User creation/update logic directly in route instead of `AuthService`.
- **Impact**: Mixing HTTP concerns with business logic.
- **Fix**: Move to `auth_service.find_or_create_oauth_user(provider, oauth_id, display_name, avatar_url)`.

---

## Major Issues

### MAJ-1: Missing Admin Role System
- **Files**: `admin_metrics.py:33`, `analytics.py:23`
- **Problem**: Admin check uses fallback email domain check `@fypglow.com`. No proper `is_admin` column or role system.
- **Fix**: Add `is_admin: bool` column to User model and proper role-based access control.

### MAJ-2: Business Logic in Routes (preferences.py)
- **File**: `app/routes/preferences.py`
- **Lines**: 48-62, 80-89
- **Problem**: Direct `db.session` operations in routes.
- **Fix**: Create `PreferencesService` with `get_preferences()`, `update_preferences()`, `complete_onboarding()`.

### MAJ-3: Business Logic in Routes (waitlist.py)
- **File**: `app/routes/waitlist.py`
- **Lines**: 39-75
- **Problem**: All CRUD operations directly in routes.
- **Fix**: Create `WaitlistService`.

### MAJ-4: Incomplete Type Hints in Services
- **Files**: Multiple services
- **Problem**: Some functions lack return type hints.
- **Example**: `auth_service.py`, `cache_service.py`
- **Fix**: Add comprehensive type hints to all public methods.

### MAJ-5: Rate Limiting Endpoint Missing
- **File**: Auth routes
- **Problem**: `/api/auth/me` endpoint returns 404 (mentioned in R1.2 tests).
- **Fix**: Implement `/api/auth/me` endpoint or update documentation.

### MAJ-6: Raw SQL in Routes
- **File**: `admin_metrics.py:295`
- **Problem**: Raw SQL `PERCENTILE_CONT` query in route.
- **Fix**: Move to service layer with parameterized query wrapper.

### MAJ-7: No Eager Loading
- **Files**: Multiple routes using `.all()`
- **Problem**: Potential N+1 queries in `categories.py:24`, `categories.py:53`.
- **Fix**: Add `joinedload()` or `selectinload()` where relationships are accessed.

### MAJ-8: Tests Coverage
- **Directory**: `backend/tests/`
- **Files**: 6 test files exist
- **Problem**: Limited integration test coverage for new features (analytics, admin metrics).
- **Fix**: Add tests for `admin_metrics.py`, `analytics_v2.py`, `plans_v2.py`.

---

## Minor Issues

### MIN-1: TODO Comments (4 found)
| Location | TODO |
|----------|------|
| `models/action.py:43` | `TODO: проверять в user_progress` |
| `routes/admin_metrics.py:33` | `TODO: Add proper admin role in users table` |
| `routes/analytics.py:23` | `TODO: Implement proper admin role check` |
| `services/curation_service.py:96` | `TODO: Add category-specific filtering` |

**Recommendation**: Create issues or implement.

### MIN-2: Missing Docstrings
- **Files**: Some route handlers lack docstrings.
- **Example**: `waitlist.py` functions.
- **Fix**: Add docstrings to all public endpoints.

### MIN-3: Hardcoded Default Category
- **File**: `app/config/constants.py:145`
- **Value**: `DEFAULT_CATEGORY_CODE: str = 'fitness'`
- **Note**: This is acceptable in config file, but should be documented.

### MIN-4: Inconsistent Error Codes
- **Files**: Various routes
- **Problem**: Mix of uppercase (`MISSING_CATEGORY_ID`) and lowercase (`unauthorized`) error codes.
- **Fix**: Standardize to lowercase snake_case.

### MIN-5: Missing Logging in Preferences
- **File**: `app/routes/preferences.py`
- **Problem**: No logging for preference updates.
- **Fix**: Add `logger.info()` for audit trail.

### MIN-6: No Bare Except (Good!)
- No `except:` bare statements found - all exceptions are typed.

### MIN-7: Duplicate Import in admin_metrics.py
- **Line**: 26-27
- **Problem**: `from app.models import User` then `user = User.query.get()` in function.
- **Fix**: Remove duplicate import inside function.

### MIN-8: Migration Naming
- **Files**: `migrations/versions/`
- **Problem**: Date prefix without consistent format (20251225 vs 20251227 vs 20251228).
- **Note**: Minor, migrations work correctly. Single head confirmed.

### MIN-9: Hardcoded Timeout
- **File**: `app/routes/oauth.py:76, 107`
- **Value**: `timeout=10`
- **Fix**: Move to config `OAuthConfig.REQUEST_TIMEOUT = 10`.

### MIN-10: Language Hardcoded
- **File**: `app/routes/oauth.py:141`
- **Value**: `language='en'`
- **Fix**: Use constant `DEFAULT_LANGUAGE = 'en'` from config.

### MIN-11: Logging Count Good
- **Routes**: 32 logging statements
- **Services**: 62 logging statements
- **Status**: Adequate logging coverage.

### MIN-12: Security Headers Present
- CORS, X-Frame-Options, X-Content-Type-Options verified in middleware.
- Rate limiting configured on all sensitive endpoints.

### MIN-13: PKCE OAuth Implemented
- **File**: `oauth.py`
- **Status**: Correctly implements PKCE with `code_verifier`.
- **Note**: SEC-001 redirect_uri validation present.

---

## Good Practices Found

1. **Proper Service Layer**: `plan_service_v2.py` is well-structured with clear separation.
2. **Type Hints**: Most services have type hints on key methods.
3. **Docstrings**: Services have good docstrings with Args/Returns.
4. **Error Handling**: Proper try/except with specific exceptions, no bare `except:`.
5. **Logging**: 94 logging statements across routes and services.
6. **Security**:
   - Redirect URI whitelist validation
   - PKCE implementation
   - Rate limiting on auth endpoints
   - Security headers configured
7. **Caching**: Redis caching properly implemented via `cache_service`.
8. **Migrations**: Single head, proper dependency chain.
9. **Singleton Pattern**: Services use singleton pattern correctly.
10. **Constants**: Category codes, limits moved to `config/constants.py`.

---

## Recommendations

### Priority 1 (Critical)
1. **Create AdminMetricsService** - Extract all queries from `admin_metrics.py` to service layer.
2. **Refactor OAuth Route** - Move user creation logic to `AuthService`.

### Priority 2 (Major)
3. **Add is_admin Column** - Implement proper admin role system.
4. **Create PreferencesService** - Extract DB operations from routes.
5. **Add Type Hints** - Complete type annotations across all services.
6. **Add Missing Tests** - Integration tests for new features.

### Priority 3 (Minor)
7. **Standardize Error Codes** - Use lowercase snake_case consistently.
8. **Add Missing Logging** - Audit logging for preference changes.
9. **Resolve TODOs** - Create issues or implement 4 TODO items.
10. **Move Timeouts to Config** - `REQUEST_TIMEOUT = 10`.

---

## Files Need Refactoring

| File | Reason | Priority |
|------|--------|----------|
| `routes/admin_metrics.py` | Heavy business logic in routes | Critical |
| `routes/oauth.py` | User creation logic in route | Critical |
| `routes/preferences.py` | DB operations in routes | Major |
| `routes/waitlist.py` | All CRUD in routes | Major |
| `services/auth_service.py` | Add oauth user management | Major |

---

## Architecture Compliance

| Principle | Status | Notes |
|-----------|--------|-------|
| Routes = thin controllers | Partial | admin_metrics, oauth need refactor |
| Services = business logic | Good | plan_service_v2 exemplary |
| Models = ORM only | Good | Clean models |
| Config separation | Good | constants.py, .env |
| Error handling | Good | No bare except |
| Logging | Good | 94 statements |
| Security | Good | PKCE, rate limiting, headers |
| Tests | Partial | Need more coverage |

---

## Metrics

- **Routes files**: 18
- **Services files**: 17
- **Models files**: 24
- **Test files**: 6
- **Migrations**: 7 (single head)
- **Lines of Python**: ~4,500 estimated
