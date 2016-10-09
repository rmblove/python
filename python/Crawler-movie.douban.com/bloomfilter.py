# python3.5
# -*- coding = 'utf-8' -*-
# version = 1.0
# bloom filter 
import hashlib
import time
size = 100000000

def check_str(func):
    def wrapper(arg):
        if isinstance(arg, type('basestring')):
            return func(arg)
        print("you should put in a string type arg*")
        return
    return wrapper

@check_str
def hash1(str):
    result = hashlib.new('md5')
    result.update(str.encode('utf-8'))
    return int(result.hexdigest(), 16) % size
    pass

@check_str
def hash2(str):
    result = hashlib.new('sha1')
    result.update(str.encode('utf-8'))
    return int(result.hexdigest(), 16) % size
    pass

@check_str
def hash3(str):
    result = hashlib.new('md5')
    result.update(str.encode('utf-8'))
    result.update('a little bit salt'.encode('utf-8'))#加盐
    return int(result.hexdigest(), 16) % size
    pass

@check_str
def hash4(str):
    result = hashlib.new('sha1')
    result.update(str.encode('utf-8'))
    result.update('a little bit salt'.encode('utf-8'))
    return int(result.hexdigest(), 16) % size
    pass

class BloomFilter:
    def __init__(self, s = 100000000):
        self.size = s
        self.bloom_map = [0] * size
    
    def checkin(self, str):
        h1 = hash1(str)
        h2 = hash2(str)
        h3 = hash3(str)
        h4 = hash4(str)    
        if self.bloom_map[h1] * self.bloom_map[h2] * self.bloom_map[h3] * self.bloom_map[h4] == 0:
            self.bloom_map[h1] = 1
            self.bloom_map[h2] = 1
            self.bloom_map[h3] = 1
            self.bloom_map[h4] = 1
            return(False)
        else:
            return(True)
    
    def check(self, str): 
        h1 = hash1(str)
        h2 = hash2(str)
        h3 = hash3(str)
        h4 = hash4(str)    
        if self.bloom_map[h1] * self.bloom_map[h2] * self.bloom_map[h3] * self.bloom_map[h4] == 0:
            return(False)
        else:
            return(True)
        
    def clear(self):
        self.bloom_map = '0' * self.size


