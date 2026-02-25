from typing import List
import math
import time
from page import Page
from bucket import Bucket

class HashIndex:
    def __init__(self, page_size: int, bucket_factor: int):
        self.page_size = page_size
        self.FR = bucket_factor  # Tuplas por bucket
        self.pages: List[Page] = []
        self.buckets: List[Bucket] = []
        self.NR = 0
        self.NB = 0

        # Estatísticas
        self.collisions = 0
        self.overflows = 0

    # ==========================
    # Função Hash (modular)
    # ==========================
    def hash_function(self, key: str) -> int:
        return hash(key) % self.NB

    # ==========================
    # Carregar arquivo e dividir em páginas
    # ==========================
    def load_data(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            records = [line.strip() for line in f.readlines()]

        self.NR = len(records)

        # Criar páginas
        total_pages = math.ceil(self.NR / self.page_size)

        for i in range(total_pages):
            start = i * self.page_size
            end = start + self.page_size
            page_records = records[start:end]
            self.pages.append(Page(i, page_records))

        print(f"Total de registros (NR): {self.NR}")
        print(f"Total de páginas criadas: {len(self.pages)}")

    # ==========================
    # Construção do índice
    # ==========================
    def build_index(self):

        # NB > NR / FR
        self.NB = math.ceil(self.NR / self.FR) + 1

        self.buckets = [Bucket(i, self.FR) for i in range(self.NB)]

        for page in self.pages:
            for key in page.records:
                bucket_index = self.hash_function(key)
                bucket = self.buckets[bucket_index]

                # Verificar colisão
                if len(bucket.entries) > 0:
                    self.collisions += 1

                overflow_occurred = bucket.insert(key, page.page_id)

                if overflow_occurred:
                    self.overflows += 1

        print(f"Número de Buckets (NB): {self.NB}")

    # ==========================
    # Busca usando índice
    # ==========================
    def search(self, key: str):
        start_time = time.time()

        bucket_index = self.hash_function(key)
        page_id, bucket_reads = self.buckets[bucket_index].search(key)

        page_reads = 0
        found = False

        if page_id is not None:
            page_reads += 1
            page = self.pages[page_id]
            if key in page.records:
                found = True

        end_time = time.time()
        elapsed = end_time - start_time

        total_cost = bucket_reads + page_reads

        return {
            "found": found,
            "page_id": page_id,
            "bucket_reads": bucket_reads,
            "page_reads": page_reads,
            "total_cost": total_cost,
            "time": elapsed
        }

    # ==========================
    # Table Scan
    # ==========================
    def table_scan(self, key: str):
        start_time = time.time()

        page_reads = 0
        found_page = None

        for page in self.pages:
            page_reads += 1
            if key in page.records:
                found_page = page.page_id
                break

        end_time = time.time()
        elapsed = end_time - start_time

        return {
            "found": found_page is not None,
            "page_id": found_page,
            "page_reads": page_reads,
            "total_cost": page_reads,
            "time": elapsed
        }

    # ==========================
    # Estatísticas
    # ==========================
    def statistics(self):
        collision_rate = (self.collisions / self.NR) * 100
        overflow_rate = (self.overflows / self.NR) * 100

        return {
            "collision_rate (%)": collision_rate,
            "overflow_rate (%)": overflow_rate
        }