-- Function to delete user from auth.users when deleted from profiles
-- Run this SQL in Supabase SQL Editor

-- First, create a function to delete auth user
CREATE OR REPLACE FUNCTION public.delete_auth_user()
RETURNS TRIGGER AS $$
BEGIN
  -- Delete from auth.users using the service role
  -- Note: This requires the function to be SECURITY DEFINER
  DELETE FROM auth.users WHERE id = OLD.id;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger to delete auth user when profile is deleted
DROP TRIGGER IF EXISTS on_profile_deleted ON profiles;
CREATE TRIGGER on_profile_deleted
    AFTER DELETE ON profiles
    FOR EACH ROW EXECUTE FUNCTION public.delete_auth_user();
