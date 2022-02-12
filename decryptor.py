import numpy as np
import pandas as pd

def second_step_decryptor(keys,data):
    keys = keys[::-1]
    def converter(column):
        first = column[:12]
        second = column[12:32]
        third = column[32:52]
        fourth = column[52:]
        if((first[-1]^fourth[-1])%2 == 1):
            return np.concatenate((second,fourth,first,third))
        else:
            return np.concatenate((second,first,fourth,third))
    for i in keys:
        data = data.reshape(int(data.size/64),64)
        data = np.apply_along_axis(converter, axis=1, arr=data).ravel()
        data = data ^ i
    return data
    
def third_step_decryption(keys,data):
    def changekeys(key):
        a = np.arange(256).astype(np.uint8)
        x = np.vstack((key, a)).T
        x = x[np.argsort(x[:, 0])]
        return x[:,1]
    key = np.apply_along_axis(changekeys, axis=1, arr=keys)
    i = 0
    def changer(data):
        nonlocal i
        returned = key[i][data]
        i+=1
        return returned
    data = np.apply_along_axis(changer,axis=1,arr=data.reshape(int(data.size/128),128)).ravel()
    return data
    
def fourth_step_decryption(keys,data):
    a = np.arange(keys.size)
    x = np.vstack((keys, a)).T
    x = x[np.argsort(x[:, 0])]
    keys = x[:,1]
    data = data.reshape(int(data.size/8),8)
    return data[keys].ravel()