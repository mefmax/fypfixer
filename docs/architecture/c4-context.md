# FYPFixer – System Context (C4 Level 1)

FYPFixer is a web and API service that generates daily checklists to help users retrain their TikTok For You Page (FYP) toward desired topics.

## Primary actors

- TikTok User  
  - A creator or regular user who wants to clean and retrain their TikTok FYP.  
  - Uses FYPFixer via the web UI on mobile or desktop.

- Premium User  
  - Same as TikTok User, but pays for advanced, AI-powered and more personalized plans.  

- Admin  
  - Product owner / operator who monitors analytics and manages configurations.

## External systems (present and future)

- TikTok  
  - Short-video platform and source of trends (potential future scraping or third-party APIs).

- OpenAI API  
  - Optional external LLM provider for premium or fallback AI generation.

- Email Service  
  - Service for sending onboarding and reminder emails (future).

- Payment Provider  
  - Stripe or similar provider used for handling premium billing (future).

## Relationships

- TikTok User → FYPFixer: requests daily plans through the web UI.  
- Premium User → FYPFixer: requests more advanced and personalized plans via the same UI or API.  
- Admin → FYPFixer: views dashboards and adjusts configurations.  

- FYPFixer → TikTok: may read public trends via scraping or APIs in the future.  
- FYPFixer → OpenAI API: may call external LLM for completions as an optional provider.  
- FYPFixer → Email Service: may send notification and reminder emails in the future.  
- FYPFixer → Payment Provider: may handle subscription and premium payments in the future.