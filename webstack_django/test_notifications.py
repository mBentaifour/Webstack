import os
from dotenv import load_dotenv
from main.supabase_adapter import SupabaseAdapter
import time

# Charger les variables d'environnement
load_dotenv()

def test_notifications():
    # Initialiser l'adaptateur Supabase
    supabase = SupabaseAdapter()
    
    # Se connecter avec un utilisateur de test
    email = "bentaifourmoh@gmail.com"
    password = "AdminDroguerie2024!"
    
    # Connexion
    login_result = supabase.sign_in(email, password)
    if not login_result.get("success"):
        print("❌ Échec de la connexion:", login_result.get("error"))
        return
    
    user_id = login_result["data"]["user"]["id"]
    print("✅ Connexion réussie avec l'ID:", user_id)

    # Test 1: Créer une notification
    create_result = supabase.create_notification(
        user_id=user_id,
        title="Test de notification",
        message="Ceci est un test de création de notification",
        type="info"
    )
    
    if create_result.get("success"):
        print("✅ Notification créée avec succès")
        notification = create_result["data"]
        notification_id = notification["id"]
        print(f"  ID de la notification: {notification_id}")
    else:
        print("❌ Échec de la création de la notification:", create_result.get("error"))
        return

    # Attendre un peu pour s'assurer que la notification est bien enregistrée
    time.sleep(1)

    # Test 2: Récupérer les notifications
    get_result = supabase.get_notifications(user_id)
    if get_result.get("success"):
        notifications = get_result["data"]
        print(f"✅ {len(notifications)} notifications récupérées")
        for notif in notifications:
            print(f"  - {notif['title']}: {notif['message']} (lu: {notif['read']})")
    else:
        print("❌ Échec de la récupération des notifications:", get_result.get("error"))

    # Test 3: Marquer la notification comme lue
    mark_result = supabase.mark_notification_as_read(notification_id, user_id)
    if mark_result.get("success"):
        print("✅ Notification marquée comme lue")
    else:
        print("❌ Échec du marquage de la notification:", mark_result.get("error"))

    # Vérifier que la notification est bien marquée comme lue
    get_result = supabase.get_notifications(user_id)
    if get_result.get("success"):
        notifications = get_result["data"]
        for notif in notifications:
            if notif["id"] == notification_id:
                print(f"✅ État final de la notification: lu = {notif['read']}")

if __name__ == "__main__":
    test_notifications()
