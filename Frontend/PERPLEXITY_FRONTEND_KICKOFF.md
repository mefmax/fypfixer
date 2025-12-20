# PERPLEXITY AI — FRONTEND DEVELOPER KICKOFF

**Project:** FYPFixer MVP  
**Your Role:** Frontend Developer (React 18)  
**Timeline:** Day 1 (14 Dec 2025)  
**Duration:** 60 minutes total

---

## 🎯 YOUR MISSION TODAY

Set up React 18 frontend foundation with:
- Project structure (Vite + React)
- Component library (Must-Have features)
- API service (connect to Flask backend)
- Tailwind CSS (design tokens)

---

## ✅ TASK 1: PROJECT SETUP (15 min)

Create React project with Vite:

```bash
npm create vite@latest fypfixer-frontend -- --template react
cd fypfixer-frontend
npm install
npm install react-router-dom@6 zustand axios
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Test: `npm run dev` → should open localhost:5173

---

## ✅ TASK 2: TAILWIND CONFIG (5 min)

Update `tailwind.config.js`:

```javascript
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: '#208E9F',    // Teal
        cta: '#FF6B35',        // Hot Orange
        premium: '#A855F7',    // Purple
        success: '#10B981',    // Green
        warning: '#F59E0B',    // Yellow
        error: '#EF4444',      // Red
        dark: '#0F172A',       // Background
      },
    },
  },
  plugins: [],
}
```

Update `src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-dark text-white;
}
```

---

## ✅ TASK 3: FOLDER STRUCTURE (10 min)

Create this structure in `src/`:

```
src/
├── components/
│   ├── Plan/
│   │   ├── VideoCard.jsx
│   │   ├── ProgressTracker.jsx
│   │   └── DailyPlan.jsx
│   └── Common/
│       ├── Button.jsx
│       └── Loading.jsx
├── pages/
│   └── Dashboard.jsx
├── services/
│   └── api.js
├── store/
│   └── useStore.js
└── App.jsx
```

---

## ✅ TASK 4: CREATE COMPONENTS (20 min)

### VideoCard.jsx
```jsx
// src/components/Plan/VideoCard.jsx
export default function VideoCard({ video }) {
  return (
    <div className="bg-gray-900 border-t-4 border-primary rounded-xl p-4">
      <div className="relative w-full h-80 bg-gray-800 rounded-lg mb-3">
        <img src={video.thumbnail_url} alt={video.title} className="w-full h-full object-cover rounded-lg" />
        <div className="absolute bottom-3 right-3 bg-white rounded-full w-10 h-10 flex items-center justify-center">
          ▶
        </div>
      </div>
      <h3 className="text-white font-semibold mb-1">{video.title}</h3>
      <p className="text-gray-400 text-sm mb-2">{video.creator}</p>
      <button className="w-full bg-cta text-white font-semibold py-3 rounded-lg hover:opacity-90">
        Open in TikTok
      </button>
    </div>
  );
}
```

### ProgressTracker.jsx
```jsx
// src/components/Plan/ProgressTracker.jsx
export default function ProgressTracker({ completed, total }) {
  const percent = (completed / total) * 100;
  return (
    <div className="bg-gray-900 border border-primary/20 rounded-xl p-4 mb-6">
      <div className="flex justify-between mb-2">
        <span className="text-white font-semibold">Daily Progress</span>
        <span className="text-primary">{completed}/{total}</span>
      </div>
      <div className="w-full bg-gray-800 rounded-full h-2 mb-2">
        <div className="bg-primary h-2 rounded-full" style={{width: `${percent}%`}} />
      </div>
      <p className="text-warning text-sm text-center">
        {completed === 0 && "Let's start! 🎯"}
        {completed === 1 && "Great start! 💪"}
        {completed === 2 && "Almost there! 🔥"}
        {completed === 3 && "Day complete! ✨"}
      </p>
    </div>
  );
}
```

### DailyPlan.jsx
```jsx
// src/components/Plan/DailyPlan.jsx
import VideoCard from './VideoCard';
import ProgressTracker from './ProgressTracker';

export default function DailyPlan({ plan }) {
  return (
    <div className="max-w-6xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-2">Today's Plan: {plan.category_name}</h2>
      <p className="text-gray-400 mb-6">Watch → Like → Follow. Your FYP learns in 10 minutes.</p>
      <ProgressTracker completed={1} total={3} />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {plan.videos?.map((video, i) => <VideoCard key={i} video={video} />)}
      </div>
    </div>
  );
}
```

---

## ✅ TASK 5: API SERVICE (10 min)

```javascript
// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {'Content-Type': 'application/json'},
});

export const getPlan = async (category = 'personal_growth', lang = 'en') => {
  const { data } = await api.get(`/api/plan?category=${category}&lang=${lang}`);
  return data;
};

export default api;
```

---

## ✅ DELIVERABLES (what to show me)

1. Screenshot: npm run dev running
2. Screenshot: VideoCard component rendered
3. Screenshot: ProgressTracker component rendered
4. Confirmation: API service created (show code)

Total time: ~60 minutes

---

## 🚨 IF YOU GET STUCK

- Tailwind not working? Check `tailwind.config.js` content array
- Component won't render? Check import paths
- Port 5173 busy? Run on different port: `npm run dev -- --port 5174`

---

Ready? Let's build! 🚀
