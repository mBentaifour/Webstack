import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Vérifier les variables Supabase
supabase_url = os.getenv('SUPABASE_URL')
supabase_anon_key = os.getenv('SUPABASE_ANON_KEY')

print("Test des variables d'environnement Supabase:")
print(f"SUPABASE_URL: {'Présent' if supabase_url else 'Manquant'}")
print(f"SUPABASE_ANON_KEY: {'Présent' if supabase_anon_key else 'Manquant'}")

if supabase_url and supabase_anon_key:
    print("\nValeurs trouvées:")
    print(f"URL: {supabase_url}")
    print(f"ANON_KEY: {supabase_anon_key[:10]}...")  # Afficher seulement le début de la clé pour la sécurité
else:
    print("\nERREUR: Certaines variables d'environnement sont manquantes")
