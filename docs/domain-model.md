# FYPFixer – Domain Model (Draft)

## Core entities

- User  
  - Anonymous user identified by a generated `client_id` (stored in cookie or localStorage).  
  - Has language preference and optional preferred category/niche.  

- Plan  
  - A daily checklist for retraining the TikTok FYP.  
  - Belongs to a User (or is a generic template used by many users).  
  - Has a date, category, difficulty/level, and language.

- Step  
  - One actionable instruction inside a Plan (for example: “Like 10 videos in X niche”).  
  - Has an order (position inside the plan).  
  - Has text, optional type (watch / like / block / search) and optional tags.

- Category  
  - Logical topic like “IT”, “Fitness”, “Fashion”, etc.  
  - Used to route users to appropriate plans and to organize templates.
