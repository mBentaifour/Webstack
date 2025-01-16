import psycopg2

def test_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres.hbqpplveyaofcqtuippl",
            password="Azerty@123456++*",
            host="aws-0-eu-central-1.pooler.supabase.com",
            port="6543"
        )
        print("Connexion réussie à la base de données!")
        
        # Test d'une requête simple
        cur = conn.cursor()
        cur.execute("SELECT current_database();")
        db_name = cur.fetchone()[0]
        print(f"Nom de la base de données : {db_name}")
        
        # Fermeture des connexions
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Erreur de connexion : {str(e)}")

if __name__ == "__main__":
    test_db_connection()
