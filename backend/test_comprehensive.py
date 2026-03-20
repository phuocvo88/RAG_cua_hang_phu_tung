# -*- coding: utf-8 -*-
"""
Comprehensive test script for RAG system with new product data
"""
import sys
import io
import os

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag_engine import query_rag_system

def print_separator(char="=", length=70):
    print(char * length)

def test_query(query_text, description=""):
    """Test a single query and display results"""
    print(f"\n{'='*70}")
    if description:
        print(f"📝 {description}")
    print(f"❓ Query: {query_text}")
    print_separator("-")

    try:
        response = query_rag_system(query_text, provider="google")
        print(f"💬 Response:\n{response}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print_separator("=")

def main():
    print("\n" + "="*70)
    print(" 🚀 COMPREHENSIVE RAG SYSTEM TEST - New Product Data")
    print("="*70)

    # Test 1: Search by product name
    test_query(
        "Cho toi biet thong tin ve kinh chieu hau SH",
        "Test 1: Search by product name (Kinh chieu hau SH)"
    )

    # Test 2: Search by brand
    test_query(
        "Honda co nhung phu tung gi gia duoi 200000 dong?",
        "Test 2: Search by brand and price range"
    )

    # Test 3: Search by category
    test_query(
        "Tim phuoc cho xe Yamaha NVX",
        "Test 3: Search by vehicle model and part type"
    )

    # Test 4: Search for specific part
    test_query(
        "Bugi NGK co trong kho khong?",
        "Test 4: Check stock availability"
    )

    # Test 5: Search by SKU
    test_query(
        "Ma HD-017 la phu tung gi?",
        "Test 5: Search by SKU code"
    )

    # Test 6: General question
    test_query(
        "Lop xe Yamaha Exciter gia bao nhieu?",
        "Test 6: Price inquiry for specific model"
    )

    # Test 7: Compare products
    test_query(
        "So sanh gia noi Winner va phuoc NVX",
        "Test 7: Product comparison"
    )

    # Test 8: Promotion query
    test_query(
        "Co san pham nao dang khuyen mai khong?",
        "Test 8: Search for promotions"
    )

    print("\n" + "="*70)
    print(" ✅ TEST COMPLETED")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
