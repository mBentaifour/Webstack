-- Politiques de sécurité consolidées pour Supabase

-- Politiques pour la table profiles
CREATE POLICY "Les utilisateurs peuvent voir leur propre profil"
ON public.profiles
FOR SELECT
TO authenticated
USING (auth.uid() = id);

CREATE POLICY "Les utilisateurs peuvent mettre à jour leur propre profil"
ON public.profiles
FOR UPDATE
TO authenticated
USING (auth.uid() = id);

-- Politiques pour la table products
CREATE POLICY "Lecture publique des produits actifs"
ON public.products
FOR SELECT
TO public
USING (is_active = true);

CREATE POLICY "Les administrateurs peuvent tout faire sur les produits"
ON public.products
FOR ALL
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = auth.uid()
        AND is_admin = true
    )
);

-- Politiques pour la table categories
CREATE POLICY "Lecture publique des catégories"
ON public.categories
FOR SELECT
TO public
USING (true);

CREATE POLICY "Les administrateurs peuvent tout faire sur les catégories"
ON public.categories
FOR ALL
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = auth.uid()
        AND is_admin = true
    )
);

-- Politiques pour la table brands
CREATE POLICY "Lecture publique des marques"
ON public.brands
FOR SELECT
TO public
USING (true);

CREATE POLICY "Les administrateurs peuvent tout faire sur les marques"
ON public.brands
FOR ALL
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = auth.uid()
        AND is_admin = true
    )
);

-- Politiques pour la table orders
CREATE POLICY "Les utilisateurs peuvent voir leurs propres commandes"
ON public.orders
FOR SELECT
TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "Les utilisateurs peuvent créer leurs propres commandes"
ON public.orders
FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "Les administrateurs peuvent tout voir"
ON public.orders
FOR SELECT
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = auth.uid()
        AND is_admin = true
    )
);

-- Politiques pour la table order_items
CREATE POLICY "Les utilisateurs peuvent voir leurs propres articles de commande"
ON public.order_items
FOR SELECT
TO authenticated
USING (
    order_id IN (
        SELECT id FROM public.orders
        WHERE user_id = auth.uid()
    )
);

CREATE POLICY "Les administrateurs peuvent tout faire sur les articles de commande"
ON public.order_items
FOR ALL
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = auth.uid()
        AND is_admin = true
    )
);
