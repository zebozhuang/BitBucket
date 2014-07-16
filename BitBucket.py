#!/usr/bin/env python
#-*- coding:utf-8 -*-

SHIFT = 5  # 如果计算机为32位,SHIFT为5;如果计算机为64位,SHIFT为6
MASK = 0x1F  # 如果计算机为32位,MASK为0x1F;如果计算机为64位,MASK为0x3F

class BitBucket(object):
    def __init__(self):
        self._unique_key_count = 0   # 唯一的key有多少个
        self._total_key_count = 0    # 加入的key有多少个
        self._bit = {}
        self._map = {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f':'6'}

    def set(self, value):
        """return last bit"""
        value = self._translate(value)
        self._total_key_count += 1

        if not self._has_key(value):
            self._unique_key_count += 1
            key = value >> SHIFT
            self._bit[key] = self._bit.get(key, 0) | (1 << (value & MASK))
            return 0
        return 1

    def exist(self, value):
        value = self._translate(value)
        if self._has_key(value):
            return True
        return False

    def clear(self, value):
        value = self._translate(value)
        if self._has_key(value):
            self._unique_key_count -= 1
            self._total_key_count -= 1

            key = value >> SHIFT
            self._bit[key] = self._bit[key] & (~(1 << (value & MASK)))
            return True
        return False

    def get_total_count(self):
        return self._total_key_count

    def get_bit_count(self):
        return self._unique_key_count

    def _has_key(self, value):
        key = value >> SHIFT
        return self._bit.get(key, 0) & (1 << (value & MASK))

    def _translate(self, value):
        value = value.lower()
        return long(''.join([self._map.get(c, c) for c in value]))

if __name__ == '__main__':
    bitBucket = BitBucket()
    bitBucket.set("a"*40)
    print bitBucket.exist("a" * 40)
    print bitBucket.exist("b" * 40)
   
    bitBucket.clear("a" * 40)

    import hashlib

    for i in range(1, 27):
        a = chr(i)
        sha1 = hashlib.sha1()
        sha1.update(a)
        bitBucket.set(sha1.hexdigest())

    print bitBucket.get_total_count() 
    print bitBucket.get_bit_count()

    count = 0
    for i in range(1, 30):
        a = chr(i)
        sha1 = hashlib.sha1()
        sha1.update(a)
        if bitBucket.exist(sha1.hexdigest()):
            count += 1

    assert count == bitBucket.get_bit_count()
