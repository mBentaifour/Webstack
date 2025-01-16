import os
from supabase import create_client, Client
import time

# Configuration Supabase
SUPABASE_URL = "https://hbqpplveyaofcqtuippl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhicXBwbHZleWFvZmNxdHVpcHBsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQyNzk1NzksImV4cCI6MjA0OTg1NTU3OX0.g-JyzBu2A8-_dm56lSxjGOHJ8FLN7cB7TbebxWvVjmA"

def setup_database():
    # Connexion à Supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("Configuration de la base de données...")
    
    try:
        # Créer le compte administrateur d'abord
        email = "bentaifourmoh@gmail.com"
        password = "AdminDroguerie2024!"
        
        print("\nCréation du compte administrateur...")
        
        try:
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "role": "admin"
                    }
                }
            })
            
            print(f"\nCompte administrateur créé avec succès!")
            print(f"Email: {email}")
            print(f"Mot de passe: {password}")
            print("\nVÉRIFIEZ VOTRE EMAIL IMMÉDIATEMENT pour confirmer votre compte!")
            print("Le lien de confirmation est valable pendant une courte durée.")
            
        except Exception as auth_error:
            if "User already registered" in str(auth_error):
                print("\nLe compte existe déjà. Tentative de connexion...")
                try:
                    auth_response = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })
                    print("Connexion réussie!")
                except Exception as login_error:
                    print(f"Erreur de connexion: {str(login_error)}")
                    return
            else:
                print(f"Erreur lors de la création du compte: {str(auth_error)}")
                return
        
        # SQL pour créer les tables
        sql = """
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

        -- Désactiver RLS pour l'installation initiale
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
        """
        
        try:
            # Exécuter le SQL
            supabase.query(sql).execute()
            print("Tables créées avec succès!")
            
            # Ajouter l'utilisateur à la table des profils
            user_id = auth_response.user.id
            supabase.table('profiles').insert({
                "id": user_id,
                "email": email,
                "role": "admin"
            }).execute()
            
            print("\nProfil administrateur configuré dans la base de données.")
            
        except Exception as e:
            print(f"Erreur: {str(e)}")
            if "duplicate key" in str(e):
                print("\nLe compte existe déjà. Vérifez votre email pour le lien de confirmation.")
        
        # Ajouter des données de test
        print("\nAjout des catégories de test...")
        categories = [
            {"name": "Outillage à main", "slug": "outillage-main", "description": "Outils manuels pour tous vos travaux"},
            {"name": "Électroportatif", "slug": "electroportatif", "description": "Outils électriques professionnels"},
            {"name": "Quincaillerie", "slug": "quincaillerie", "description": "Visserie et accessoires"}
        ]
        
        for category in categories:
            try:
                supabase.table('categories').insert(category).execute()
            except Exception as e:
                if "duplicate key" not in str(e):
                    print(f"Erreur lors de l'ajout de la catégorie {category['name']}: {str(e)}")
        
        print("Catégories ajoutées!")
        
        print("\nAjout des marques de test...")
        brands = [
            {"name": "Stanley", "slug": "stanley", "description": "Outillage professionnel"},
            {"name": "Bosch", "slug": "bosch", "description": "Leader de l'électroportatif"},
            {"name": "Facom", "slug": "facom", "description": "Outillage de qualité"}
        ]
        
        for brand in brands:
            try:
                supabase.table('brands').insert(brand).execute()
            except Exception as e:
                if "duplicate key" not in str(e):
                    print(f"Erreur lors de l'ajout de la marque {brand['name']}: {str(e)}")
        
        print("Marques ajoutées!")
        
        print("\nConfiguration terminée avec succès!")
        print("\nÉTAPES SUIVANTES:")
        print("1. Vérifiez votre email et confirmez votre compte")
        print("2. Une fois confirmé, connectez-vous avec vos identifiants")
        print("3. Vous pourrez alors ajouter et gérer les produits")
            
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    setup_database()
