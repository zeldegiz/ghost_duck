'''
Bu modul ilə istifadəçi tərəfindən daxil edilən açar lazimi uzunluqlu açarlara çevrilir
'''
import numpy as np

# Baza açarı generasiya etmək üçün istifadə olunan metoddur , numpy array alır
def base_key_2048(_arr):
    bits = (((_arr[:,None] & (1 << np.arange(8)))) > 0).astype(np.bool_).ravel()
    if(bits.size == 2048):
        return bits
    elif(bits.size > 2048):
        while(bits.size != 2048):
            bits[-2049:-1] = bits[-2049:-1]^bits[-2048:]
            bits = bits[:-1]
        return bits
    else:
        while(bits.size != 2048):
            bits = np.append(bits,bits[-1])
            bits[1:] = bits[1:]^bits[:-1]
        return bits

# İkinci addım üçün 320 bitlik açarlar generasiya edir
def second_step_base_key_320x8(base_key_2048):
    keys = np.array([] , dtype=np.bool_)
    exponential_2 = 2 ** np.arange(8)
    for i in range(8):
        p1 = np.sum(base_key_2048[:10] * 2 ** np.arange(10)[::-1])
        p2 = np.sum(base_key_2048[p1:p1+10] * 2 ** np.arange(10)[::-1])
        keys = np.append(keys,np.append(base_key_2048[p1:p1+160],[base_key_2048[p2:p2+160]]))
        base_key_2048 = np.roll(base_key_2048,p1+p2)
    z = []
    for i in keys.reshape(320,8):
        z.append(np.sum(i * exponential_2))
    return np.array(z).reshape(8,40).astype(np.uint8)
# İkinci Addım üçün 8 iterasiyanın hər biri üçün 40*n (number_of_block) qədər byte generasiya edilir
def second_step_blocks_keys(second_step_base,number_of_block):
    blocks = np.arange(0,number_of_block).astype(np.uint8)
    r = []
    for i in second_step_base.T:
        r.append(np.sum(i))
    for i in r:
        blocks[:number_of_block] = np.roll(blocks[:number_of_block],i)
        blocks[number_of_block:] = np.roll(blocks[number_of_block:],i)
    result = (second_step_base.reshape(second_step_base.size,1)*blocks%256).T.reshape(8,40*number_of_block).astype(np.uint8)
    d = np.array([]).astype(np.uint8)
    zeros = np.zeros(number_of_block*24).reshape(number_of_block,24).astype(np.uint8)
    for i in result:
        k = i.reshape(number_of_block,40)
        z = np.concatenate((k[:,:20],zeros,k[:,20:]),axis=1)
        d = np.append(d,z.reshape(1,z.size))
    return d.reshape(8,int(d.size/8))
# Üçüncü Addım üçün Əvəzedici Bloklar Generasiya edir
def third_step_base_key(base_key_2048,number_of_block):
    exponential_2 = 2 ** np.arange(8)
    base_key_2048 =  np.apply_along_axis(lambda x: np.sum(exponential_2*x), axis=1, arr=base_key_2048.reshape(int(base_key_2048.size/8),8)).ravel()
    block_keys = np.ones(number_of_block).reshape(number_of_block,1)*np.arange(256).reshape(1,256)
    def shifter(shifted_column):
        nonlocal base_key_2048
        shifted_column = np.roll(shifted_column,base_key_2048[0])
        shifted_column[:128] = np.roll(shifted_column[:128],base_key_2048[1])
        shifted_column[128:] = np.roll(shifted_column[128:],-base_key_2048[2])
        shifted_column[64:192] = np.roll(shifted_column[64:192],base_key_2048[4])
        base_key_2048 = np.roll(base_key_2048,5)
        return shifted_column
    return np.apply_along_axis(shifter,axis=1,arr=block_keys).astype(np.uint8)
# Dorduncu Addim Map Generasiyasi
def fourth_step_base(base_key_2048,number_of_block):
    exponential_2 = 2 ** np.arange(8)
    base_key_2048 =  np.apply_along_axis(lambda x: np.sum(exponential_2*x), axis=1, arr=base_key_2048.reshape(int(base_key_2048.size/8),8)).ravel()
    keys = np.arange(number_of_block)
    q1 = int(number_of_block/4)
    q3 = int(number_of_block/4)*3
    for i in base_key_2048:
        keys[:q1] = np.roll(keys[:q1],-i)
        keys[q3:] = np.roll(keys[q3:],i)
        keys = np.roll(keys,i)
    return keys
            
