-- Migration script to change user_id from INTEGER to UUID

-- Drop existing user_id columns (safe since they are NULL for all existing rows)
ALTER TABLE guide_bookings DROP COLUMN IF EXISTS user_id;
ALTER TABLE transport_bookings DROP COLUMN IF EXISTS user_id;
ALTER TABLE activity_bookings DROP COLUMN IF EXISTS user_id;
ALTER TABLE package_bookings DROP COLUMN IF EXISTS user_id;

-- Add user_id column as UUID referencing auth.users
ALTER TABLE guide_bookings ADD COLUMN user_id UUID REFERENCES auth.users(id);
ALTER TABLE transport_bookings ADD COLUMN user_id UUID REFERENCES auth.users(id);
ALTER TABLE activity_bookings ADD COLUMN user_id UUID REFERENCES auth.users(id);
ALTER TABLE package_bookings ADD COLUMN user_id UUID REFERENCES auth.users(id);
