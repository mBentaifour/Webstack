from dotenv import load_dotenv
import os
from supabase import create_client, Client
import time

def resend_confirmation():
    # Charger les variables d'environnement
    load_dotenv()
    
    # Connexion à Supabase
    supabase: Client = create_client(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    email = "bentaifourmoh@gmail.com"
    password = "AdminDroguerie2024!"
    
    try:
        # Créer un nouveau compte qui enverra automatiquement un email de confirmation
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "role": "admin"
                },
                "emailRedirectTo": "http://localhost:3000/auth/success"
            }
        })
        
        print(f"\nUn nouveau lien de confirmation a été envoyé à {email}")
        print("Veuillez vérifier votre boîte mail et cliquer sur le lien.")
        print("NOTE: Le lien est valable pendant 24 heures.")
            
    except Exception as e:
        if "User already registered" in str(e):
            try:
                # Si l'utilisateur existe déjà, on essaie de se connecter
                auth_response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                print(f"\nVotre compte existe déjà.")
                print("Veuillez vérifier votre boîte mail pour un ancien lien de confirmation")
                print("ou contactez le support pour réinitialiser votre compte.")
            except Exception as login_error:
                print(f"Erreur de connexion: {str(login_error)}")
        else:
            print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    resend_confirmation()
