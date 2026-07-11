import psycopg2
import sys

URL = "postgresql://postgres:fMFQAipszSase1ZV@db.jbiovrijnxrjmpkawlgx.supabase.co:5432/postgres"

def run():
    try:
        conn = psycopg2.connect(URL)
        cur = conn.cursor()
        
        tables = ['guide_bookings', 'transport_bookings', 'activity_bookings', 'package_bookings', 'users', 'user_roles']
        
        print("=== SCHEMA INFO ===")
        for t in tables:
            cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='public' AND table_name='{t}'")
            cols = cur.fetchall()
            if not cols:
                cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='auth' AND table_name='{t}'")
                cols = cur.fetchall()
                if cols:
                    print(f"Table auth.{t}:")
                else:
                    print(f"Table {t} does not exist.")
                    continue
            else:
                print(f"Table public.{t}:")
            for c in cols:
                print(f"  {c[0]}: {c[1]}")
                
        print("\n=== FOREIGN KEYS ===")
        for t in tables:
            cur.execute(f"""
                SELECT
                    kcu.column_name,
                    ccu.table_schema AS foreign_table_schema,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM 
                    information_schema.table_constraints AS tc 
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                      AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                      ON ccu.constraint_name = tc.constraint_name
                      AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='{t}';
            """)
            fks = cur.fetchall()
            for fk in fks:
                print(f"{t}.{fk[0]} -> {fk[1]}.{fk[2]}.{fk[3]}")
                
        print("\n=== RLS STATUS & POLICIES ===")
        for t in tables:
            cur.execute(f"""
                SELECT relrowsecurity 
                FROM pg_class 
                WHERE relname='{t}'
            """)
            rls_status = cur.fetchone()
            if rls_status:
                print(f"{t} RLS Enabled: {rls_status[0]}")
            
            cur.execute(f"""
                SELECT polname, polcmd, polroles, polqual, polwithcheck 
                FROM pg_policy 
                WHERE polrelid = '{t}'::regclass
            """)
            try:
                pols = cur.fetchall()
                for p in pols:
                    print(f"  Policy '{p[0]}' for {p[1]}: USING ({p[3]}) WITH CHECK ({p[4]})")
            except Exception as e:
                pass
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run()
