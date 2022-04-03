from huffman.bitstream import *
from unittest import TestCase
from random import randbytes, getrandbits


def randbits(n):
    if n == 0:
        return ()
    bits = bin(getrandbits(n))[2:]
    bits = '0' * (n - len(bits)) + bits
    return list(map(int, bits))


class TestBitStream(TestCase):
    def test_bit_byte_bit(self):
        for i in range(1000):
            bits = randbits(i)
            bits2 = BytesToBits(BitsToBytes(bits))
            self.assertListEqual(list(bits), list(bits2)[:i])

        for i in range(1000):
            bits = randbits(1000)
            bits2 = BytesToBits(BitsToBytes(bits))
            self.assertListEqual(list(bits), list(bits2))

    def test_byte_bit_byte(self):
        for i in range(1000):
            bs = randbytes(i)
            bs2 = BitsToBytes(BytesToBits(bs))
            self.assertEqual(bs, bytes(bs2))

        for i in range(1000):
            bs = randbytes(1000)
            bs2 = BitsToBytes(BytesToBits(bs))
            self.assertEqual(bs, bytes(bs2))
