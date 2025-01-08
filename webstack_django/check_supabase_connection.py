import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

def check_supabase_connection():
    # Load environment variables
    load_dotenv('.env.new')
    
    # Get Supabase credentials
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("Error: Missing Supabase credentials in .env.new file")
        return False
    
    try:
        # Initialize Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Try to fetch something from the database
        response = supabase.table('products').select("*").limit(1).execute()
        
        if response.data is not None:
            print("Successfully connected to Supabase!")
            print(f"Retrieved {len(response.data)} records")
            return True
        else:
            print("Connection failed: No data received")
            return False
            
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Supabase connection...")
    check_supabase_connection()
