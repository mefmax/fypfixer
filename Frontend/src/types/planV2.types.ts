/**
 * Plan V2 Types - New plan structure with Clear/Watch/Reinforce steps
 */

export interface ToxicCreator {
  creator_id: string;
  creator_name: string;
  view_count: number;
  completion_rate: number;
  reason: string;
}

export interface CuratedVideo {
  video_id: string;
  video_url: string;
  thumbnail_url: string | null;
  creator_name: string;
  creator_display_name?: string;
  duration_seconds: number;
  quality_score: number | null;
  description?: string;
  views?: number;
  likes?: number;
}

export interface FavoriteVideo {
  video_id: string;
  video_url: string | null;
  thumbnail_url: string | null;
  creator_name: string | null;
  creator_display_name?: string;
  duration_seconds?: number;
  description?: string;
  liked_at: string | null;
}

export interface ClearStep {
  type: 'CLEAR';
  title: string;
  description: string;
  toxic_creators: ToxicCreator[];
  completed: boolean;
}

export interface WatchStep {
  type: 'WATCH';
  title: string;
  description: string;
  videos: CuratedVideo[];
  completed: boolean;
}

export interface ReinforceStep {
  type: 'REINFORCE';
  title: string;
  description: string;
  favorite_video: FavoriteVideo | null;
  show_share: boolean;
  completed: boolean;
}

export interface PlanV2Steps {
  clear: ClearStep;
  watch: WatchStep;
  reinforce: ReinforceStep;
}

export interface PlanV2 {
  plan_id: string;
  db_id?: number;
  user_id: number;
  category_id: number;
  day_of_challenge: number;
  created_at: string;
  steps: PlanV2Steps;
  target_signals: number;
}

export type StepType = 'clear' | 'watch' | 'reinforce' | 'complete';

export type SignalType = 'blocks' | 'watchesFull' | 'likes' | 'follows' | 'shares';

export interface SignalsState {
  blocks: number;
  watchesFull: number;
  likes: number;
  follows: number;
  shares: number;
}

export interface StepsCompleted {
  clear: boolean;
  watch: boolean;
  reinforce: boolean;
}
