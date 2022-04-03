from huffman import *
from unittest import TestCase
from random import choices


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

    def test_encode_bits(self):
        message = bytes(choices(range(256), k=1001))
        distribution = [0] * 256
        for code in message:
            distribution[code] += 1

        encoder = Encoder(distribution)
        self.assertEqual(len(encoder.end_code), encoder.end_code_length)
        encoder.forest.merge_step()
        self.assertListEqual(list(message), list(encoder.decode_bits(encoder.encode_bits(message))))

    def test_encode_bytes(self):
        message = bytes(choices(range(256), k=1001))
        distribution = [0] * 256
        for code in message:
            distribution[code] += 1

        encoder = Encoder(distribution)
        self.assertListEqual(list(message), list(encoder.decode(encoder.encode(message))))

        for i in range(1000, 1100):
            message = bytes(choices(range(256), k=i))
            self.assertListEqual(list(message), list(encoder.decode(encoder.encode(message)))[:i])

        encoder = Encoder(distribution, end_flag=False)
        for i in range(100):
            message = bytes(choices(range(256), k=i))
            self.assertListEqual(list(message), list(encoder.decode(encoder.encode(message)))[:i])
