from functools import wraps
from main.supabase_adapter import SupabaseAdapter

def rls_policy(table_name, policy_name):
    """
    Decorator to create RLS policies in Supabase
    """
    def decorator(policy_func):
        @wraps(policy_func)
        def wrapper(*args, **kwargs):
            policy = policy_func(*args, **kwargs)
            supabase = SupabaseAdapter()
            
            # Create or update the policy
            sql = f"""
            CREATE POLICY "{policy_name}" ON "{table_name}"
            AS PERMISSIVE
            FOR ALL
            TO authenticated
            USING ({policy['using']})
            WITH CHECK ({policy.get('with_check', policy['using'])});
            """
            
            try:
                supabase.execute_sql(sql)
            except Exception as e:
                # Policy might already exist, try to update it
                sql = f"""
                ALTER POLICY "{policy_name}" ON "{table_name}"
                USING ({policy['using']})
                WITH CHECK ({policy.get('with_check', policy['using'])});
                """
                supabase.execute_sql(sql)
                
            return policy
        return wrapper
    return decorator

# Example RLS policies
@rls_policy('products', 'products_view_policy')
def products_view_policy():
    return {
        'using': 'true',  # Anyone can view products
    }

@rls_policy('orders', 'orders_access_policy')
def orders_access_policy():
    return {
        'using': """
            auth.uid() = user_id 
            OR 
            EXISTS (
                SELECT 1 FROM auth.users
                WHERE auth.uid() = id
                AND 'admin' = ANY(roles)
            )
        """
    }

@rls_policy('user_profiles', 'profiles_access_policy')
def profiles_access_policy():
    return {
        'using': """
            auth.uid() = id 
            OR 
            EXISTS (
                SELECT 1 FROM auth.users
                WHERE auth.uid() = id
                AND 'admin' = ANY(roles)
            )
        """
    }

def setup_rls_policies():
    """
    Setup all RLS policies
    """
    products_view_policy()
    orders_access_policy()
    profiles_access_policy()
    
    # Enable RLS on all tables
    tables = ['products', 'orders', 'user_profiles']
    supabase = SupabaseAdapter()
    
    for table in tables:
        sql = f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;"
        try:
            supabase.execute_sql(sql)
        except Exception:
            # Table might already have RLS enabled
            pass
