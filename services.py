import db

def search_catalog(category_id=None, brand_id=None, min_price=None, max_price=None):
    """
    FR-1: Browse and filter available products.
    Accepts human-friendly price inputs (in dollars) and converts them to cents.
    """
    min_cents = int(min_price * 100) if min_price is not None else None
    max_cents = int(max_price * 100) if max_price is not None else None
    
    products = db.get_products(
        category_id=category_id, 
        brand_id=brand_id, 
        min_cents=min_cents, 
        max_cents=max_cents
    )
    
    # Format prices for clean presentation
    for p in products:
        p["price_formatted"] = f"${p['price_cents'] / 100:.2f}"
        
    return products

def get_filtered_parts_by_vehicle(make, model, year):
    """
    FR-1 Variant: Filter parts specifically fitting a user's vehicle.
    """
    parts = db.find_parts(make, model, year)
    for p in parts:
        p["price_formatted"] = f"${p['price_cents'] / 100:.2f}"
    return parts

def get_product_details(product_id):
    """
    FR-2: Show product details including price, description, installation instructions,
    availability status, stock count, and fitment list.
    """
    product = db.get_product(product_id)
    if not product:
        return None
        
    product["price_formatted"] = f"${product['price_cents'] / 100:.2f}"
    product["availability_status"] = "In Stock" if product["in_stock"] else "Out of Stock"
    
    return product


def add_to_cart(cart_id):
    """UI-3: Prompt for product and quantity, then insert/update cart."""
    print("\n--- Add Item to Cart ---")
    pid_input = input("Enter Product ID: ").strip()
    if not pid_input.isdigit():
        print("[-] Invalid Product ID. Must be an integer.")
        return

    product_id = int(pid_input)

    qty_input = input("Enter Quantity (default 1): ").strip()
    if not qty_input:
        quantity = 1
    elif qty_input.isdigit() and int(qty_input) > 0:
        quantity = int(qty_input)
    else:
        print("[-] Quantity must be a positive integer.")
        return

    try:

        db.add_to_cart(cart_id, product_id, quantity)

        print(f"[+] Successfully added {quantity} unit(s) of Product #{product_id} to Cart #{cart_id}.")
    except Exception as e:
        print(f"[-] Could not add product: {e}")
    return

def display_total(cart_id):
    """UI-3: Query cart summary and display formatted currency values."""
    print(f"\n--- Cart #{cart_id} Summary ---")
    try:

        totals = db.get_cart_total(cart_id)

        subtotal = totals["subtotal_cents"] / 100
        tax = totals["tax_cents"] / 100
        total = totals["total_cents"] / 100

        print(f"  Subtotal: ${subtotal:,.2f}")
        print(f"  HST (13%): ${tax:,.2f}")
        print(f"  Total:    ${total:,.2f}")
    except Exception as e:
        print(f"[-] Failed to fetch cart total: {e}")
    return
