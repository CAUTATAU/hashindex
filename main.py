from hash_index import HashIndex

file_path = "words.txt"  # caminho do arquivo de palavras

with open(file_path, "r", encoding="utf-8") as f:
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
        result_scan["time"] - result_index["time"])