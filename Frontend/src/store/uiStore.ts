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
