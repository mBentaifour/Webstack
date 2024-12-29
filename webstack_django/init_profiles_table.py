import os
from supabase import create_client
from dotenv import load_dotenv
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_profiles_table():
    """Crée la table des profils utilisateurs"""
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        logger.error("Variables d'environnement manquantes")
        return
    
    try:
        supabase = create_client(supabase_url, supabase_key)
        
        # Créer la table profiles via l'API REST
        response = supabase.table('profiles').select('id').limit(1).execute()
        
        if response.data is None:
            # La table n'existe pas, on la crée
            logger.info("Création de la table profiles...")
            
            # Utiliser la fonction rpc pour exécuter le SQL
            sql = """
            CREATE TABLE IF NOT EXISTS public.profiles (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                phone VARCHAR(20),
                address TEXT,
                is_admin BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
                UNIQUE(user_id)
            );
            """
            
            # Exécuter via la fonction rpc
            supabase.rpc('exec_sql', {'sql': sql}).execute()
            
            # Configurer RLS et les politiques
            policies = [
                """
                ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
                """,
                """
                CREATE POLICY "Users can view own profile" 
                ON public.profiles FOR SELECT 
                USING (auth.uid() = user_id);
                """,
                """
                CREATE POLICY "Users can update own profile" 
                ON public.profiles FOR UPDATE 
                USING (auth.uid() = user_id);
                """,
                """
                CREATE POLICY "Admins can view all profiles" 
                ON public.profiles FOR SELECT 
                USING (
                    auth.uid() IN (
                        SELECT p.user_id 
                        FROM public.profiles p 
                        WHERE p.is_admin = true
                    )
                );
                """
            ]
            
            for policy in policies:
                try:
                    supabase.rpc('exec_sql', {'sql': policy}).execute()
                except Exception as e:
                    logger.warning(f"Erreur lors de l'application de la politique (peut-être déjà existante): {str(e)}")
            
            logger.info("Table des profils créée avec succès")
        else:
            logger.info("La table des profils existe déjà")
        
    except Exception as e:
        logger.error(f"Erreur lors de la création de la table des profils: {str(e)}")
        raise

if __name__ == "__main__":
    create_profiles_table()
