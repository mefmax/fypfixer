-- Add is_premium flag to categories

ALTER TABLE categories
ADD COLUMN is_premium BOOLEAN NOT NULL DEFAULT FALSE;
