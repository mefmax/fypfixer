# FYPGlow Developer Handbook

## Quick Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- Git

### Local Development
```bash
# Clone repository
git clone https://github.com/mefmax/fypfixer.git
cd fypfixer

# Start backend services
docker-compose up -d

# Start frontend
cd Frontend
npm install
npm run dev
```
Open http://localhost:5173

### Environment Variables
Copy `.env.example` to `.env` and fill in:
- `JWT_SECRET_KEY` - Random 32+ char string
- `TIKTOK_CLIENT_KEY` - From TikTok Developer Portal
- `TIKTOK_CLIENT_SECRET` - From TikTok Developer Portal
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string

## Code Standards

### Backend (Python)

**Architecture**
- Routes = thin controllers (NO business logic!)
- Services = ALL business logic
- Models = SQLAlchemy ORM only

**Style**
```python
# Good: Type hints on all functions
def get_user_by_id(user_id: int) -> User | None:
    return User.query.get(user_id)

# Good: Use logger, not print
from app import logger
logger.info(f"User {user_id} logged in")

# Bad: Business logic in routes
@bp.route('/users/<int:id>')
def get_user(id):
    # Don't do complex logic here!
    pass
```

**Error Handling**
```python
from app.utils.errors import NotFoundError, ValidationError
from app.utils.responses import success_response, error_response

# Raise custom errors
if not user:
    raise NotFoundError("User not found")

# Return consistent responses
return success_response({"user": user.to_dict()})
```

### Frontend (TypeScript)

**Architecture**
- Components = pure UI, no API calls
- Pages = compose components, handle routing
- Stores = global state (Zustand)
- API = all HTTP calls

**Style**
```typescript
// Good: Proper types, no `any`
interface User {
  id: number;
  email: string;
}

// Good: Error handling with unknown
try {
  await api.login(data);
} catch (error: unknown) {
  const axiosError = error as { response?: { data?: { error?: { message?: string } } } };
  const message = axiosError.response?.data?.error?.message || 'Failed';
}

// Good: Use logger from lib/logger.ts
import { logger } from '../lib/logger';
logger.error('Failed to load:', error);

// Bad: console.log in production code
console.log('Debug:', data); // NO!
```

**Accessibility**
```tsx
// Good: Alt on all images
<img src={url} alt={title} />

// Good: ARIA on interactive elements
<button aria-label="Close menu" aria-expanded={isOpen}>

// Good: Keyboard navigation
onKeyDown={(e) => e.key === 'Enter' && handleClick()}
```

**Components**
```tsx
// Good: Functional components only
const UserCard: React.FC<{ user: User }> = ({ user }) => {
  return <div>{user.name}</div>;
};

// Good: Use ErrorBoundary
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

## Git Workflow

### Branch Strategy
- `main` - Production branch
- Feature branches: `feat/feature-name`
- Bugfix branches: `fix/bug-description`

### Commit Messages
```
feat: add user authentication
fix: resolve login redirect loop
refactor: extract business logic to services
docs: update API documentation
chore: update dependencies
test: add unit tests for auth service
```

### Pull Request Checklist
- [ ] TypeScript builds without errors
- [ ] No `any` types
- [ ] All images have `alt` attributes
- [ ] No `console.log` (use logger)
- [ ] Tests pass (when applicable)
- [ ] Code reviewed

## Testing

### Backend
```bash
cd backend
pytest tests/ -v
```

### Frontend
```bash
cd Frontend
npm run test
npm run lint
```

### Type Checking
```bash
cd Frontend
npx tsc --noEmit
```

## Debugging

### Backend Logs
```bash
docker-compose logs -f backend
```

### Database
```bash
docker-compose exec db psql -U postgres -d fypglow
```

### Redis
```bash
docker-compose exec redis redis-cli
```

## Common Issues

### TikTok OAuth Errors
- Check PKCE code_verifier matches between auth and callback
- Desktop apps need HEX encoding, web apps need Base64URL
- Verify redirect_uri matches TikTok app settings exactly

### Database Migrations
```bash
docker-compose exec backend flask db upgrade
```

### Clear Redis Cache
```bash
docker-compose exec redis redis-cli FLUSHALL
```
