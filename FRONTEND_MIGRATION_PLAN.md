# 🟢 FYPFixer — ПЛАН МИГРАЦИИ FRONTEND

**Для:** Claude Code (Frontend Sonnet) в VS Code  
**Репозиторий:** mefmax/fypfixer  
**Время:** ~4 часа

---

## 📋 ОБЗОР ЗАДАЧИ

Создать React SPA в папке `frontend/` согласно спецификации из `docs/03_FRONTEND_ARCHITECTURE.md`.

**Важно:**
- Использовать **Vite + React + TypeScript** (НЕ Next.js!)
- НЕ использовать код из `v0-designs/` — он на Next.js
- API будет на `http://localhost:8000/api`
- Читать целевую архитектуру в `docs/03_FRONTEND_ARCHITECTURE.md`

---

## Фаза F1: Инициализация проекта (30 мин)

### 1.1 Создать Vite проект

```bash
cd fypfixer
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
```

### 1.2 Установить зависимости

```bash
# Routing + State + Data Fetching
npm install react-router-dom@6 zustand @tanstack/react-query axios

# Forms + Validation
npm install react-hook-form zod @hookform/resolvers

# Utilities
npm install clsx

# Tailwind CSS
npm install -D tailwindcss postcss autoprefixer @types/node
npx tailwindcss init -p
```

---

## Фаза F2: Настройка Tailwind (15 мин)

### 2.1 `frontend/tailwind.config.js`

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#FF2D55',
          dark: '#cc2445',
          light: '#ff5a7a',
        },
        secondary: {
          DEFAULT: '#FF9F0A',
          dark: '#cc7f08',
        },
        background: {
          DEFAULT: '#0a0e27',
          secondary: '#1a1f3a',
          tertiary: '#252b4a',
        },
        surface: {
          DEFAULT: 'rgba(255, 255, 255, 0.04)',
          hover: 'rgba(255, 255, 255, 0.08)',
        },
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

### 2.2 `frontend/src/styles/globals.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  @apply bg-background text-gray-200 antialiased;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1a2e 100%);
  min-height: 100vh;
  line-height: 1.6;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Focus styles */
*:focus-visible {
  @apply outline-none ring-2 ring-primary ring-offset-2 ring-offset-background;
}
```

### 2.3 Обновить `frontend/src/index.css`

```css
@import './styles/globals.css';
```

---

## Фаза F3: Структура папок (20 мин)

### 3.1 Создать структуру

```bash
cd frontend/src

# API layer
mkdir -p api

# Components
mkdir -p components/common
mkdir -p components/layout
mkdir -p components/auth
mkdir -p components/video
mkdir -p components/plan

# Pages
mkdir -p pages/auth
mkdir -p pages/dashboard

# State management
mkdir -p store

# Hooks
mkdir -p hooks

# Utilities
mkdir -p lib

# Types
mkdir -p types

# Styles
mkdir -p styles
```

### Итоговая структура:

```
frontend/src/
├── api/
│   ├── auth.api.ts
│   └── plans.api.ts
├── components/
│   ├── common/
│   │   ├── Button.tsx
│   │   └── Input.tsx
│   ├── layout/
│   │   └── Header.tsx
│   ├── auth/
│   ├── video/
│   │   ├── VideoCard.tsx
│   │   └── VideoModal.tsx
│   └── plan/
│       └── ProgressTracker.tsx
├── pages/
│   ├── auth/
│   │   ├── LoginPage.tsx
│   │   └── RegisterPage.tsx
│   └── dashboard/
│       └── DashboardPage.tsx
├── store/
│   ├── authStore.ts
│   └── uiStore.ts
├── hooks/
├── lib/
│   └── axios.ts
├── types/
│   ├── auth.types.ts
│   ├── plan.types.ts
│   └── api.types.ts
├── styles/
│   └── globals.css
├── App.tsx
└── main.tsx
```

---

## Фаза F4: TypeScript Types (20 мин)

### 4.1 `frontend/src/types/auth.types.ts`

```typescript
export interface User {
  id: number;
  client_id: string;
  email: string | null;
  language: string;
  is_premium: boolean;
  created_at: string | null;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  language?: string;
}

export interface AuthResponse {
  success: boolean;
  data: {
    user: User;
    token: string;
    refresh_token: string;
  };
}
```

### 4.2 `frontend/src/types/plan.types.ts`

```typescript
export interface Category {
  id: number;
  code: string;
  name: string;
  icon?: string;
  is_premium: boolean;
}

export interface StepItem {
  id: number;
  video_id: string;
  creator_username: string;
  title: string;
  thumbnail_url: string;
  video_url: string;
  engagement_score?: number;
  reason_text?: string;
}

export interface PlanStep {
  id: number;
  step_order: number;
  action_type: string;
  text: string;
  duration_minutes: number;
  items: StepItem[];
}

export interface Plan {
  id: number;
  title: string;
  plan_date: string;
  language: string;
  category: Category;
  steps: PlanStep[];
}

export interface PlanListResponse {
  plans: Plan[];
  pagination: {
    total: number;
    limit: number;
    offset: number;
  };
}
```

### 4.3 `frontend/src/types/api.types.ts`

```typescript
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface ApiError {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, string>;
  };
}
```

---

## Фаза F5: API Layer (30 мин)

### 5.1 `frontend/src/lib/axios.ts`

```typescript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor - добавляем токен
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - обработка ошибок
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Если 401 и это не повторный запрос
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // Пробуем refresh token
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const { token } = response.data.data;
          localStorage.setItem('access_token', token);

          originalRequest.headers.Authorization = `Bearer ${token}`;
          return apiClient(originalRequest);
        } catch {
          // Refresh failed - logout
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/auth/login';
        }
      } else {
        // No refresh token - logout
        localStorage.removeItem('access_token');
        window.location.href = '/auth/login';
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
```

### 5.2 `frontend/src/api/auth.api.ts`

```typescript
import apiClient from '../lib/axios';
import type { LoginRequest, RegisterRequest, AuthResponse } from '../types/auth.types';

export const authApi = {
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/auth/login', data);
    return response.data;
  },

  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/auth/register', data);
    return response.data;
  },

  logout: async (): Promise<void> => {
    await apiClient.post('/auth/logout');
  },

  getProfile: async () => {
    const response = await apiClient.get('/user');
    return response.data;
  },
};
```

### 5.3 `frontend/src/api/plans.api.ts`

```typescript
import apiClient from '../lib/axios';
import type { Plan, Category } from '../types/plan.types';
import type { ApiResponse } from '../types/api.types';

export const plansApi = {
  getDailyPlan: async (category: string, lang = 'en'): Promise<ApiResponse<Plan>> => {
    const response = await apiClient.get<ApiResponse<Plan>>('/plan', {
      params: { category, lang },
    });
    return response.data;
  },

  getPlans: async (params?: { category?: string; language?: string; limit?: number; offset?: number }) => {
    const response = await apiClient.get('/plans', { params });
    return response.data;
  },

  completeStep: async (planId: number, stepId: number): Promise<ApiResponse<{ step_id: number; completed: boolean }>> => {
    const response = await apiClient.post(`/plans/${planId}/steps/${stepId}/complete`);
    return response.data;
  },

  getCategories: async (language = 'en'): Promise<ApiResponse<{ categories: Category[] }>> => {
    const response = await apiClient.get('/categories', {
      params: { language },
    });
    return response.data;
  },
};
```

---

## Фаза F6: Zustand Stores (30 мин)

### 6.1 `frontend/src/store/authStore.ts`

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '../types/auth.types';
import { authApi } from '../api/auth.api';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, language?: string) => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
  setUser: (user: User | null) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email, password) => {
        set({ isLoading: true, error: null });
        try {
          const response = await authApi.login({ email, password });
          
          localStorage.setItem('access_token', response.data.token);
          localStorage.setItem('refresh_token', response.data.refresh_token);
          
          set({
            user: response.data.user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error: any) {
          const message = error.response?.data?.error?.message || 'Login failed';
          set({ error: message, isLoading: false });
          throw new Error(message);
        }
      },

      register: async (email, password, language = 'en') => {
        set({ isLoading: true, error: null });
        try {
          const response = await authApi.register({ email, password, language });
          
          localStorage.setItem('access_token', response.data.token);
          localStorage.setItem('refresh_token', response.data.refresh_token);
          
          set({
            user: response.data.user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error: any) {
          const message = error.response?.data?.error?.message || 'Registration failed';
          set({ error: message, isLoading: false });
          throw new Error(message);
        }
      },

      logout: async () => {
        try {
          await authApi.logout();
        } catch {
          // Ignore logout errors
        }
        
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        
        set({
          user: null,
          isAuthenticated: false,
        });
      },

      clearError: () => set({ error: null }),
      
      setUser: (user) => set({ user, isAuthenticated: !!user }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
```

### 6.2 `frontend/src/store/uiStore.ts`

```typescript
import { create } from 'zustand';
import type { StepItem } from '../types/plan.types';

interface UIState {
  // Video Modal
  isVideoModalOpen: boolean;
  currentVideo: StepItem | null;
  
  // Theme
  isDarkMode: boolean;
  
  // Language
  language: string;
  
  // Loading states
  isGlobalLoading: boolean;

  // Actions
  openVideoModal: (video: StepItem) => void;
  closeVideoModal: () => void;
  toggleDarkMode: () => void;
  setLanguage: (lang: string) => void;
  setGlobalLoading: (loading: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  isVideoModalOpen: false,
  currentVideo: null,
  isDarkMode: true,
  language: 'en',
  isGlobalLoading: false,

  openVideoModal: (video) => set({ 
    isVideoModalOpen: true, 
    currentVideo: video 
  }),
  
  closeVideoModal: () => set({ 
    isVideoModalOpen: false, 
    currentVideo: null 
  }),
  
  toggleDarkMode: () => set((state) => ({ 
    isDarkMode: !state.isDarkMode 
  })),
  
  setLanguage: (language) => set({ language }),
  
  setGlobalLoading: (isGlobalLoading) => set({ isGlobalLoading }),
}));
```

---

## Фаза F7: UI Компоненты (45 мин)

### 7.1 `frontend/src/components/common/Button.tsx`

```tsx
import React from 'react';
import { clsx } from 'clsx';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  fullWidth?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  fullWidth = false,
  className,
  disabled,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {
    primary: 'bg-gradient-to-r from-primary to-secondary text-white hover:opacity-90 shadow-lg shadow-primary/25',
    secondary: 'bg-white/10 text-white border border-white/20 hover:bg-white/20',
    outline: 'bg-transparent text-primary border-2 border-primary hover:bg-primary hover:text-white',
    ghost: 'bg-transparent text-gray-300 hover:bg-white/10',
  };
  
  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
  };

  return (
    <button
      className={clsx(
        baseStyles,
        variants[variant],
        sizes[size],
        fullWidth && 'w-full',
        className
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <>
          <svg
            className="animate-spin -ml-1 mr-2 h-4 w-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
          Loading...
        </>
      ) : (
        children
      )}
    </button>
  );
};
```

### 7.2 `frontend/src/components/common/Input.tsx`

```tsx
import React, { forwardRef } from 'react';
import { clsx } from 'clsx';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, className, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-gray-300 mb-2">
            {label}
          </label>
        )}
        <input
          ref={ref}
          className={clsx(
            'w-full px-4 py-3 rounded-xl',
            'bg-white/5 border border-white/10',
            'text-white placeholder-gray-500',
            'focus:outline-none focus:border-primary focus:bg-white/10',
            'transition-all duration-200',
            error && 'border-red-500 focus:border-red-500',
            className
          )}
          {...props}
        />
        {error && (
          <p className="mt-2 text-sm text-red-500">{error}</p>
        )}
        {helperText && !error && (
          <p className="mt-2 text-sm text-gray-500">{helperText}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
```

### 7.3 `frontend/src/components/video/VideoCard.tsx`

```tsx
import React from 'react';
import type { StepItem } from '../../types/plan.types';
import { useUIStore } from '../../store/uiStore';

interface VideoCardProps {
  video: StepItem;
  isCompleted?: boolean;
  onComplete?: () => void;
}

export const VideoCard: React.FC<VideoCardProps> = ({ 
  video, 
  isCompleted = false,
  onComplete 
}) => {
  const { openVideoModal } = useUIStore();

  const handleClick = () => {
    openVideoModal(video);
  };

  return (
    <div
      onClick={handleClick}
      className={clsx(
        'relative rounded-xl overflow-hidden cursor-pointer',
        'bg-gradient-to-br from-primary/30 to-background',
        'border border-primary/40 hover:border-primary/60',
        'transition-all duration-300 hover:scale-[1.02] hover:shadow-xl hover:shadow-primary/20',
        isCompleted && 'opacity-60'
      )}
    >
      {/* Thumbnail */}
      <div className="relative aspect-[9/16]">
        <img
          src={video.thumbnail_url || '/placeholder-video.jpg'}
          alt={video.title}
          className="w-full h-full object-cover"
        />
        
        {/* Play overlay */}
        <div className="absolute inset-0 flex items-center justify-center bg-black/20">
          <div className="w-14 h-14 rounded-full bg-black/70 flex items-center justify-center backdrop-blur-sm">
            <span className="text-white text-xl ml-1">▶</span>
          </div>
        </div>

        {/* Completed badge */}
        {isCompleted && (
          <div className="absolute top-3 left-3 px-2 py-1 bg-green-500/90 rounded-full">
            <span className="text-xs text-white font-medium">✓ Watched</span>
          </div>
        )}

        {/* Checkbox */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            onComplete?.();
          }}
          className={clsx(
            'absolute top-3 right-3 w-6 h-6 rounded-md border-2',
            'flex items-center justify-center transition-all',
            isCompleted 
              ? 'bg-green-500 border-green-500 text-white' 
              : 'border-white/50 bg-black/30 hover:border-white'
          )}
        >
          {isCompleted && '✓'}
        </button>
      </div>

      {/* Meta */}
      <div className="p-4 bg-black/40">
        <h4 className="text-sm font-semibold text-white line-clamp-2 mb-1">
          {video.title}
        </h4>
        <p className="text-xs text-gray-400">
          {video.creator_username}
        </p>
        {video.reason_text && (
          <p className="text-xs text-gray-500 mt-2 line-clamp-2 italic">
            {video.reason_text}
          </p>
        )}
      </div>
    </div>
  );
};

// Добавляем clsx для использования в компоненте
import { clsx } from 'clsx';
```

### 7.4 `frontend/src/components/video/VideoModal.tsx`

```tsx
import React, { useEffect } from 'react';
import { useUIStore } from '../../store/uiStore';

export const VideoModal: React.FC = () => {
  const { isVideoModalOpen, currentVideo, closeVideoModal } = useUIStore();

  // Close on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') closeVideoModal();
    };

    if (isVideoModalOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isVideoModalOpen, closeVideoModal]);

  if (!isVideoModalOpen || !currentVideo) return null;

  const handleOpenInTikTok = () => {
    window.open(currentVideo.video_url, '_blank');
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm"
      onClick={closeVideoModal}
    >
      <div
        className="relative w-full max-w-md h-[90vh] max-h-[800px] bg-black rounded-xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close button */}
        <button
          className="absolute top-4 right-4 z-10 w-10 h-10 rounded-full bg-black/70 text-white flex items-center justify-center hover:bg-black/90 transition-colors"
          onClick={closeVideoModal}
        >
          ✕
        </button>

        {/* Video embed placeholder */}
        <div className="w-full h-full flex flex-col">
          {/* TikTok Embed */}
          <div className="flex-1 bg-gray-900 flex items-center justify-center">
            <iframe
              src={`https://www.tiktok.com/embed/v2/${currentVideo.video_id}`}
              className="w-full h-full border-none"
              allowFullScreen
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            />
          </div>

          {/* Bottom actions */}
          <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/90 to-transparent">
            <div className="mb-3">
              <h3 className="text-white font-semibold line-clamp-1">
                {currentVideo.title}
              </h3>
              <p className="text-gray-400 text-sm">
                {currentVideo.creator_username}
              </p>
            </div>
            
            <button
              onClick={handleOpenInTikTok}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-primary to-secondary text-white font-semibold hover:opacity-90 transition-opacity"
            >
              🎬 Open in TikTok
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
```

### 7.5 `frontend/src/components/plan/ProgressTracker.tsx`

```tsx
import React from 'react';
import { clsx } from 'clsx';

interface ProgressTrackerProps {
  total: number;
  completed: number;
}

export const ProgressTracker: React.FC<ProgressTrackerProps> = ({ total, completed }) => {
  const percentage = total > 0 ? (completed / total) * 100 : 0;

  return (
    <div className="bg-white/5 border border-primary/20 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-white">Daily Progress</h3>
        <span className="text-xs text-gray-400">
          {completed}/{total} completed
        </span>
      </div>

      {/* Checkboxes */}
      <div className="flex gap-2 mb-3">
        {Array.from({ length: total }).map((_, i) => (
          <div
            key={i}
            className={clsx(
              'w-6 h-6 rounded-md border-2 flex items-center justify-center transition-all',
              i < completed
                ? 'bg-green-500 border-green-500 text-white'
                : 'border-gray-600 bg-transparent'
            )}
          >
            {i < completed && '✓'}
          </div>
        ))}
      </div>

      {/* Progress bar */}
      <div className="h-2 bg-white/10 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-primary to-green-500 rounded-full transition-all duration-500"
          style={{ width: `${percentage}%` }}
        />
      </div>

      {/* Motivation text */}
      <p className="text-xs text-gray-500 mt-3">
        {completed === 0 && "Ready to start? Let's go! 💪"}
        {completed > 0 && completed < total && "Great progress! Keep going! 🔥"}
        {completed === total && "Amazing! Day complete! 🎉"}
      </p>
    </div>
  );
};
```

### 7.6 `frontend/src/components/layout/Header.tsx`

```tsx
import React from 'react';
import { useAuthStore } from '../../store/authStore';
import { Button } from '../common/Button';

export const Header: React.FC = () => {
  const { user, logout } = useAuthStore();

  return (
    <header className="sticky top-0 z-40 bg-background/80 backdrop-blur-lg border-b border-white/10">
      <div className="max-w-md mx-auto px-4 py-3 flex items-center justify-between">
        <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
          FYPFixer
        </h1>
        
        <div className="flex items-center gap-3">
          {user?.email && (
            <span className="text-xs text-gray-400 hidden sm:block">
              {user.email}
            </span>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={logout}
          >
            Logout
          </Button>
        </div>
      </div>
    </header>
  );
};
```

---

## Фаза F8: Routing и App (20 мин)

### 8.1 `frontend/src/App.tsx`

```tsx
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuthStore } from './store/authStore';
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';
import { DashboardPage } from './pages/dashboard/DashboardPage';
import { VideoModal } from './components/video/VideoModal';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
    },
  },
});

// Protected Route wrapper
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore();
  
  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }
  
  return <>{children}</>;
};

// Public Route wrapper (redirect to dashboard if authenticated)
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore();
  
  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  
  return <>{children}</>;
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route
            path="/auth/login"
            element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            }
          />
          <Route
            path="/auth/register"
            element={
              <PublicRoute>
                <RegisterPage />
              </PublicRoute>
            }
          />

          {/* Protected routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />

          {/* Catch all - redirect to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>

        {/* Global components */}
        <VideoModal />
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
```

---

## Фаза F9: Страницы (45 мин)

### 9.1 `frontend/src/pages/auth/LoginPage.tsx`

```tsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useAuthStore } from '../../store/authStore';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, isLoading } = useAuthStore();
  const [error, setError] = useState<string>('');

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    setError('');
    try {
      await login(data.email, data.password);
      navigate('/');
    } catch (err: any) {
      setError(err.message || 'Login failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            FYPFixer
          </h1>
          <p className="text-gray-400 mt-2">Welcome back! Log in to continue.</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {error && (
            <div className="p-4 rounded-xl bg-red-500/20 border border-red-500/50 text-red-400 text-sm">
              {error}
            </div>
          )}

          <Input
            label="Email"
            type="email"
            placeholder="you@example.com"
            error={errors.email?.message}
            {...register('email')}
          />

          <Input
            label="Password"
            type="password"
            placeholder="••••••••"
            error={errors.password?.message}
            {...register('password')}
          />

          <Button
            type="submit"
            fullWidth
            isLoading={isLoading}
          >
            Log In
          </Button>
        </form>

        {/* Footer */}
        <p className="text-center mt-6 text-gray-400">
          Don't have an account?{' '}
          <Link
            to="/auth/register"
            className="text-primary hover:text-primary-light transition-colors"
          >
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
};
```

### 9.2 `frontend/src/pages/auth/RegisterPage.tsx`

```tsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useAuthStore } from '../../store/authStore';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const registerSchema = z.object({
  email: z.string().email('Please enter a valid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type RegisterFormData = z.infer<typeof registerSchema>;

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { register: registerUser, isLoading } = useAuthStore();
  const [error, setError] = useState<string>('');

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    setError('');
    try {
      await registerUser(data.email, data.password);
      navigate('/');
    } catch (err: any) {
      setError(err.message || 'Registration failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            FYPFixer
          </h1>
          <p className="text-gray-400 mt-2">Create your account to get started.</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {error && (
            <div className="p-4 rounded-xl bg-red-500/20 border border-red-500/50 text-red-400 text-sm">
              {error}
            </div>
          )}

          <Input
            label="Email"
            type="email"
            placeholder="you@example.com"
            error={errors.email?.message}
            {...register('email')}
          />

          <Input
            label="Password"
            type="password"
            placeholder="Min 8 characters"
            error={errors.password?.message}
            {...register('password')}
          />

          <Input
            label="Confirm Password"
            type="password"
            placeholder="Repeat your password"
            error={errors.confirmPassword?.message}
            {...register('confirmPassword')}
          />

          <Button
            type="submit"
            fullWidth
            isLoading={isLoading}
          >
            Create Account
          </Button>
        </form>

        {/* Footer */}
        <p className="text-center mt-6 text-gray-400">
          Already have an account?{' '}
          <Link
            to="/auth/login"
            className="text-primary hover:text-primary-light transition-colors"
          >
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
};
```

### 9.3 `frontend/src/pages/dashboard/DashboardPage.tsx`

```tsx
import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { plansApi } from '../../api/plans.api';
import { useAuthStore } from '../../store/authStore';
import { Header } from '../../components/layout/Header';
import { VideoCard } from '../../components/video/VideoCard';
import { ProgressTracker } from '../../components/plan/ProgressTracker';

export const DashboardPage: React.FC = () => {
  const { user } = useAuthStore();
  const queryClient = useQueryClient();
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());

  // Fetch daily plan
  const { data, isLoading, error } = useQuery({
    queryKey: ['dailyPlan', 'personal_growth', user?.language || 'en'],
    queryFn: () => plansApi.getDailyPlan('personal_growth', user?.language || 'en'),
  });

  // Complete step mutation
  const completeMutation = useMutation({
    mutationFn: ({ planId, stepId }: { planId: number; stepId: number }) =>
      plansApi.completeStep(planId, stepId),
    onSuccess: (_, variables) => {
      setCompletedSteps((prev) => new Set([...prev, variables.stepId]));
    },
  });

  const plan = data?.data;
  const totalVideos = plan?.steps.reduce((acc, step) => acc + step.items.length, 0) || 0;

  const handleCompleteVideo = (planId: number, stepId: number) => {
    if (!completedSteps.has(stepId)) {
      completeMutation.mutate({ planId, stepId });
    }
  };

  return (
    <div className="min-h-screen pb-20">
      <Header />

      <main className="max-w-md mx-auto px-4 py-6 space-y-6">
        {/* Hero section */}
        <div>
          <h2 className="text-2xl font-bold text-white">
            Your 10-Minute FYP Plan
          </h2>
          <p className="text-gray-400 mt-1">
            {totalVideos} videos curated for Personal Growth today
          </p>
          <p className="text-xs text-gray-500 mt-1 italic">
            Not 40 minutes of scrolling — just what matters
          </p>
        </div>

        {/* Anti-pattern card */}
        <div className="bg-primary/10 border border-primary/30 rounded-xl p-4">
          <div className="flex gap-6">
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <span className="text-red-500">❌</span>
                <span className="text-sm font-semibold text-red-400">TikTok</span>
              </div>
              <p className="text-xs text-gray-400 mt-1">40 min/day</p>
              <p className="text-xs text-gray-500 line-through">for 10 min of value</p>
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <span className="text-green-500">✅</span>
                <span className="text-sm font-semibold text-green-400">FYPFixer</span>
              </div>
              <p className="text-xs text-gray-400 mt-1">10 min/day</p>
              <p className="text-xs text-green-400">= 3.5h saved/week</p>
            </div>
          </div>
        </div>

        {/* Progress tracker */}
        <ProgressTracker total={totalVideos} completed={completedSteps.size} />

        {/* Loading state */}
        {isLoading && (
          <div className="flex justify-center py-12">
            <div className="animate-spin w-10 h-10 border-4 border-primary border-t-transparent rounded-full" />
          </div>
        )}

        {/* Error state */}
        {error && (
          <div className="p-4 rounded-xl bg-red-500/20 border border-red-500/50 text-red-400 text-center">
            Failed to load plan. Please try again.
          </div>
        )}

        {/* Plan steps */}
        {plan?.steps.map((step) => (
          <div key={step.id} className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-primary to-secondary flex items-center justify-center text-white text-sm font-bold">
                {step.step_order}
              </div>
              <h3 className="text-lg font-semibold text-white">{step.text}</h3>
            </div>

            <div className="grid gap-4">
              {step.items.map((video) => (
                <VideoCard
                  key={video.id}
                  video={video}
                  isCompleted={completedSteps.has(video.id)}
                  onComplete={() => handleCompleteVideo(plan.id, video.id)}
                />
              ))}
            </div>
          </div>
        ))}
      </main>
    </div>
  );
};
```

---

## Фаза F10: Финализация (10 мин)

### 10.1 `frontend/src/main.tsx`

```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### 10.2 `frontend/.env.example`

```bash
VITE_API_URL=http://localhost:8000/api
```

### 10.3 `frontend/Dockerfile`

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 10.4 `frontend/nginx.conf`

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # SPA routing - all routes to index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy to backend
    location /api {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

---

## ✅ ЧЕК-ЛИСТ FRONTEND

### Фаза F1: Инициализация
- [ ] Создать Vite проект с React + TypeScript
- [ ] Установить react-router-dom, zustand, @tanstack/react-query, axios
- [ ] Установить react-hook-form, zod, @hookform/resolvers
- [ ] Установить и настроить Tailwind CSS

### Фаза F2: Tailwind
- [ ] Настроить `tailwind.config.js` с кастомными цветами
- [ ] Создать `src/styles/globals.css`

### Фаза F3: Структура
- [ ] Создать папки: `api`, `components/*`, `pages/*`, `store`, `hooks`, `lib`, `types`

### Фаза F4: Types
- [ ] Создать `src/types/auth.types.ts`
- [ ] Создать `src/types/plan.types.ts`
- [ ] Создать `src/types/api.types.ts`

### Фаза F5: API Layer
- [ ] Создать `src/lib/axios.ts`
- [ ] Создать `src/api/auth.api.ts`
- [ ] Создать `src/api/plans.api.ts`

### Фаза F6: Stores
- [ ] Создать `src/store/authStore.ts`
- [ ] Создать `src/store/uiStore.ts`

### Фаза F7: Компоненты
- [ ] Создать `src/components/common/Button.tsx`
- [ ] Создать `src/components/common/Input.tsx`
- [ ] Создать `src/components/video/VideoCard.tsx`
- [ ] Создать `src/components/video/VideoModal.tsx`
- [ ] Создать `src/components/plan/ProgressTracker.tsx`
- [ ] Создать `src/components/layout/Header.tsx`

### Фаза F8: Routing
- [ ] Обновить `src/App.tsx` с роутами и ProtectedRoute

### Фаза F9: Страницы
- [ ] Создать `src/pages/auth/LoginPage.tsx`
- [ ] Создать `src/pages/auth/RegisterPage.tsx`
- [ ] Создать `src/pages/dashboard/DashboardPage.tsx`

### Фаза F10: Финализация
- [ ] Обновить `src/main.tsx`
- [ ] Создать `.env.example`
- [ ] Создать `Dockerfile`
- [ ] Создать `nginx.conf`

### Проверка
- [ ] `npm run dev` запускается без ошибок
- [ ] Открыть `http://localhost:5173` — видна страница Login
- [ ] Форма логина валидирует данные
- [ ] После входа (с работающим backend) — переход на Dashboard

---

## ⚠️ ВАЖНЫЕ ЗАМЕЧАНИЯ

1. **НЕ использовать** код из `v0-designs/` — он на Next.js, несовместим
2. **Использовать** Vite + React (НЕ Next.js!)
3. **API_URL** настроить через `.env` файл: `VITE_API_URL=http://localhost:8000/api`
4. **Tailwind** цвета взять из плана (primary: #FF2D55, secondary: #FF9F0A)
5. **Тестировать** каждую фазу перед переходом к следующей
6. **Коммитить** после каждой фазы

---

## 🔗 СВЯЗЬ С BACKEND

Frontend ожидает следующие эндпоинты от Backend:

| Эндпоинт | Метод | Описание |
|----------|-------|----------|
| `/api/auth/register` | POST | Регистрация |
| `/api/auth/login` | POST | Вход |
| `/api/auth/logout` | POST | Выход |
| `/api/plan` | GET | Получить дневной план |
| `/api/categories` | GET | Получить категории |
| `/api/plans/:id/steps/:id/complete` | POST | Отметить шаг выполненным |

---

**Общее время: ~4 часа**
