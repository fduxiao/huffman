class BytesToBits:
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        for b in self.iterable:
            for i in range(8):
                yield (b & (1 << i)) >> i


class BitsToBytes:
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        shift = 0
        acc = 0
        for bit in self.iterable:
            acc |= bit << shift
            shift += 1

            if shift == 8:
                yield acc
                shift = 0
                acc = 0

        if shift != 0:
            yield acc
