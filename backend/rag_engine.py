"""
RAG Engine - Phiên bản 2 sử dụng google-genai SDK mới nhất
kết hợp SQLAlchemy để query dữ liệu cấu trúc và LlamaIndex để query Vector DB
"""
import os
import sqlite3

from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types
from llama_index.core import StorageContext, load_index_from_storage, Settings, Document
from llama_index.core.embeddings import BaseEmbedding
from llama_index.llms.anthropic import Anthropic
from pydantic import Field
from typing import List, Any

# ==========================================
# CUSTOM GEMINI EMBEDDING (dùng google-genai SDK, không cần PyTorch)
# ==========================================
class GeminiDirectEmbedding(BaseEmbedding):
    api_key: str = Field(description="Google API key")

    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key=api_key, **kwargs)

    @classmethod
    def class_name(cls) -> str:
        return "GeminiDirectEmbedding"

    def _embed(self, text: str) -> List[float]:
        import requests
        url = f"https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent?key={self.api_key}"
        resp = requests.post(url, json={"content": {"parts": [{"text": text}]}})
        if not resp.ok:
            raise RuntimeError(f"Embedding API error: {resp.status_code} {resp.json().get('error', {}).get('message', '')}")
        return resp.json()["embedding"]["values"]

    def _get_query_embedding(self, query: str) -> List[float]:
        return self._embed(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        return self._embed(text)

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

_google_api_key = os.environ.get("GOOGLE_API_KEY", "")
if _google_api_key:
    Settings.embed_model = GeminiDirectEmbedding(api_key=_google_api_key)

# ==========================================
# ĐỌC API KEY TỪ FILE (Bảo mật)
# ==========================================
def read_api_key_from_file(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
    except Exception:
        pass
    return None

def get_google_api_key():
    # Try environment variable first (cross-platform)
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        # Try relative path as fallback (optional)
        key_file_path = os.path.join(".", "keys", "google_api_key.txt")
        api_key = read_api_key_from_file(key_file_path)
    return api_key

def get_anthropic_api_key():
    # Try environment variable first (cross-platform)
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # Try relative path as fallback (optional)
        key_file_path = os.path.join(".", "keys", "anthropic_api_key.txt")
        api_key = read_api_key_from_file(key_file_path)
    return api_key

# ==========================================
# 1. SQL SEARCH: Tìm sản phẩm trong CSDL
# ==========================================
def search_sql_by_keyword(keyword: str, limit: int = 10) -> str:
    """Tìm kiếm sản phẩm trong SQLite theo từ khóa"""
    conn = sqlite3.connect('./database/store.db')
    cursor = conn.cursor()

    # Search in name, SKU, category, brand, and notes
    cursor.execute('''
        SELECT sku, name, brand, category, price, in_stock, promotion, warranty, notes
        FROM products
        WHERE name LIKE ? OR sku LIKE ? OR category LIKE ? OR brand LIKE ? OR notes LIKE ?
        ORDER BY in_stock DESC, price ASC
        LIMIT ?
    ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', limit))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "Khong tim thay san pham phu hop trong co so du lieu."

    result_lines = ["Thong tin san pham tim duoc:"]
    for row in rows:
        sku, name, brand, category, price, in_stock, promotion, warranty, notes = row
        stock_status = "Con hang" if in_stock else "Het hang"
        promo_text = f" (KM: {promotion})" if promotion else ""
        warranty_text = f" | BH: {warranty}" if warranty else ""
        result_lines.append(
            f"- Ma: {sku} | {name} [{brand}] | Gia: {price:,} VND{promo_text} | {stock_status}{warranty_text}"
        )
    return "\n".join(result_lines)

def extract_keywords_from_query(query: str) -> list:
    """
    Extract potential product keywords from user query
    Simple approach: split query into words and filter common Vietnamese words
    """
    # Common Vietnamese stopwords to ignore
    stopwords = {
        'cho', 'toi', 'biet', 've', 'cua', 'va', 'co', 'khong', 'la', 'ma', 'san', 'pham',
        'gia', 'bao', 'nhieu', 'nao', 'nay', 'kia', 'het', 'hang', 'duoc', 'dung', 'nhu',
        'the', 'voi', 'tu', 'o', 'trong', 'tren', 'duoi', 'giup', 'tim', 'kiem', 'xem'
    }

    # Normalize and split query
    words = query.lower().split()

    # Extract meaningful keywords (length > 2 and not in stopwords)
    keywords = [w for w in words if len(w) > 2 and w not in stopwords]

    # Also try the full query as a keyword
    if query.strip():
        keywords.insert(0, query.strip())

    return keywords[:5]  # Return top 5 keywords

# ==========================================
# 2. VECTOR SEARCH: Tìm kiến thức tương thích
# ==========================================
def search_knowledge(query: str) -> str:
    """Tìm kiếm kinh nghiệm và thông tin tương thích trong Vector DB"""
    storage_dir = "./database/storage"
    if not os.path.exists(storage_dir) or not os.listdir(storage_dir):
        return ""
    try:
        storage_context = StorageContext.from_defaults(persist_dir=storage_dir)
        index = load_index_from_storage(storage_context)
        retriever = index.as_retriever(similarity_top_k=3)
        nodes = retriever.retrieve(query)
        if not nodes:
            return ""
        return "\n".join([n.text for n in nodes])
    except Exception as e:
        print(f"Vector search unavailable: {e}")
        return ""

# ==========================================
# 3. RAG QUERY FUNCTION
# ==========================================
def query_rag_system(user_query: str, provider: str = "google") -> str:
    """
    Main RAG query function:
    provider: "google" hoặc "anthropic" (mặc định Google Gemini)
    """
    # Extract keywords from user query dynamically
    keywords = extract_keywords_from_query(user_query)

    sql_context = ""
    for kw in keywords:
        result = search_sql_by_keyword(kw)
        if "Khong tim" not in result:
            sql_context = result
            break

    # If no results found, try a broader search with first word only
    if not sql_context and keywords:
        for word in keywords[1:]:  # Try individual words
            result = search_sql_by_keyword(word)
            if "Khong tim" not in result:
                sql_context = result
                break

    # Tìm kiến thức tương thích
    knowledge_context = search_knowledge(user_query)

    # Tạo Prompt kết hợp tất cả
    system_instruction = """Ban la tro ly tu van ban phu tung xe may chuyen nghiep.
Nhiem vu cua ban la tra loi ngan gon, chinh xac va chay theo phuong chau cua cua hang.
Khi tra loi:
- Neu ro TEN SAN PHAM va MA SKU (in hoa)
- Neu ro GIA BAN (dinh dang so VND)
- Neu ro TINH TUONG THICH voi cac dong xe khac neu co
- Tra loi bang tieng Viet don gian, de hieu"""

    prompt = f"""
Cau hoi cua nhan vien: {user_query}

--- DU LIEU SAN PHAM TU CO SO DU LIEU ---
{sql_context}

--- KIEN THUC TUONG THICH TU KHO KINH NGHIEM ---
{knowledge_context}

Vui long tong hop thong tin tren va tra loi cau hoi cua nhan vien.
"""

    if provider == "anthropic":
        api_key = get_anthropic_api_key()
        if not api_key:
            return "Loi: Khong tim thay ANTHROPIC_API_KEY."

        llm = Anthropic(model="claude-3-5-sonnet-20240620", api_key=api_key)
        # Combine system instruction with prompt since complete() doesn't accept system_prompt
        full_prompt = f"{system_instruction}\n\n{prompt}"
        response = llm.complete(full_prompt)
        return response.text
    else:
        # Fallback về Gemini dùng SDK mới
        api_key = get_google_api_key()
        if not api_key:
            return "Loi: Khong tim thay GOOGLE_API_KEY."
        
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="models/gemini-2.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                max_output_tokens=1024,
                temperature=0.2
            )
        )
        return response.text

# ==========================================
# 4. ADD KNOWLEDGE TO VECTOR DB DYNAMICALLY
# ==========================================
def add_knowledge_to_vector_db(knowledge_text: str) -> bool:
    """
    Add new knowledge document to the existing Vector Database
    This is used when admin approves a feedback submission
    """
    try:
        # Load existing index
        storage_context = StorageContext.from_defaults(persist_dir="./database/storage")
        index = load_index_from_storage(storage_context)

        # Create a new document from the knowledge text
        new_document = Document(text=knowledge_text)

        # Insert the document into the index
        index.insert(new_document)

        # Persist the updated index back to storage
        index.storage_context.persist(persist_dir="./database/storage")

        return True
    except Exception as e:
        print(f"Error adding knowledge to vector DB: {str(e)}")
        raise e
