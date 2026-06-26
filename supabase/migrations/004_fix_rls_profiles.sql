-- Fix RLS policies for profiles table
-- Run this SQL in Supabase SQL Editor

-- 先删除旧的策略
DROP POLICY IF EXISTS "Users can view own profile" ON profiles;

-- 创建新的策略：允许用户读取自己的 profile
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (
        auth.uid() = id
    );

-- 允许用户更新自己的 profile
DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (
        auth.uid() = id
    );

-- 允许认证用户插入 profile（用于注册触发器）
DROP POLICY IF EXISTS "Enable insert for authenticated users" ON profiles;
CREATE POLICY "Enable insert for authenticated users" ON profiles
    FOR INSERT WITH CHECK (
        auth.uid() = id
    );

-- 验证策略
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE tablename = 'profiles';
