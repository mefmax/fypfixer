// Тип действия в TikTok
export type ActionType = 'follow' | 'like' | 'save' | 'not_interested';

// Категория действия (для визуального разделения)
export type ActionCategory = 'positive' | 'negative';

// Цель действия
export interface ActionTarget {
  type: 'creator' | 'video' | 'content_type';
  name: string; // "@jayshetty" или "Танцевальные челленджи"
  description?: string; // "Мотивация, осознанность, привычки"
  thumbnailUrl?: string; // URL превью (для positive actions)
  tiktokUrl?: string; // Ссылка на TikTok (только для positive)
}

// Одно действие в плане
export interface PlanAction {
  id: string;
  type: ActionType;
  category: ActionCategory;
  target: ActionTarget;
  completed: boolean;
  completedAt?: string;
}

// Plan metadata from AI Pipeline
export interface PlanMetadata {
  source: 'ai' | 'seed' | 'cache';
  generatedAt: string;
  provider: string;
  generationTimeMs: number;
}

// Дневной план
export interface DailyActionPlan {
  id: string;
  date: string;
  categoryCode: string;
  categoryName: string;
  actions: PlanAction[];
  motivation?: string;          // AI-generated motivation message
  progress?: ActionProgress;    // Completion progress
  metadata?: PlanMetadata;      // AI pipeline info
}

// Прогресс
export interface ActionProgress {
  completed: number;
  total: number;
  percentage: number;
}

// Ответ API при завершении действия
export interface CompleteActionResponse {
  actionId: string;
  completed: boolean;
  completedAt: string;
  xpEarned?: number;      // XP earned for this action
  planCompleted?: boolean; // Whether entire plan is now complete
}
