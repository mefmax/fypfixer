export interface Video {
  id: string;
  video_id: string;
  creator_username: string;
  title: string;
  thumbnail_url: string;
  video_url: string;
  engagement_score?: number;
  reason_text?: string;
}

export interface PlanStep {
  id: string;
  step_order: number;
  action_type: string;
  text_en: string;
  videos?: Video[];
}

export interface Plan {
  id: string;
  title: string;
  description?: string;
  category: string;
  plan_date: string;
  steps: PlanStep[];
}

export interface Category {
  id: string;
  code: string;
  name_en: string;
  icon?: string;
  is_premium: boolean;
}
