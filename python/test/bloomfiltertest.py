# python3.5
# -*- coding = 'utf-8' -*-
#
# bloom filter test
import hashlib
import time
size = 100000000
bloom_map = '0' * size

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

@check_str
def is_inbmap(str):
    global bloom_map
    h1 = hash1(str)
    h2 = hash2(str)
    h3 = hash3(str)
    h4 = hash4(str)    
    if int(bloom_map[h1]) * int(bloom_map[h2]) * int(bloom_map[h3]) * int(bloom_map[h4]) == 0:
        bloom_map = bloom_map[:h1] + '1' + bloom_map[h1+1:]
        bloom_map = bloom_map[:h2] + '1' + bloom_map[h2+1:]
        bloom_map = bloom_map[:h3] + '1' + bloom_map[h3+1:]
        bloom_map = bloom_map[:h4] + '1' + bloom_map[h4+1:]
        return(False)
    else:
        return(True)

print(hash1('feoifjwejf'))
print(hash1(123123))
print(is_inbmap('ejfowifefefoiwjef'))
print(is_inbmap('ejfowijefdsfoiwjef'))
print(is_inbmap('ejfowijesdfsdfoiwjef'))
print(is_inbmap('ejfowijeffoiwjef'))
print(is_inbmap('ejfowijsdfweefoiwjef'))
print(is_inbmap('ejfowifefefoiwjef'))
