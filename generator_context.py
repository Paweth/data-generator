from typing import *

# from tables import Table

class GeneratorContext:
    def __init__(self):
        self.tables_max_id : Dict[Table, int | Tuple[int]] = {}
        self.existing_key_pairs : Dict[Table, Set[int, int]] = {}
