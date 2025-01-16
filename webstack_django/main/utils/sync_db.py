from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def sync_database_schema():
    """
    Synchronise le schéma de la base de données entre Django et Supabase
    """
    try:
        # Connexion à la base de données Supabase
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Créer un curseur
        cur = conn.cursor()
        
        # Activer l'extension uuid-ossp si elle n'est pas déjà activée
        cur.execute("""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        """)
        
        # Créer les tables nécessaires si elles n'existent pas
        cur.execute("""
        CREATE TABLE IF NOT EXISTS public.categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            slug VARCHAR(200) UNIQUE NOT NULL,
            category_type VARCHAR(50) NOT NULL,
            description TEXT,
            image VARCHAR(255),
            icon VARCHAR(50),
            featured_brands JSONB DEFAULT '[]'::jsonb,
            discount_count INTEGER DEFAULT 0,
            tips JSONB DEFAULT '[]'::jsonb,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS public.brands (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            slug VARCHAR(200) UNIQUE NOT NULL,
            logo VARCHAR(255),
            description TEXT,
            website VARCHAR(200),
            quality_tier VARCHAR(20) DEFAULT 'standard',
            country_of_origin VARCHAR(100),
            warranty_info TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS public.products (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            category_id INTEGER REFERENCES public.categories(id),
            brand_id INTEGER REFERENCES public.brands(id),
            name VARCHAR(200) NOT NULL,
            slug VARCHAR(200) UNIQUE NOT NULL,
            description TEXT,
            usage_type VARCHAR(20) DEFAULT 'diy',
            power_source VARCHAR(20),
            price DECIMAL(10,2) NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS public.reviews (
            id SERIAL PRIMARY KEY,
            product_id UUID REFERENCES public.products(id),
            user_id UUID REFERENCES auth.users(id),
            rating INTEGER CHECK (rating >= 1 AND rating <= 5),
            comment TEXT,
            pros TEXT,
            cons TEXT,
            usage_duration VARCHAR(50),
            usage_frequency VARCHAR(50),
            would_recommend BOOLEAN DEFAULT true,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(product_id, user_id)
        );
        """)
        
        # Ajouter des politiques RLS
        cur.execute("""
        ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.brands ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;
        ALTER TABLE public.reviews ENABLE ROW LEVEL SECURITY;

        -- Politique pour les catégories (lecture publique, écriture admin)
        CREATE POLICY IF NOT EXISTS "Categories are viewable by everyone" 
            ON public.categories FOR SELECT 
            USING (true);

        -- Politique pour les marques (lecture publique, écriture admin)
        CREATE POLICY IF NOT EXISTS "Brands are viewable by everyone" 
            ON public.brands FOR SELECT 
            USING (true);

        -- Politique pour les produits (lecture publique, écriture admin)
        CREATE POLICY IF NOT EXISTS "Products are viewable by everyone" 
            ON public.products FOR SELECT 
            USING (true);

        -- Politique pour les avis (lecture publique, écriture authentifiée)
        CREATE POLICY IF NOT EXISTS "Reviews are viewable by everyone" 
            ON public.reviews FOR SELECT 
            USING (true);
        CREATE POLICY IF NOT EXISTS "Users can create their own reviews" 
            ON public.reviews FOR INSERT 
            WITH CHECK (auth.uid() = user_id);
        CREATE POLICY IF NOT EXISTS "Users can update their own reviews" 
            ON public.reviews FOR UPDATE 
            USING (auth.uid() = user_id);
        """)
        
        print("Synchronisation réussie !")
        
    except Exception as e:
        print(f"Erreur lors de la synchronisation : {str(e)}")
        raise
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    sync_database_schema()
