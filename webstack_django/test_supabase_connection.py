from supabase import create_client
import os

# Configuration Supabase
SUPABASE_URL = 'https://hbqpplveyaofcqtuippl.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhicXBwbHZleWFvZmNxdHVpcHBsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQyNzk1NzksImV4cCI6MjA0OTg1NTU3OX0.g-JyzBu2A8-_dm56lSxjGOHJ8FLN7cB7TbebxWvVjmA'

def test_connection():
    try:
        # Création du client Supabase
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Test de connexion en récupérant les données d'une table
        print("Tentative de connexion à Supabase...")
        
        # Test de lecture des données
        response = supabase.table('categories').select("*").execute()
        print("\nDonnées de la table categories :")
        print(response.data)
        
        return True, "Connexion réussie à Supabase!"
        
    except Exception as e:
        return False, f"Erreur de connexion : {str(e)}"

if __name__ == "__main__":
    success, message = test_connection()
    print(f"\nRésultat : {message}")
