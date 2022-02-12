'''
--- Test Edildi---
Bu modul daxil edilən byte ardıcıllığına uyğun , numpy array 
və ya tərsinə daxil edilən numpy array-a uyğun byte ardıcıllığı qaytarır
'''
import numpy as np

def bytes_to_arr(_bytes):
    return np.array(list(_bytes) , dtype=np.uint8)
    
def arr_to_bytes(_arr):
    return bytes(list(_arr))

def length_1024(_arr):
    size = np.array(list((_arr.size).to_bytes(16, byteorder='big')), dtype=np.uint8)
    random = np.random.randint(256, size=(128-(_arr.size+16)%128) , dtype=np.uint8)
    return np.concatenate((_arr,random,size))
    
def shorter(_arr):
    size = int.from_bytes(bytes(list(_arr[-16:])), "big")
    return _arr[:size]