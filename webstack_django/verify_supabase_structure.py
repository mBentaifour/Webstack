import os
from dotenv import load_dotenv
from main.supabase_adapter import SupabaseAdapter
from typing import Dict, List

load_dotenv()

def check_table_structure():
    supabase = SupabaseAdapter()
    
    required_tables = {
        'categories': {
            'required_columns': {
                'id': 'uuid',
                'name': 'varchar',
                'slug': 'varchar',
                'description': 'text',
                'created_at': 'timestamptz',
                'updated_at': 'timestamptz'
            }
        },
        'brands': {
            'required_columns': {
                'id': 'uuid',
                'name': 'varchar',
                'slug': 'varchar',
                'description': 'text',
                'created_at': 'timestamptz',
                'updated_at': 'timestamptz'
            }
        },
        'products': {
            'required_columns': {
                'id': 'uuid',
                'name': 'varchar',
                'slug': 'varchar',
                'description': 'text',
                'price': 'numeric',
                'stock': 'integer',
                'category_id': 'uuid',
                'brand_id': 'uuid',
                'created_at': 'timestamptz',
                'updated_at': 'timestamptz'
            }
        },
        'notifications': {
            'required_columns': {
                'id': 'uuid',
                'user_id': 'uuid',
                'title': 'varchar',
                'message': 'text',
                'type': 'varchar',
                'read': 'boolean',
                'created_at': 'timestamptz',
                'updated_at': 'timestamptz'
            }
        },
        'orders': {
            'required_columns': {
                'id': 'bigint',
                'user_id': 'uuid',
                'status': 'varchar',
                'total_amount': 'numeric',
                'created_at': 'timestamptz'
            }
        },
        'order_items': {
            'required_columns': {
                'id': 'bigint',
                'order_id': 'bigint',
                'product_id': 'uuid',
                'quantity': 'integer',
                'price': 'numeric',
                'created_at': 'timestamptz'
            }
        }
    }

    print(">>> Vérification de la structure de la base de données Supabase...")
    print("\n=== Tables et Colonnes ===")

    for table_name, table_info in required_tables.items():
        try:
            # Vérifier si la table existe
            response = supabase.supabase.table(table_name).select("*").limit(1).execute()
            print(f"\n[OK] Table '{table_name}' existe")
        except Exception as e:
            print(f"[!!] Table '{table_name}' n'existe pas ou erreur: {str(e)}")

    print("\n=== Vérification des Relations ===")
    
    # Liste des relations attendues (public schema)
    public_relations = [
        ('products.category_id -> categories.id', 'products', 'categories(*)', 'category'),
        ('products.brand_id -> brands.id', 'products', 'brands(*)', 'brand'),
        ('order_items.order_id -> orders.id', 'order_items', 'orders(*)', 'order'),
        ('order_items.product_id -> products.id', 'order_items', 'products(*)', 'product')
    ]
    
    for relation_name, table, join_table, alias in public_relations:
        try:
            query = f"{alias}:{join_table}"
            response = supabase.supabase.table(table).select(query).limit(1).execute()
            print(f"[OK] Relation {relation_name}")
        except Exception as e:
            print(f"[!!] Problème avec la relation {relation_name}: {str(e)}")
    
    print("\n=== Vérification des Relations avec Auth Users ===")
    auth_tables = ['notifications', 'orders']
    
    for table in auth_tables:
        relation_name = f"{table}.user_id -> auth.users.id"
        try:
            # Vérifier si la colonne user_id existe et n'est pas null
            response = supabase.supabase.table(table).select("user_id").not_("user_id", "is", "null").limit(1).execute()
            print(f"[OK] Relation {relation_name}")
        except Exception as e:
            print(f"[!!] Problème avec la relation {relation_name}: {str(e)}")

if __name__ == "__main__":
    check_table_structure()
