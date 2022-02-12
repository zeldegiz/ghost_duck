import numpy as np

def second_step_encryption(keys,data):
    def converter(column):
        first = column[:20]
        second = column[20:32]
        third = column[32:44]
        fourth = column[44:]
        if((second[-1]^third[-1])%2 == 1):
            return np.concatenate((third,first,fourth,second))
        else:
            return np.concatenate((second,first,fourth,third))
    for i in keys:
        data = data ^ i
        data = data.reshape(int(data.size/64),64)
        data = np.apply_along_axis(converter, axis=1, arr=data).ravel()
    return data

def third_step_encryption(key,data):
    i = 0
    def changer(data):
        nonlocal i
        returned = key[i][data]
        i+=1
        return returned
    data = np.apply_along_axis(changer,axis=1,arr=data.reshape(int(data.size/128),128)).ravel()
    return data
    
def fourth_step_encryption(key,data):
    data = data.reshape(int(data.size/8),8)
    return data[key].ravel()
    