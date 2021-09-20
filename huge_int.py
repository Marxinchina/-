"""
实现高精度大数的四则运算
"""
PRECISION = 500


# 首先创建高精度大数类
class HugeInt:
    def __init__(self, s='0', precision=PRECISION):  # 默认数是0
        self.negative = ''
        # self.string = s
        self.nums = [0 for i in range(precision)]
        self.len = len(s)
        if s[0] == '-':
            self.str2huge_int(s[1:])
            self.len -= 1
            self.negative = '' if self.nums == [0 for i in range(precision)] else '-'
            # self.string = s[1:]
        else:
            self.str2huge_int(s)
        self.del_zeros()

    # 去除高位0，如001会变为1
    def del_zeros(self):
        while self.nums[self.len - 1] == 0 and self.len > 1:
            self.len -= 1

    def str2huge_int(self, s):
        n = len(s)
        for i in range(n):
            self.nums[i] = ord(s[n - i - 1]) - ord('0')

    def huge_int2str(self):
        res, length = '', self.len
        for i in range(length):
            res += chr(self.nums[length - i - 1] + ord('0'))
        if self.negative == '-':
            res = '-' + res
        return res

    def __str__(self):
        return self.huge_int2str()

    def __abs__(self):
        res = HugeInt(str(self))
        res.negative = ''
        return res

    # 绝对值比较
    def _abs_cmp(self, other):
        one, other = abs(self), abs(other)
        if one.len > other.len:
            return 1
        elif one.len < other.len:
            return -1
        else:
            length = one.len
            for i in range(length):
                if one.nums[length - i - 1] > other.nums[length - i - 1]:
                    return 1
                elif one.nums[length - i - 1] < other.nums[length - i - 1]:
                    return -1
                else:
                    continue
        return 0

    # 绝对值是否大于
    def _abs_great(self, other):
        if self._abs_cmp(other) > 0:
            return True
        else:
            return False

    # 绝对值是否大于等于
    def _abs_great_equal(self, other):
        if self._abs_cmp(other) >= 0:
            return True
        else:
            return False

    @staticmethod
    def deal(other):
        if type(other) != HugeInt:
            other = HugeInt(other)
        return other

    def __gt__(self, other):
        other = self.deal(other)
        if self.negative == other.negative == '-':
            return not self._abs_great_equal(other)
        elif self.negative == other.negative == '':
            return self._abs_great(other)
        elif other.negative != self.negative == '-':
            return False
        else:
            return True

    def __eq__(self, other):
        other = self.deal(other)
        if self.negative == other.negative and self._abs_cmp(other) == 0:
            return True
        else:
            return False

    def __ge__(self, other):
        return self > other or self == other

    def _abs_operation(self, other, ope='add'):
        other = self.deal(other)
        one, other, res = abs(self), abs(other), HugeInt()
        length = max(one.len, other.len)
        res.len = length


        if ope == 'add':
            for i in range(length):
                res.nums[i] += one.nums[i] + other.nums[i]
                res.nums[i + 1] += res.nums[i] // 10
                res.nums[i] %= 10
            # 控制进位，res本来的长度就有1
            if res.nums[length] > 0:
                res.len += 1
        elif ope == 'sub':
            if one < other:
                one, other = other, one  # 大数在前
            elif one == other:
                return HugeInt()

            for i in range(length):
                res.nums[i] += one.nums[i] - other.nums[i]
                if res.nums[i] < 0:
                    res.nums[i] += 10
                    res.nums[i + 1] -= 1
            res.del_zeros()
        elif ope == 'times':
            res.len = one.len + other.len - 1
            for j in range(other.len):
                for i in range(one.len):
                    res.nums[i + j] += one.nums[i] * other.nums[j]
                    res.nums[i + j + 1] += res.nums[i + j] // 10
                    res.nums[i + j] %= 10
            if res.nums[res.len] > 0:
                res.len += 1
            # res.del_zeros()  # 乘法怎么会有高位0在前
        elif ope == 'floordiv':
            if one < other:
                res.len = 1
                return res
            elif one == other:
                return res + 1
            else:
                le = one.len - other.len
                save = ''
                for i in range(le):
                    divided = other * pow(10, le - 1 - i)
                    inner_count = 0
                    while divided <= one:
                        inner_count += 1
                        one -= divided
                    save += str(inner_count)
                res = HugeInt(save)

        return res

    def _abs_sub(self, other):
        return self._abs_operation(other, 'sub')

    def _abs_mul(self, other):
        return self._abs_operation(other, 'times')

    def _abs_add(self, other):
        return self._abs_operation(other, 'add')

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -(self - other)

    def __rmul__(self, other):
        return self * other

    def __add__(self, other):
        res = None
        if type(other) == HugeInt:
            if self.negative == other.negative:
                res = self._abs_add(other)
                res.negative = self.negative
                return res
            else:
                res = self._abs_sub(other)
                if self.negative == '-':
                    res.negative = '' if abs(res) <= other else '-'
                else:
                    res.negative = '' if abs(res) >= other else '-'
                return res
        else:
            other = HugeInt(str(other))
            return self + other

    def __neg__(self):
        res = HugeInt(str(self))
        res.negative = '-' if self.negative == '' else ''
        return res

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if type(other) == HugeInt:
            res = self._abs_mul(other)
            res.negative = '' if self.negative == other.negative else '-'
            return res
        else:
            other = HugeInt(str(other))
            return self * other

    def __floordiv__(self, other):
        if type(other) == HugeInt:
            res = self._abs_floordiv(other)
            if self.negative != other.negative:
                res.negative = '-'
                res -= 1
            return res
        else:
            other = HugeInt(str(other))
            return self // other

    def __rfloordiv__(self, other):
        if type(other) != HugeInt:
            other = HugeInt(str(other))
        return other // self

    def __rdiv__(self, other):
        if type(other) != HugeInt:
            other = HugeInt(str(other))
        return other / self

    def __rdivmod__(self, other):
        if type(other) != HugeInt:
            other = HugeInt(str(other))
        return divmod(other, self)

    def __mod__(self, other):
        return self - other * (self // other)

    def __truediv__(self, other):
        return self // other

    def __divmod__(self, other):
        return self // other, self % other

    def _abs_floordiv(self, other):
        return self._abs_operation(other, ope='floordiv')


if __name__ == '__main__':
    import random as r

    # a = r.randint(0, 1000000) if r.randint(0, 1) == 0 else -r.randint(0, 1000000)
    # b = r.randint(0, 1000000) if r.randint(0, 1) == 0 else -r.randint(0, 1000000)
    a, b = -1000002, -102
    print('{}//{}={}'.format(a, b, a // b))
    # a, b = '20', '-80'
    a, b = str(a), str(b)
    hi1, hi2 = HugeInt(a), HugeInt(b)
    print('{}//{}={}'.format(hi1, hi2, hi1 // hi2))
    # print(-hi1)

    # print(22 + hi1)
    # print(hi1 + 22)
    # print(22 - hi1)
    # print(hi1 - 22)
    # print(22 * hi1)
    # print(hi1 * -22)

    print(HugeInt('-22') / hi1)
    # hi1 -= 22
    # print(hi1)

    print(HugeInt('0000000'))