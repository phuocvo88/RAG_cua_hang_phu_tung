# -*- coding: utf-8 -*-
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

def test_gemini():
    print("=== TESTING GEMINI RAG SYSTEM ===\n")
    query = "Kinh chieu hau Airblade co hang khong va gia bao nhieu?"

    try:
        print(f"Query: {query}\n")
        print("Calling RAG system with Gemini...")
        response = query_rag_system(query, provider="google")
        print("\n" + "="*60)
        print("Response from Gemini:")
        print("="*60)
        print(response)
        print("="*60)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini()
