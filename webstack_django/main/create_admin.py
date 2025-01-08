from dotenv import load_dotenv
import os
from supabase import create_client, Client

def create_admin_account():
    # Charger les variables d'environnement
    load_dotenv()
    
    # Connexion à Supabase
    supabase: Client = create_client(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    try:
        # Créer un nouvel utilisateur admin
        email = "bentaifourmoh@gmail.com"
        password = "AdminDroguerie2024!"  # Mot de passe sécurisé
        
        # Enregistrer l'utilisateur avec une redirection personnalisée
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
        
        if auth_response.user:
            print(f"\nCompte administrateur créé avec succès!")
            print(f"Email: {email}")
            print(f"Mot de passe: {password}")
            print("\nVeuillez noter ces informations de connexion et les garder en sécurité.")
            print("\nIMPORTANT: Vérifiez votre email et cliquez sur le lien de confirmation.")
            print("NOTE: Si le lien expire, vous pouvez demander un nouveau lien de confirmation.")
            
            # Ajouter l'utilisateur à la table des profils avec le rôle admin
            user_id = auth_response.user.id
            supabase.table('profiles').insert({
                "id": user_id,
                "role": "admin",
                "email": email
            }).execute()
            
            print("\nProfil administrateur configuré dans la base de données.")
            
        else:
            print("Erreur: L'utilisateur n'a pas été créé.")
            
    except Exception as e:
        print(f"Erreur: {str(e)}")
        if "User already registered" in str(e):
            print("\nCe compte existe déjà. Vous pouvez demander un nouveau lien de confirmation.")
            try:
                # Demander un nouveau lien de confirmation
                supabase.auth.resend_signup_email({
                    "email": email,
                    "options": {
                        "emailRedirectTo": "http://localhost:3000/auth/success"
                    }
                })
                print("Un nouveau lien de confirmation a été envoyé à votre email.")
            except Exception as resend_error:
                print(f"Erreur lors de l'envoi du nouveau lien: {str(resend_error)}")

if __name__ == "__main__":
    create_admin_account()
