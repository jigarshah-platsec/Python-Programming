class Solution(object):

    def countBits(self, value):
        count = 0
        while value != 0:
            if value & 1:
                count = count + 1
            value = value >> 1
        return count

    def setBit(self, value, bitNum):
        value = value | (1 << bitNum)
        return value

    def resetBit(self, value, bitNum):
        value = value & ~(1 << bitNum)
        return value

    def flipBit(self, value, bitNum):
        if value & (1 << bitNum):
            result = self.resetBit(value, bitNum)
        else:
            result = self.setBit(value, bitNum)
        return result

    def findOddOccuringNumber(self, array):
        result = 0
        for num in array:
            result = result ^ num
        return result

    def find2OddOccuringNumber(self, array):
        result = 0
        for num in array:
            result = result ^ num
        return result

    def powerSet(self, array):
        powerSetSize = pow(2, len(array))
        print(powerSetSize)
        powerSet = []
        for counter in range(powerSetSize):
            subset = []
            for bitPosition in range(len(array)):
                if counter & (1 << bitPosition):
                    subset.append(array[bitPosition])
            powerSet.append(subset)
        return powerSet

s = Solution()
print(s.countBits(5))
print(s.countBits(7))
print(s.countBits(8))
print(s.flipBit(5, 1))
print(s.findOddOccuringNumber([12, 12, 14, 90, 14, 14, 14]))


"""
https://www.geeksforgeeks.org/?p=588
"""
QueSet = ['a', 'b', 'c']
print(s.powerSet(QueSet))