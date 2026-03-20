import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, ".")
from rag_engine import query_rag_system

print("=== TEST SCENARIO: Nhan vien hoi ve Guong chieu hau ===\n")
query = "Cho toi biet ma san pham va gia cua Kinh chieu hau Honda Airblade 2018. Va loai nay co dung duoc cho xe Airblade 2020 khong?"
print(f"Cau hoi: {query}")
print("\n" + "="*60 + "\n")
answer = query_rag_system(query)
print("\n" + "="*60)
print("Tra loi cua AI:")
print(answer)
