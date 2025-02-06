import hashlib

class MerkleTree:
    def __init__(self, data_list):
        self.leaves = [self.hash_data(data) for data in data_list]
        self.root = self.build_tree(self.leaves)

    def hash_data(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def build_tree(self, leaves):
        if len(leaves) == 1:
            return leaves[0]
        
        if len(leaves) % 2 != 0:
            leaves.append(leaves[-1])
        
        parent_level = []
        for i in range(0, len(leaves), 2):
            parent_hash = self.hash_data(leaves[i] + leaves[i + 1])
            parent_level.append(parent_hash)
        
        return self.build_tree(parent_level)

    def get_root(self):
        return self.root

# Example usage
data = ["block1"]
merkle_tree = MerkleTree(data)
print("Merkle Root:", merkle_tree.get_root())
