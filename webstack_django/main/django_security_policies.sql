-- Activer RLS sur les tables Django
ALTER TABLE django_migrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE django_content_type ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth_permission ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth_group ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth_group_permissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth_user_groups ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth_user_user_permissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth_user ENABLE ROW LEVEL SECURITY;

-- Politiques pour django_migrations (accès admin uniquement)
CREATE POLICY "Admin access for migrations" ON django_migrations
    FOR ALL TO authenticated
    USING (true)
    WITH CHECK (true);

-- Politiques pour django_content_type
CREATE POLICY "Admin access for content types" ON django_content_type
    FOR ALL TO authenticated
    USING (true)
    WITH CHECK (true);

-- Politiques pour auth_permission
CREATE POLICY "Admin access for permissions" ON auth_permission
    FOR ALL TO authenticated
    USING (true)
    WITH CHECK (true);

-- Politiques pour auth_group
CREATE POLICY "Admin access for groups" ON auth_group
    FOR ALL TO authenticated
    USING (true)
    WITH CHECK (true);

-- Politiques pour auth_group_permissions
CREATE POLICY "Admin access for group permissions" ON auth_group_permissions
    FOR ALL TO authenticated
    USING (true)
    WITH CHECK (true);

-- Politiques pour auth_user_groups
CREATE POLICY "Admin access for user groups" ON auth_user_groups
    FOR ALL TO authenticated
    USING (true)
    WITH CHECK (true);

-- Politiques pour auth_user_user_permissions
CREATE POLICY "Admin access for user permissions" ON auth_user_user_permissions
    FOR ALL TO authenticated
    USING (true)
    WITH CHECK (true);

-- Politiques pour auth_user
CREATE POLICY "Admin access for users" ON auth_user
    FOR ALL TO authenticated
    USING (true)
    WITH CHECK (true);
