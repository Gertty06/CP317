import services
import db
from pathlib import Path
DEFAULT_CART_ID = 1 

def initialize_database_if_needed():
    """Helper to ensure the SQLite database is created and seeded if missing."""
    db_file = db.DB_PATH
    if not db_file.exists():
        print("[*] Initializing database from database.sql...")
        db_file.parent.mkdir(parents=True, exist_ok=True)
        # Point to database.sql inside the carco-db folder
        schema_path = Path(__file__).parent / "carco-db" / "database.sql"
        schema_sql = schema_path.read_text()
        with db.get_connection() as conn:
            conn.executescript(schema_sql)
        print("[+] Database initialized successfully.")
        
def main():
    initialize_database_if_needed()
    
    while True:
        print("\n==============================")
        print("      CARCO E-STORE (CLI)     ")
        print("==============================")
        print("1. Browse & Filter Products (FR-1)")
        print("2. Find Parts by Vehicle (FR-1)")
        print("3. View Product Details (FR-2)")
        print("4. Add to cart (FR-3)")
        print("5. View current total (FR-3)")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == "1":
            print("\n--- Browse & Filter Products ---")
            cat_input = input("Category ID (Leave blank for all): ").strip()
            brand_input = input("Brand ID (Leave blank for all): ").strip()
            max_input = input("Max Price in $ (e.g., 150, leave blank for any): ").strip()
            
            cat_id = int(cat_input) if cat_input.isdigit() else None
            brand_id = int(brand_input) if brand_input.isdigit() else None
            max_p = float(max_input) if max_input else None
            
            results = services.search_catalog(category_id=cat_id, brand_id=brand_id, max_price=max_p)
            
            print(f"\nFound {len(results)} product(s):")
            for p in results:
                print(f"  ID: {p['product_id']} | {p['name']} ({p['brand']} - {p['category']}) - {p['price_formatted']}")
                
        elif choice == "2":
            print("\n--- Fitment Search ---")
            make = input("Vehicle Make (e.g., Honda): ").strip()
            model = input("Vehicle Model (e.g., Civic): ").strip()
            year_str = input("Vehicle Year (e.g., 2022): ").strip()
            
            if year_str.isdigit():
                parts = services.get_filtered_parts_by_vehicle(make, model, int(year_str))
                print(f"\nParts fitting {year_str} {make} {model}:")
                for p in parts:
                    print(f"  ID: {p['product_id']} | {p['name']} - {p['price_formatted']}")
            else:
                print("[-] Invalid year format.")
                
        elif choice == "3":
            print("\n--- Product Details View ---")
            pid_str = input("Enter Product ID: ").strip()
            if pid_str.isdigit():
                prod = services.get_product_details(int(pid_str))
                if prod:
                    print(f"\n=== {prod['name']} ===")
                    print(f"Brand: {prod.get('brand', 'N/A')}")
                    print(f"Price: {prod['price_formatted']}")
                    print(f"Status: {prod['availability_status']} ({prod['stock']} units left)")
                    print(f"Description: {prod['description']}")
                    print(f"Install Instructions: {prod['install_instructions']}")
                    print("Vehicle Fitment:")
                    if prod["fitment"]:
                        for f in prod["fitment"]:
                            print(f"  - {f['year']} {f['make']} {f['model']}")
                    else:
                        print("  - Universal / No specific fitment listed")
                else:
                    print("[-] Product not found or inactive.")
            else:
                print("[-] Invalid ID.")
        elif choice == "4":
            services.add_to_cart(DEFAULT_CART_ID)

            break

        elif choice == "5":
            services.display_total(DEFAULT_CART_ID)      
            
        elif choice == "6":
            print("Exiting. Goodbye!")
            break
        else:
            print("[-] Invalid selection. Choose 1-6.")

if __name__ == "__main__":
    main()
