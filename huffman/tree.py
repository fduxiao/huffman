"""
basic tree structure
"""


class HuffmanBase:
    """
    class interfaces
    """
    def __init__(self, frequency):
        self.frequency = frequency

    def __add__(self, other):
        return HuffmanBranch(self, other, self.frequency + other.frequency)

    def dump(self):
        pass

    def load(self, data):
        pass

    def walk(self, path_prefix=b""):
        pass

    def decode_one(self, stream):
        pass

    def decode_stream(self, stream):
        stream = iter(stream)
        while True:
            try:
                yield self.decode_one(stream)
            except StopIteration:
                return


class HuffmanLeaf(HuffmanBase):
    def __init__(self, value, frequency=1):
        super().__init__(frequency)
        self.value = value

    def dump(self):
        return self.value, self.frequency

    def load(self, data):
        self.value, self.frequency = data

    def walk(self, path_prefix=b""):
        yield self.value, path_prefix

    def decode_one(self, stream):
        return self.value


class HuffmanBranch(HuffmanBase):
    def __init__(self, left, right, frequency=None):
        if not isinstance(left, HuffmanBase):
            left = HuffmanLeaf(left)
        self.left = left

        if not isinstance(right, HuffmanBase):
            right = HuffmanLeaf(right)
        self.right = right

        if frequency is None:
            frequency = left.frequency + right.frequency
        super().__init__(frequency)

    def dump(self):
        return self.left.dump(), self.right.dump(), self.frequency

    def load(self, data):
        left, right, self.frequency = data
        self.left.load(left)
        self.right.load(right)

    def walk(self, path_prefix=b""):
        yield from self.left.walk(path_prefix+b"\0")
        yield from self.right.walk(path_prefix+b"\1")

    def decode_one(self, stream):
        i = next(stream)
        if i == 0:
            return self.left.decode_one(stream)
        else:
            return self.right.decode_one(stream)
