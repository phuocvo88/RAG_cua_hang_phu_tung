import sys
import os

# Thêm thư mục hiện tại vào path để import rag_engine
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_engine import query_rag_system

def test_claude_integration():
    print("--- ĐANG KIỂM TRA TÍCH HỢP CLAUDE ---")
    query = "Kính chiếu hậu Airblade có hàng không và giá bao nhiêu?"
    
    try:
        # Mặc định dùng anthropic
        response = query_rag_system(query)
        print("\nCâu trả lời từ Claude:")
        print("-" * 30)
        print(response)
        print("-" * 30)
    except Exception as e:
        print(f"\nLỗi khi gọi Claude: {e}")

if __name__ == "__main__":
    test_claude_integration()
