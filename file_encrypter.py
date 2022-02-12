import converter
import encryptor
import key_gen

file_name = input('Please Enter File Name : ')
password = input('Please Enter Password : ')

with open(file_name,'rb') as f:
    r = f.read()
    
bytes_arr = converter.bytes_to_arr(r)
bytes_arr = converter.length_1024(bytes_arr)

base_pass = password.encode('utf-8')
base_pass = converter.bytes_to_arr(base_pass)
base_pass = key_gen.base_key_2048(base_pass)
second_step_base_keys = key_gen.second_step_base_key_320x8(base_pass)
second_step_block_keys = key_gen.second_step_blocks_keys(second_step_base_keys,int(bytes_arr.size/64))
third_step_keys = key_gen.third_step_base_key(base_pass,int(bytes_arr.size/128))
fourth_step_key = key_gen.fourth_step_base(base_pass,int(bytes_arr.size/8))

# second step encryption
second_step_encrypted = encryptor.second_step_encryption(second_step_block_keys,bytes_arr)

# third step encryption
third_step_encrypted = encryptor.third_step_encryption(third_step_keys,second_step_encrypted)

# fourth step encryption
fourth_step_encrypted = encryptor.fourth_step_encryption(fourth_step_key,third_step_encrypted)


output_name = input('Please Enter Output File Name : ')
output = converter.arr_to_bytes(fourth_step_encrypted)

with open(output_name,'wb') as f:
    f.write(output)