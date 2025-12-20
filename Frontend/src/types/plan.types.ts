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
