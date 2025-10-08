from collections import defaultdict
from dataclasses import dataclass
import hashlib
import os
from typing import List

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


class SimpleMiner:
    def __init__(self, hash_level: int):
        self.hash_level = hash_level

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


@dataclass
class BlockData:
    prev_hash: str
    nonce: int
    value: str
    block_hash: str


def read_block(block_id: int, block_folder: str, fork_id: int) -> BlockData:
    with open(block_folder + f'/block_{block_id}_{fork_id}', 'r') as f:
        previous_hash = f.readline().strip('\n')
        nonce = f.readline().strip('\n')
        value = f.readline().strip('\n')
        hashed_value = f.readline().strip('\n')
    res = BlockData(prev_hash=previous_hash, nonce=int(
        nonce), value=value, block_hash=hashed_value)
    return res


class MinerProofOfWork:
    def __init__(self, hash_level: int, current_block: int = 0, current_fork=0, blocks_folder: str = 'lesson_two_blocks'):
        self.hash_level = hash_level
        self.current_block = current_block
        self.blocks_folder = blocks_folder
        self.current_fork = current_fork

    @property
    def block(self):
        block = read_block(self.current_block,
                           self.blocks_folder, self.current_fork)
        return block

    @block.setter
    def block(self, s: str):
        prev_block = read_block(
            self.current_block, self.blocks_folder, self.current_fork)
        hash, nonce = self.mine(s, prev_block.block_hash)
        self.current_block += 1
        self.create_block(self.current_block,
                          prev_block.block_hash, nonce, s, hash)

    def fork_branch(self, block_id: int) -> str:
        for fork_id in range(self.current_fork, 15):
            filefullname = f"{self.blocks_folder}/block_{block_id}_{fork_id}"
            if not os.path.isfile(filefullname):
                return filefullname, fork_id
        raise ValueError('File for reach max limit')

    def create_block(self, n_block: int, previous_hash: str, nonce: int, value: str, hashed_value: str):
        file_fullname, fork_id = self.fork_branch(n_block)
        self.current_fork = int(fork_id)
        with open(file_fullname, 'w') as f:
            f.write(previous_hash + '\n')
            f.write(str(nonce) + '\n')
            f.write(value + '\n')
            f.write(hashed_value + '\n')
        return True

    def mine(self, s: str, previous_hash: str):
        n = 0
        line = str(s+str(previous_hash)+str(n))
        target_hash = hashlib.sha256(line.encode()).hexdigest()
        while target_hash[:self.hash_level] != '0' * self.hash_level:
            n += 1
            line = str(s+str(previous_hash)+str(n))
            target_hash = hashlib.sha256(line.encode()).hexdigest()

        return target_hash, n


class BlockChainChecker:
    def __init__(self, target_folder: str):
        self.target_folder = target_folder

    def find_all_blocks_id(self) -> List[List[int]]:
        filenames: List[str] = []
        ids: List[List[int]] = []
        for (_, _, filenames) in os.walk(self.target_folder):
            for filename in filenames:

                ids.append([int(filename.split('_')[1]),
                           int(filename.split('_')[2])])
        return ids

    def _is_hashed(self, block: BlockData) -> bool:
        block_data: str = str(block.value + block.prev_hash + str(block.nonce))
        hashing_value = hashlib.sha256(block_data.encode()).hexdigest()
        if hashing_value != block.block_hash:
            return False
        return True

    def _is_next_same_hash(self, block: BlockData, next_block: BlockData) -> bool:
        return block.block_hash == next_block.prev_hash

    def is_block_correct(self, block_id: int, fork_id: int) -> bool:
        block = read_block(block_id, self.target_folder, fork_id)
        if not self._is_hashed(block):
            return False
        try:
            next_block = read_block(block_id+1, self.target_folder, fork_id)
        except FileNotFoundError:
            return True
        if not self._is_next_same_hash(block, next_block):
            return False
        return True

    def check_all_blocks(self):
        ids = self.find_all_blocks_id()
        for block_id, fork_id in ids:
            if not self.is_block_correct(block_id, fork_id):
                return False, block_id, fork_id
        return True, 0, 0


m = MinerProofOfWork(2)
blockchecker = BlockChainChecker('lesson_two_blocks')

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

print(blockchecker.check_all_blocks())

hack_miner = MinerProofOfWork(2, 5)
hack_miner.block = 'IM HACKER'
hack_miner.block = 'correct transaction myau'
print(hack_miner.block)

m.block = 'Correct transaction'
print(m.block)

print(blockchecker.check_all_blocks())

bcc = BlockChainChecker('lesson_two_blocks')
