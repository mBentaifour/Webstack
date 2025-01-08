import os
from supabase import create_client
from datetime import datetime

# Configuration Supabase (utilisez les mêmes credentials que dans init_supabase_data.py)
SUPABASE_URL = "https://hbqpplveyaofcqtuippl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhicXBwbHZleWFvZmNxdHVpcHBsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNDI3OTU3OSwiZXhwIjoyMDQ5ODU1NTc5fQ.rLdOBtD3uJsEKnbj2QyvoyQVzh0XbsBGN4gITOXq48Y"

def create_notifications_table():
    if not SUPABASE_KEY:
        print("Erreur: Veuillez ajouter votre clé service_role dans le script")
        return
        
    try:
        # Initialiser le client Supabase
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print("Connexion à Supabase établie...")
        
        # Créer la table notifications via SQL
        sql = """
        CREATE TABLE IF NOT EXISTS public.notifications (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            type VARCHAR(50) NOT NULL,
            read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
        );

        -- Ajouter les politiques RLS pour la table notifications
        ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;

        -- Politique pour permettre aux utilisateurs de voir uniquement leurs notifications
        CREATE POLICY "Users can view their own notifications" 
        ON public.notifications FOR SELECT 
        USING (auth.uid() = user_id);

        -- Politique pour permettre aux utilisateurs de mettre à jour leurs notifications
        CREATE POLICY "Users can update their own notifications" 
        ON public.notifications FOR UPDATE 
        USING (auth.uid() = user_id);

        -- Créer un trigger pour mettre à jour updated_at
        CREATE OR REPLACE FUNCTION public.handle_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';

        CREATE TRIGGER update_notifications_updated_at
            BEFORE UPDATE ON public.notifications
            FOR EACH ROW
            EXECUTE PROCEDURE public.handle_updated_at();
        """
        
        # Exécuter le SQL
        result = supabase.rpc('exec_sql', {'query': sql}).execute()
        print("Table notifications créée avec succès!")
        
    except Exception as e:
        print("Erreur lors de la création de la table notifications:", str(e))

if __name__ == '__main__':
    print("Création de la table notifications dans Supabase...")
    create_notifications_table()
    print("\nTerminé!")
