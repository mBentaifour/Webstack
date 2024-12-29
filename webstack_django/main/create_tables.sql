-- Table des catégories
CREATE TABLE IF NOT EXISTS public.categories (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    name text NOT NULL UNIQUE,
    slug text NOT NULL UNIQUE,
    description text,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- Table des marques
CREATE TABLE IF NOT EXISTS public.brands (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    name text NOT NULL UNIQUE,
    slug text NOT NULL UNIQUE,
    description text,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- Table des produits
CREATE TABLE IF NOT EXISTS public.products (
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
CREATE POLICY "Lecture publique des catégories" ON public.categories
    FOR SELECT USING (true);

CREATE POLICY "Lecture publique des marques" ON public.brands
    FOR SELECT USING (true);

CREATE POLICY "Lecture publique des produits actifs" ON public.products
    FOR SELECT USING (is_active = true);

-- Politique pour permettre aux administrateurs de tout faire
CREATE POLICY "Les administrateurs peuvent tout faire sur les catégories" ON public.categories
    FOR ALL TO authenticated
    USING (EXISTS (SELECT 1 FROM public.profiles WHERE profiles.id = auth.uid() AND profiles.role = 'admin'))
    WITH CHECK (EXISTS (SELECT 1 FROM public.profiles WHERE profiles.id = auth.uid() AND profiles.role = 'admin'));

CREATE POLICY "Les administrateurs peuvent tout faire sur les marques" ON public.brands
    FOR ALL TO authenticated
    USING (EXISTS (SELECT 1 FROM public.profiles WHERE profiles.id = auth.uid() AND profiles.role = 'admin'))
    WITH CHECK (EXISTS (SELECT 1 FROM public.profiles WHERE profiles.id = auth.uid() AND profiles.role = 'admin'));

CREATE POLICY "Les administrateurs peuvent tout faire sur les produits" ON public.products
    FOR ALL TO authenticated
    USING (EXISTS (SELECT 1 FROM public.profiles WHERE profiles.id = auth.uid() AND profiles.role = 'admin'))
    WITH CHECK (EXISTS (SELECT 1 FROM public.profiles WHERE profiles.id = auth.uid() AND profiles.role = 'admin'));
