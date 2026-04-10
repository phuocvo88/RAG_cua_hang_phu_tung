"""
Run this script once locally to rebuild the vector store using Gemini embeddings.
Requires GOOGLE_API_KEY in backend/.env

Usage: python rebuild_index.py
"""
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

from llama_index.core import VectorStoreIndex, Document, Settings
from rag_engine import GeminiDirectEmbedding

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Make sure backend/.env is set up.")

Settings.embed_model = GeminiDirectEmbedding(api_key=GOOGLE_API_KEY)

documents = [
    Document(text="Kính chiếu hậu xe Honda Airblade đời 2018 hoàn toàn có thể dùng cho xe Honda Airblade 2020 hoặc 2021 vì chúng dùng chung 1 loại ngàm vặn chân 10 ly răng thuận. Giá của kính 2018 thường rẻ hơn một chút."),
    Document(text="Lốp xe số kích thước 90/90-14 có thể gắn vừa cho cả bánh sau xe Honda Airblade các đời từ 2013 đến 2022 và bánh sau xe Honda Vision."),
    Document(text="Bình ắc quy GS GTZ5S dùng tốt cho hầu hết các dòng xe tay ga nhỏ dưới 125 phân khối như Vision, Lead cũ, Airblade không có hệ thống dừng cầm chừng (Idling Stop)."),
    Document(text="Nhớt Motul 3100 Silver là nhớt bán tổng hợp, chạy dịu máy, anh em thợ khuyên nên dùng cho xe chạy loanh quanh trong phố, khoảng 1500km thay 1 lần."),
    Document(text="giá phanh trước SH 2023 là 250000 VND"),
    Document(text="cập nhật giá tàu hũ hay còn gọi bộ nồi của xe giá 1500000"),
]

STORAGE_DIR = "./database/storage"
if os.path.exists(STORAGE_DIR):
    shutil.rmtree(STORAGE_DIR)
os.makedirs(STORAGE_DIR)

print("Building index with Gemini embeddings...")
index = VectorStoreIndex.from_documents(documents)
index.storage_context.persist(persist_dir=STORAGE_DIR)
print("Done! Vector store saved to", STORAGE_DIR)
print("Now commit the database/storage/ folder and push to GitHub.")
