import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Video } from '../types/plan.types';

interface UIState {
  theme: 'light' | 'dark';
  language: 'en' | 'ru' | 'es';
  isVideoModalOpen: boolean;
  currentVideo: Video | null;

  toggleTheme: () => void;
  setLanguage: (lang: 'en' | 'ru' | 'es') => void;
  openVideoModal: (video: Video) => void;
  closeVideoModal: () => void;
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      theme: 'dark',
      language: 'en',
      isVideoModalOpen: false,
      currentVideo: null,

      toggleTheme: () =>
        set((state) => ({
          theme: state.theme === 'dark' ? 'light' : 'dark',
        })),

      setLanguage: (lang) => set({ language: lang }),

      openVideoModal: (video) =>
        set({
          isVideoModalOpen: true,
          currentVideo: video,
        }),

      closeVideoModal: () =>
        set({
          isVideoModalOpen: false,
          currentVideo: null,
        }),
    }),
    {
      name: 'ui-storage',
      partialize: (state) => ({
        theme: state.theme,
        language: state.language,
      }),
    }
  )
);
