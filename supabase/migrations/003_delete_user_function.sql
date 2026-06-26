-- Helper function to delete a user completely (auth + profile)
-- Run this SQL in Supabase SQL Editor

CREATE OR REPLACE FUNCTION public.delete_user(user_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
  -- Delete profile (trigger will handle auth.users deletion)
  DELETE FROM profiles WHERE id = user_id;
  RETURN TRUE;
EXCEPTION
  WHEN OTHERS THEN
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
