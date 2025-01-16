from supabase import create_client
import os
from dotenv import load_dotenv

# Configuration Supabase
SUPABASE_URL = 'https://hbqpplveyaofcqtuippl.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhicXBwbHZleWFvZmNxdHVpcHBsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQyNzk1NzksImV4cCI6MjA0OTg1NTU3OX0.g-JyzBu2A8-_dm56lSxjGOHJ8FLN7cB7TbebxWvVjmA'

def test_supabase_connection():
    try:
        # Création du client Supabase
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Test de connexion simple
        print("Tentative de connexion à Supabase...")
        
        # Liste des tables disponibles
        print("\nTables disponibles :")
        tables = supabase.table('').select("*").execute()
        print(tables)
        
        return True, "Connexion réussie à Supabase!"
        
    except Exception as e:
        return False, f"Erreur de connexion : {str(e)}"

if __name__ == "__main__":
    success, message = test_supabase_connection()
    print(f"\nRésultat : {message}")
