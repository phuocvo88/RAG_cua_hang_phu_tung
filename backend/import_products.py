# -*- coding: utf-8 -*-
"""
Import script to load products from products.csv into SQLite database
"""
import sqlite3
import csv
import os
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def import_products_from_csv(csv_path, db_path):
    """
    Import products from CSV file to SQLite database
    """
    # Check if CSV file exists
    if not os.path.exists(csv_path):
        print(f"ERROR: CSV file not found at {csv_path}")
        return False

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create products table (drop if exists for fresh import)
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            brand TEXT,
            category TEXT,
            price INTEGER NOT NULL,
            in_stock BOOLEAN NOT NULL,
            promotion TEXT,
            warranty TEXT,
            min_quantity INTEGER,
            notes TEXT
        )
    ''')

    # Read CSV and import data
    imported_count = 0
    skipped_count = 0

    print(f"Reading products from: {csv_path}")
    print("="*70)

    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                # Parse boolean for stock status
                in_stock = row['Ton_Kho'].strip().upper() in ['TRUE', '1', 'YES', 'CO']

                # Parse price (remove any non-numeric characters except digits)
                price = int(row['Gia'].strip())

                # Parse minimum quantity
                min_qty = int(row['SL_Toi_Thieu'].strip()) if row['SL_Toi_Thieu'].strip() else 0

                # Insert into database
                cursor.execute('''
                    INSERT INTO products (sku, name, brand, category, price, in_stock, promotion, warranty, min_quantity, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['Ma_SP'].strip(),
                    row['Ten_SP'].strip(),
                    row['Hang'].strip(),
                    row['Nhom_Hang'].strip(),
                    price,
                    in_stock,
                    row['Khuyen_Mai'].strip() if row['Khuyen_Mai'].strip() != '0' else None,
                    row['Bao_Hanh'].strip() if row['Bao_Hanh'].strip().lower() != 'khong' else None,
                    min_qty,
                    row['Ghi_Chu'].strip()
                ))

                imported_count += 1
                print(f"✓ Imported: {row['Ma_SP']} - {row['Ten_SP'][:40]}...")

            except Exception as e:
                skipped_count += 1
                print(f"✗ Skipped {row.get('Ma_SP', 'UNKNOWN')}: {e}")

    # Commit changes
    conn.commit()

    # Print summary
    print("="*70)
    print(f"\n✅ Import completed!")
    print(f"   - Successfully imported: {imported_count} products")
    print(f"   - Skipped/errors: {skipped_count} products")

    # Show sample data
    print("\n📊 Sample products in database:")
    print("-"*70)
    cursor.execute('SELECT sku, name, brand, price, in_stock FROM products LIMIT 5')
    for row in cursor.fetchall():
        stock_status = "✓ In stock" if row[4] else "✗ Out of stock"
        print(f"   {row[0]}: {row[1][:30]:30s} | {row[2]:7s} | {row[3]:>10,} VND | {stock_status}")

    # Show statistics
    print("\n📈 Database statistics:")
    print("-"*70)

    cursor.execute('SELECT COUNT(*) FROM products')
    total = cursor.fetchone()[0]
    print(f"   Total products: {total}")

    cursor.execute('SELECT COUNT(*) FROM products WHERE in_stock = 1')
    in_stock_count = cursor.fetchone()[0]
    print(f"   In stock: {in_stock_count}")

    cursor.execute('SELECT COUNT(*) FROM products WHERE in_stock = 0')
    out_of_stock = cursor.fetchone()[0]
    print(f"   Out of stock: {out_of_stock}")

    cursor.execute('SELECT brand, COUNT(*) FROM products GROUP BY brand')
    print(f"\n   By brand:")
    for brand, count in cursor.fetchall():
        print(f"      - {brand}: {count} products")

    cursor.execute('SELECT category, COUNT(*) FROM products GROUP BY category ORDER BY COUNT(*) DESC LIMIT 5')
    print(f"\n   Top 5 categories:")
    for category, count in cursor.fetchall():
        print(f"      - {category}: {count} products")

    conn.close()
    return True

if __name__ == "__main__":
    # Paths
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, 'products.csv')
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'store.db')

    print("🚀 Starting product import process...")
    print(f"   CSV source: {csv_path}")
    print(f"   Database: {db_path}")
    print()

    success = import_products_from_csv(csv_path, db_path)

    if success:
        print("\n✨ Import process completed successfully!")
    else:
        print("\n❌ Import process failed!")
        sys.exit(1)
