import hashlib 

class SimpleMiner:
    def __init__(self, hash_level: int):
        self.hash_level= hash_level

    def mine(self, s: str):
        n = 0
        target_hash = hashlib.sha256(str(s+str(n)).encode()).hexdigest()
        while target_hash[:self.hash_level] != '0' * self.hash_level:
            n += 1
            target_hash = hashlib.sha256(str(s+str(n)).encode()).hexdigest()

        return target_hash, n

m = SimpleMiner(2)
hash_value, n = m.mine('dwadfsdpfsdhfhe;fjekjfwdhwwd')
print(hash_value, n)
blocks_folder = 'lesson_two_blocks'
class MinerProofOfWork:
    def __init__(self, hash_level: int, current_block: int = 0, blocks_folder: str = 'lesson_two_blocks'):
        self.hash_level= hash_level
        self.current_block = current_block
        self.blocks_folder = blocks_folder

    @property
    def block(self):
        block = self.read_block(self.current_block)
        return block

    @block.setter
    def block(self, s: str):
        prev_block = self.read_block(self.current_block)
        hash, nonce = self.mine(s, prev_block[3])
        self.current_block += 1
        self.create_block(self.current_block, prev_block[3], nonce, s, hash)


    def read_block(self, n_block: int):
        with open(self.blocks_folder + f'/block_{n_block}', 'r') as f:
            previous_hash = f.readline().strip('\n')
            nonce = f.readline().strip('\n')
            value = f.readline().strip('\n')
            hashed_value = f.readline().strip('\n')
        return previous_hash, nonce, value, hashed_value

    def create_block(self, n_block: int, previous_hash: str, nonce: int, value: str, hashed_value: str):
        with open(self.blocks_folder + f'/block_{n_block}', 'w') as f:
            f.write(previous_hash + '\n')
            f.write(str(nonce) + '\n')
            f.write(value + '\n')
            f.write(hashed_value + '\n')
        return True

    def mine(self, s: str, previous_hash: str):
        n = 0
        line = str(s+str(previous_hash)+str(n))
        print('\n\n',line)
        target_hash = hashlib.sha256(line.encode()).hexdigest()
        while target_hash[:self.hash_level] != '0' * self.hash_level:
            n += 1
            target_hash = hashlib.sha256(str(s+str(n)).encode()).hexdigest()

        return target_hash, n

m = MinerProofOfWork(2)
m.block = 'hello world'
print(m.block)
m.block = 'goodbye world'
print(m.block)
m.block = 'hello kitty buul'
print(m.block)
m.block = 'hello world'
print(m.block)
m.block = 'goodbye world'
print(m.block)
m.block = 'hello kitty buul'
print(m.block)