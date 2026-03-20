import sqlite3
import pandas as pd
import chromadb
from llama_index.core import Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings
import os
from dotenv import load_dotenv

load_dotenv()

# Setup SQLite Database cho dữ liệu cấu trúc (Sản phẩm, giá, tồn kho)
def setup_sqlite_db():
    print("Setting up SQLite Database for products...")
    conn = sqlite3.connect('database/store.db')
    cursor = conn.cursor()

    # Tạo bảng Products
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT,
            price INTEGER NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    # Xóa dữ liệu cũ nếu có
    cursor.execute('DELETE FROM products')

    # Thêm dữ liệu mẫu (Mock data)
    products = [
        ('MIRROR-AB18', 'Kính chiếu hậu Honda Airblade 2018', 'Phụ tùng ngoài', 150000, 20),
        ('MIRROR-AB20', 'Kính chiếu hậu Honda Airblade 2020', 'Phụ tùng ngoài', 165000, 15),
        ('BRAKE-PAD-WAVE', 'Bố thắng đĩa trước Honda Wave Alpha', 'Phanh', 85000, 50),
        ('TIRE-MICHELIN-90/90-14', 'Lốp Michelin 90/90-14, Dùng cho bánh sau AB, Vision', 'Lốp xe', 550000, 10),
        ('OIL-MOTUL-3100', 'Nhớt Motul 3100 Silver 0.8L', 'Dầu nhớt', 110000, 100),
        ('BATTERY-GS-GTZ5S', 'Bình ắc quy GS GTZ5S 12V-3.5Ah', 'Điện - Bình', 280000, 30)
    ]

    cursor.executemany('INSERT INTO products (sku, name, category, price, stock) VALUES (?, ?, ?, ?, ?)', products)
    conn.commit()
    conn.close()
    print("SQLite Database setup completed.")

# Setup ChromaDB cho dữ liệu phi cấu trúc (Kiến thức ngầm, mẹo, khả năng tương thích)
def read_api_key_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception:
        return None

def setup_vector_db():
    print("Setting up Vector Database for compatibility knowledge...")
    
    # Lấy key từ file
    key_file_path = r"F:\side_projects\keys\Google key\RAG_cua_hang_phu_tung.txt"
    api_key = read_api_key_from_file(key_file_path)
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")
        
    if not api_key:
        print(f"WARNING: GOOGLE_API_KEY is not set in {key_file_path}. Cannot generate embeddings.")
        return

    os.environ["GOOGLE_API_KEY"] = api_key

    # Khởi tạo Local HuggingFace Embedding thay vì Gemini vì lỗi tương thích thư viện
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Settings.embed_model = embed_model
    
    # Kiến thức ngầm (Text)
    knowledge = [
        "Kính chiếu hậu xe Honda Airblade đời 2018 hoàn toàn có thể dùng cho xe Honda Airblade 2020 hoặc 2021 vì chúng dùng chung 1 loại ngàm vặn chân 10 ly răng thuận. Giá của kính 2018 thường rẻ hơn một chút.",
        "Lốp xe số kích thước 90/90-14 có thể gắn vừa cho cả bánh sau xe Honda Airblade các đời từ 2013 đến 2022 và bánh sau xe Honda Vision.",
        "Bình ắc quy GS GTZ5S dùng tốt cho hầu hết các dòng xe tay ga nhỏ dưới 125 phân khối như Vision, Lead cũ, Airblade không có hệ thống dừng cầm chừng (Idling Stop).",
        "Nhớt Motul 3100 Silver là nhớt bán tổng hợp, chạy dịu máy, anh em thợ khuyên nên dùng cho xe chạy loanh quanh trong phố, khoảng 1500km thay 1 lần."
    ]

    documents = [Document(text=t) for t in knowledge]
    
    # Tạo chỉ mục và lưu bằng SimpleVectorStore mặc định
    index = VectorStoreIndex.from_documents(
        documents,
        show_progress=True
    )
    
    # Lưu ra đĩa cứng tại thư mục database/storage
    index.storage_context.persist(persist_dir="./database/storage")
    print("Vector Database setup completed (SimpleVectorStore).")

if __name__ == "__main__":
    setup_sqlite_db()
    setup_vector_db()
