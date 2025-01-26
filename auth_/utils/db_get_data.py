from sqlalchemy import create_engine, text
from django.conf import settings
from urllib.parse import quote_plus
import os

def get_db_connection():
    try:
        # Récupérer les informations de connexion
        db_user = str(settings.DATABASES['default']['USER'])
        db_password = str(settings.DATABASES['default']['PASSWORD'] or '')  # Utiliser une chaîne vide si None
        db_host = str(settings.DATABASES['default']['HOST'])
        db_name = str(settings.DATABASES['default']['NAME'])
        
        # Encoder le mot de passe pour l'URL
        encoded_password = quote_plus(db_password) if db_password else ''
        
        # Construire l'URL de connexion
        DATABASE_URL = f"postgresql://{db_user}:{encoded_password}@{db_host}/{db_name}"
        
        # Créer le moteur SQLAlchemy
        engine = create_engine(DATABASE_URL)
        return engine
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {str(e)}")
        raise

def email_exists(email):
    try:
        engine = get_db_connection()
        with engine.connect() as connection:
            query = text("SELECT EXISTS(SELECT 1 FROM auth.users WHERE email = :email)")
            result = connection.execute(query, {"email": email})
            return result.scalar()
    except Exception as e:
        print(f"Erreur lors de la vérification de l'email: {str(e)}")
        return False 