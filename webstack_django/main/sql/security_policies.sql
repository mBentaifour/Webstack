-- Étape 1: Activer RLS sur toutes les tables
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE brands ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE inventory ENABLE ROW LEVEL SECURITY;

-- Étape 2: Politiques pour les catégories (lecture publique, modification admin)
CREATE POLICY "Lecture publique des catégories" 
    ON categories FOR SELECT 
    USING (true);

CREATE POLICY "Modification des catégories par admin" 
    ON categories FOR ALL 
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- Étape 3: Politiques pour les marques
CREATE POLICY "Lecture publique des marques" 
    ON brands FOR SELECT 
    USING (true);

CREATE POLICY "Modification des marques par admin" 
    ON brands FOR ALL 
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- Étape 4: Politiques pour les produits
CREATE POLICY "Lecture publique des produits" 
    ON products FOR SELECT 
    USING (true);

CREATE POLICY "Modification des produits par admin" 
    ON products FOR ALL 
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- Étape 5: Politiques pour les avis
CREATE POLICY "Lecture publique des avis" 
    ON reviews FOR SELECT 
    USING (true);

CREATE POLICY "Création d'avis par utilisateurs authentifiés" 
    ON reviews FOR INSERT 
    TO authenticated
    WITH CHECK (true);

CREATE POLICY "Modification de ses propres avis" 
    ON reviews FOR UPDATE 
    TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Suppression de ses propres avis" 
    ON reviews FOR DELETE 
    TO authenticated
    USING (auth.uid() = user_id);

-- Étape 6: Politiques pour l'inventaire
CREATE POLICY "Lecture de l'inventaire par admin" 
    ON inventory FOR SELECT 
    TO authenticated
    USING (true);

CREATE POLICY "Modification de l'inventaire par admin" 
    ON inventory FOR ALL 
    TO authenticated
    USING (true)
    WITH CHECK (true);
