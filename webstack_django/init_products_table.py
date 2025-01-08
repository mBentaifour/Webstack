from dotenv import load_dotenv
import os
from supabase import create_client, Client
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_products_tables(supabase: Client):
    """Initialise les tables liées aux produits dans Supabase."""
    try:
        # 1. Table des catégories avec politiques RLS
        logger.info("Création de la table categories...")
        categories_query = """
        -- Activer RLS
        alter table if exists categories enable row level security;
        
        -- Politique pour permettre la lecture à tous
        drop policy if exists "Categories are viewable by everyone" on categories;
        create policy "Categories are viewable by everyone"
        on categories for select
        using (true);
        
        -- Politique pour permettre l'insertion/modification aux administrateurs
        drop policy if exists "Categories are insertable by admins" on categories;
        create policy "Categories are insertable by admins"
        on categories for insert
        with check (true);
        
        drop policy if exists "Categories are updatable by admins" on categories;
        create policy "Categories are updatable by admins"
        on categories for update
        using (true)
        with check (true);
        """
        supabase.rpc('init_categories_policies', {}).execute()
        
        # 2. Table des marques avec politiques RLS
        logger.info("Création de la table brands...")
        brands_query = """
        -- Activer RLS
        alter table if exists brands enable row level security;
        
        -- Politique pour permettre la lecture à tous
        drop policy if exists "Brands are viewable by everyone" on brands;
        create policy "Brands are viewable by everyone"
        on brands for select
        using (true);
        
        -- Politique pour permettre l'insertion/modification aux administrateurs
        drop policy if exists "Brands are insertable by admins" on brands;
        create policy "Brands are insertable by admins"
        on brands for insert
        with check (true);
        
        drop policy if exists "Brands are updatable by admins" on brands;
        create policy "Brands are updatable by admins"
        on brands for update
        using (true)
        with check (true);
        """
        supabase.rpc('init_brands_policies', {}).execute()
        
        # 3. Table des produits avec politiques RLS
        logger.info("Création de la table products...")
        products_query = """
        -- Activer RLS
        alter table if exists products enable row level security;
        
        -- Politique pour permettre la lecture à tous
        drop policy if exists "Products are viewable by everyone" on products;
        create policy "Products are viewable by everyone"
        on products for select
        using (true);
        
        -- Politique pour permettre l'insertion/modification aux administrateurs
        drop policy if exists "Products are insertable by admins" on products;
        create policy "Products are insertable by admins"
        on products for insert
        with check (true);
        
        drop policy if exists "Products are updatable by admins" on products;
        create policy "Products are updatable by admins"
        on products for update
        using (true)
        with check (true);
        """
        supabase.rpc('init_products_policies', {}).execute()
        
        # 4. Table des mouvements de stock
        logger.info("Création de la table stock_movements...")
        stock_movements_query = """
        create type stock_movement_type as enum ('in', 'out', 'adjustment', 'return');
        
        create table if not exists stock_movements (
            id uuid default uuid_generate_v4() primary key,
            product_id uuid references products(id) not null,
            quantity integer not null,
            type stock_movement_type not null,
            reason text,
            reference_id uuid,  -- Pour lier à une commande ou un retour
            reference_type varchar(50),  -- 'order', 'return', etc.
            previous_stock integer not null,
            new_stock integer not null,
            created_by uuid references auth.users(id) not null,
            created_at timestamp with time zone default timezone('utc'::text, now()) not null
        );
        """
        supabase.query(stock_movements_query).execute()

        # 5. Table des alertes de stock
        logger.info("Création de la table stock_alerts...")
        stock_alerts_query = """
        create type alert_status as enum ('pending', 'processed', 'ignored');
        
        create table if not exists stock_alerts (
            id uuid default uuid_generate_v4() primary key,
            product_id uuid references products(id) not null,
            type varchar(50) not null,  -- 'low_stock', 'out_of_stock', 'overstock'
            message text not null,
            current_stock integer not null,
            threshold integer not null,
            status alert_status default 'pending' not null,
            processed_at timestamp with time zone,
            processed_by uuid references auth.users(id),
            created_at timestamp with time zone default timezone('utc'::text, now()) not null
        );
        """
        supabase.query(stock_alerts_query).execute()

        logger.info("Tables et politiques créées avec succès!")
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation des tables produits: {str(e)}")
        return False

def insert_test_data(supabase: Client):
    """Insère des données de test dans les tables."""
    try:
        # 1. Insérer des catégories de test
        logger.info("Insertion des catégories de test...")
        categories_data = [
            {
                "name": "Outillage à main",
                "slug": "outillage-a-main",
                "description": "Outils manuels pour tous vos travaux"
            },
            {
                "name": "Électroportatif",
                "slug": "electroportatif",
                "description": "Outils électriques pour plus d'efficacité"
            },
            {
                "name": "Quincaillerie",
                "slug": "quincaillerie",
                "description": "Tout pour l'assemblage et la fixation"
            },
            {
                "name": "Peinture",
                "slug": "peinture",
                "description": "Peintures et accessoires"
            },
            {
                "name": "Jardinage",
                "slug": "jardinage",
                "description": "Tout pour l'entretien du jardin"
            }
        ]
        
        for category in categories_data:
            supabase.table('categories').insert(category).execute()
            
        # 2. Insérer des marques de test
        logger.info("Insertion des marques de test...")
        brands_data = [
            {
                "name": "Bosch",
                "slug": "bosch",
                "description": "Marque leader en outillage"
            },
            {
                "name": "Stanley",
                "slug": "stanley",
                "description": "Outils professionnels"
            },
            {
                "name": "Makita",
                "slug": "makita",
                "description": "Spécialiste de l'électroportatif"
            }
        ]
        
        for brand in brands_data:
            supabase.table('brands').insert(brand).execute()
            
        # 3. Récupérer les IDs des catégories et marques
        categories = supabase.table('categories').select('id, slug').execute()
        brands = supabase.table('brands').select('id, slug').execute()
        
        category_ids = {cat['slug']: cat['id'] for cat in categories.data}
        brand_ids = {brand['slug']: brand['id'] for brand in brands.data}
        
        # 4. Insérer des produits de test
        logger.info("Insertion des produits de test...")
        products_data = [
            {
                "name": "Perceuse sans fil 18V",
                "slug": "perceuse-sans-fil-18v",
                "description": "Perceuse puissante avec batterie lithium-ion",
                "price": 129.99,
                "stock": 50,
                "category_id": category_ids['electroportatif'],
                "brand_id": brand_ids['bosch']
            },
            {
                "name": "Marteau de charpentier",
                "slug": "marteau-de-charpentier",
                "description": "Marteau professionnel en acier forgé",
                "price": 24.99,
                "stock": 100,
                "category_id": category_ids['outillage-a-main'],
                "brand_id": brand_ids['stanley']
            },
            {
                "name": "Scie sauteuse 650W",
                "slug": "scie-sauteuse-650w",
                "description": "Scie sauteuse professionnelle",
                "price": 89.99,
                "stock": 30,
                "category_id": category_ids['electroportatif'],
                "brand_id": brand_ids['makita']
            }
        ]
        
        for product in products_data:
            supabase.table('products').insert(product).execute()
            
        logger.info("Données de test insérées avec succès!")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'insertion des données de test: {str(e)}")
        raise

if __name__ == "__main__":
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("Les variables d'environnement SUPABASE_URL et SUPABASE_KEY sont requises")
    
    supabase = create_client(supabase_url, supabase_key)
    
    # Initialiser les tables
    init_products_tables(supabase)
    
    # Insérer les données de test
    insert_test_data(supabase)
