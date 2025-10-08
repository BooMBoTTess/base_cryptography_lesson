import hashlib
import os
from typing import Dict, List
from collections import defaultdict

def hash_custom_row(s: str) -> str:
    s = s.encode()
    return hashlib.sha256(s).hexdigest()

def find_similar_files(target_folder='./folder') -> list[str]:
    filenames:List[str] = []
    hash_table: Dict[str, List] = defaultdict(list)
    file_fullnames: List[str] = []
    for (dirpath, dirnames, filenames) in os.walk(target_folder):
        for f in filenames:
            file_fullnames.append(os.path.abspath(os.path.join(dirpath, f)))

    for filename in file_fullnames:
        with open(filename, 'r') as f:
            try:
                file_data = f.readlines()
            except UnicodeDecodeError as e:
                print('cant read file')
            hashed_file_data = hashlib.sha256(str(file_data).encode()).hexdigest()
            hash_table[hashed_file_data].append(filename)
    res = []
    for key, value in hash_table.items():
        if len(value) != 1:
            res.append(value) 
    return res

class simplehash():
    def __init__(self, filename: str = 'hash_file'):
        self.hash_file = filename
    @property
    def data(self):
        with open(self.hash_file, 'r') as f:
            return f.readlines()
    
    @data.setter
    def data(self, value: str):
        hashed_value = hashlib.sha256(str(value).encode()).hexdigest()
        with open(self.hash_file, 'w') as f:
            return f.write(value + ';' + hashed_value)
        
    def is_correct_data(self) -> bool:
        with open(self.hash_file, 'r') as f:
            for line in f.readlines():
                value, hash_value = line.split(';')
                hashing_value = hashlib.sha256(str(value).encode()).hexdigest()
                if hashing_value != hash_value:
                    return False
        return True

print(hash_custom_row('hello world'))
print(find_similar_files())


h_gen = simplehash()
h_gen.data = 'hello'
print(h_gen.data)
h_gen.data = 'world'
print(h_gen.data)
print(h_gen.is_correct_data())