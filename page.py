from typing import List

class Page:
    def __init__(self, page_id, records: List[str]):
        self.page_id = page_id
        self.records = records

    def __repr__(self):
        return f"Page({self.page_id}, {len(self.records)} registros)"
        