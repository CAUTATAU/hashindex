from hash_index import HashIndex
from fastapi import FastAPI
from pydantic import BaseModel

file_path = "words.txt"  # caminho do arquivo de palavras
app = FastAPI(title="Static Hash Index API")

class SearchRequest(BaseModel):
    page_size: int
    word: str

def build_index(page_size: int):
    bucket_factor = 50  # FR definido pela equipe

    index = HashIndex(page_size, bucket_factor)
    index.load_data(file_path)
    index.build_index()

    return index


def get_page_info(index):
    first_page = index.pages[0]
    last_page = index.pages[-1]

    return {
        "first_page": {
            "page_number": first_page.page_id,
            "records": first_page.records
        },
        "last_page": {
            "page_number": last_page.page_id,
            "records": last_page.records
        }
    }

@app.get("/")
def health_check():
    return {"message": "API de Índice Hash Estático está funcionando!"}

@app.post("/hash-search")
def hash_search(request: SearchRequest):

    index = build_index(request.page_size)

    page_info = get_page_info(index)

    result = index.search(request.word)

    return {
        "search_type": "hash_index",
        "word": request.word,
        "page_size": request.page_size,
        "pages_info": page_info,
        "search_result": result,
        "statistics": index.statistics()
    }


@app.post("/table-scan")
def table_scan(request: SearchRequest):

    index = build_index(request.page_size)

    page_info = get_page_info(index)

    result = index.table_scan(request.word)

    return {
        "search_type": "table_scan",
        "word": request.word,
        "page_size": request.page_size,
        "pages_info": page_info,
        "search_result": result
    }

"""with open(file_path, "r", encoding="utf-8") as f:
    content = f.read().splitlines()
    print(content[1])
    page_size = 100          # entrada do usuário
    bucket_factor = 50       # FR (definido pela equipe)

    index = HashIndex(page_size, bucket_factor)

    index.load_data(file_path)
    index.build_index()

    print("\nEstatísticas:")
    print(index.statistics())

    key = input("\nDigite a chave para buscar: ")

    print("\nBusca usando índice:")
    result_index = index.search(key)
    print(result_index)

    print("\nExecutando Table Scan:")
    result_scan = index.table_scan(key)
    print(result_scan)

    print("\nDiferença de tempo (scan - índice):",
        result_scan["time"] - result_index["time"])"""