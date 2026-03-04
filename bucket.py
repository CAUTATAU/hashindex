class Bucket:
    def __init__(self, bucket_id, capacity):
        self.bucket_id = bucket_id
        self.capacity = capacity
        self.entries = []  # (key, page_id)
        self.overflow = None  # Encadeamento para overflow

    def insert(self, key: str, page_id: int):
        if len(self.entries) < self.capacity:
            self.entries.append((key, page_id))
            return False  # não houve overflow
        else:
            # Overflow ocorreu aqui
            if self.overflow is None:
                self.overflow = Bucket(self.bucket_id, self.capacity)
                self.overflow.entries.append((key, page_id))
                return True  # novo overflow criado
            else:
                return self.overflow.insert(key, page_id)
        
    def search(self, key: str):
        current = self
        bucket_reads = 0

        while current:
            bucket_reads += 1
            for k, page_id in current.entries:
                if k == key:
                    return page_id, bucket_reads
            current = current.overflow

        return None, bucket_reads