from huffman.tree import *
from unittest import TestCase
from random import choices
from functools import reduce


class TestTree(TestCase):
    def test_tree_init(self):
        h = HuffmanBranch(1, 2)
        self.assertIsInstance(h.left, HuffmanBase)
        self.assertIsInstance(h.right, HuffmanBase)
        self.assertEqual(h.frequency, 2)

    def test_tree(self):
        d1 = HuffmanLeaf(1)
        d2 = HuffmanLeaf(2)
        d3 = HuffmanLeaf(3)

        h = (d1 + d2) + d3
        h.load(h.dump())

        coding = {}
        for key, value in h.walk():
            coding[key] = value

        for key, value in coding.items():
            self.assertListEqual([key], list(h.decode_stream(value)))

        data = choices(list(coding.keys()), k=20)
        encoded = reduce(lambda a, b: a + b, map(lambda x: coding[x], data), b"")
        self.assertListEqual(data, list(h.decode_stream(encoded)))

    def test_coverage(self):
        h = HuffmanBase(1)
        h.dump()
        h.load(None)
        h.walk()
        h.decode_one(None)
