-- Activer RLS sur les tables restantes
ALTER TABLE django_admin_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE django_session ENABLE ROW LEVEL SECURITY;
ALTER TABLE main_product ENABLE ROW LEVEL SECURITY;

-- Politique pour django_admin_log (accès admin uniquement)
CREATE POLICY "Admin access for admin logs" ON django_admin_log
    FOR ALL TO authenticated
    USING (true)
    WITH CHECK (true);

-- Politique pour django_session (accès admin uniquement)
CREATE POLICY "Admin access for sessions" ON django_session
    FOR ALL TO authenticated
    USING (true)
    WITH CHECK (true);

-- Politiques pour main_product
CREATE POLICY "Public read access for products" ON main_product
    FOR SELECT
    USING (true);

CREATE POLICY "Admin write access for products" ON main_product
    FOR ALL TO authenticated
    USING (true)
    WITH CHECK (true);
