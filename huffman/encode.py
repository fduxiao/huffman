from .tree import HuffmanBase, HuffmanLeaf
from .bitstream import BitsToBytes, BytesToBits


class ForestNode:
    """
    node for linked list
    """

    def __init__(self, tree: HuffmanBase = None, next_node=None):
        self.tree = tree
        self.next: ForestNode = next_node

    @property
    def frequency(self):
        if self.tree is None:
            return 0
        return self.tree.frequency


class Forest:
    """
    The Huffman tree forest is implemented as a linked list so as to manipulate it efficiently
    for us while keeping it sorted
    """
    def __init__(self, *trees):
        self.tail = ForestNode(None, None)
        self.head = ForestNode(None, self.tail)
        count = 0
        prev = self.head
        for t in trees:
            count += 1
            node = ForestNode(t, self.tail)
            prev.next = node
            prev = node
        self.count = count

    def __iter__(self):
        prev = self.head.next
        while prev is not self.tail:
            yield prev
            prev = prev.next

    def iter_prev(self):
        prev = self.head
        while prev is not self.tail:
            yield prev
            prev = prev.next

    def insert(self, tree: HuffmanBase):
        self.count += 1
        prev = self.head
        for prev in self.iter_prev():
            if prev.next.frequency > tree.frequency:
                break
        node = ForestNode(tree, prev.next)
        prev.next = node

    def merge_step(self):
        if self.count <= 1:
            return

        # pop the first two trees (smallest)
        self.count -= 2
        n1 = self.head.next
        n2 = n1.next
        self.head.next = n2.next
        self.insert(n1.tree + n2.tree)

    @property
    def final_tree(self):
        return self.head.next.tree


class Encoder:
    def __init__(self, distribution, end_flag=True):

        trees = [HuffmanLeaf(k, f) for k, f in enumerate(distribution)]
        if end_flag:
            trees.append(HuffmanLeaf(None, 0))
        trees.sort(key=lambda t: t.frequency)
        self.forest = Forest(*trees)
        # build the tree
        while self.forest.count > 1:
            self.forest.merge_step()

        # build table
        self.table = [0] * len(distribution)
        expectation = 0
        self.end_code_length = 0
        self.end_code = None
        for k, v in self.forest.final_tree.walk():
            if k is None:
                self.end_code_length = len(v)
                self.end_code = v
                continue
            self.table[k] = v
            expectation += len(v) * distribution[k]
        self.expectation = expectation

    def encode_bits(self, data):
        for i in data:
            code = self.table[i]
            for b in code:
                yield b

    def decode_bits(self, bits):
        yield from self.forest.final_tree.decode_stream(bits)

    def encode(self, stream):
        yield from BitsToBytes(self.encode_bits(stream), self.end_code or ())

    def decode(self, stream):
        for b in self.forest.final_tree.decode_stream(BytesToBits(stream)):
            if b is None:
                break
            yield b
