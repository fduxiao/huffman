from huffman import *
from unittest import TestCase


class TestEncode(TestCase):
    def test_forest(self):
        forest = Forest()
        forest.insert(HuffmanLeaf(1, 2))
        forest.insert(HuffmanLeaf(2, 1))
        forest.insert(HuffmanLeaf(3, 9))
        forest.insert(HuffmanLeaf(4, 8))

        self.assertEqual(forest.count, 4)
        self.assertListEqual(list(map(lambda x: x.tree.value, forest)), [2, 1, 4, 3])

        trees = [HuffmanLeaf(i, i) for i in range(10)]
        forest = Forest(*trees)
        self.assertEqual(forest.count, 10)
        nodes = [n for n in forest]
        self.assertEqual(len(nodes), 10)
        for n, t in zip(nodes, trees):
            self.assertIs(n.tree, t)

        for i in range(10):
            if i == 0:
                prev_node = forest.head
            else:
                prev_node = nodes[i-1]
            self.assertIs(prev_node.next, nodes[i])

            if i == 9:
                next_node = forest.tail
            else:
                next_node = nodes[i+1]
            self.assertIs(nodes[i].next, next_node)
