from .tree import HuffmanBase


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
