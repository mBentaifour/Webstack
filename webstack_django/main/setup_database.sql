-- Supprimer les tables existantes
DROP TABLE IF EXISTS public.products CASCADE;
DROP TABLE IF EXISTS public.brands CASCADE;
DROP TABLE IF EXISTS public.categories CASCADE;
DROP TABLE IF EXISTS public.profiles CASCADE;

-- Créer la table des profils
CREATE TABLE public.profiles (
    id uuid REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
    email text NOT NULL,
    role text NOT NULL DEFAULT 'user',
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- Désactiver temporairement RLS pour l'installation initiale
ALTER TABLE public.profiles DISABLE ROW LEVEL SECURITY;

-- Créer la table des catégories
CREATE TABLE public.categories (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    name text NOT NULL UNIQUE,
    slug text NOT NULL UNIQUE,
    description text,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- Créer la table des marques
CREATE TABLE public.brands (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    name text NOT NULL UNIQUE,
    slug text NOT NULL UNIQUE,
    description text,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- Créer la table des produits
CREATE TABLE public.products (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    name text NOT NULL,
    slug text NOT NULL UNIQUE,
    description text,
    price decimal(10,2) NOT NULL,
    stock integer NOT NULL DEFAULT 0,
    category_id uuid REFERENCES public.categories(id),
    brand_id uuid REFERENCES public.brands(id),
    image_url text,
    is_active boolean DEFAULT true,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- Activer RLS sur toutes les tables
ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.brands ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;

-- Politique pour permettre la lecture publique
CREATE POLICY "Lecture publique des catégories"
ON public.categories FOR SELECT
USING (true);

CREATE POLICY "Lecture publique des marques"
ON public.brands FOR SELECT
USING (true);

CREATE POLICY "Lecture publique des produits actifs"
ON public.products FOR SELECT
USING (is_active = true);

-- Politique pour permettre aux administrateurs de tout faire
CREATE POLICY "Les administrateurs peuvent tout faire sur les catégories"
ON public.categories FOR ALL
TO authenticated
USING (true)
WITH CHECK (true);

CREATE POLICY "Les administrateurs peuvent tout faire sur les marques"
ON public.brands FOR ALL
TO authenticated
USING (true)
WITH CHECK (true);

CREATE POLICY "Les administrateurs peuvent tout faire sur les produits"
ON public.products FOR ALL
TO authenticated
USING (true)
WITH CHECK (true);

-- Réactiver RLS sur la table des profils avec des politiques plus permissives
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Politique pour permettre l'insertion initiale des profils
CREATE POLICY "Permettre l'insertion des profils"
ON public.profiles FOR INSERT
TO authenticated
WITH CHECK (true);

-- Politique pour permettre la lecture des profils
CREATE POLICY "Permettre la lecture des profils"
ON public.profiles FOR SELECT
TO authenticated
USING (true);

-- Politique pour permettre la mise à jour des profils
CREATE POLICY "Permettre la mise à jour des profils"
ON public.profiles FOR UPDATE
TO authenticated
USING (true)
WITH CHECK (true);
