import converter
import decryptor
import key_gen

file_name = input('Please Enter File Name : ')
password = input('Please Enter Password : ')

with open(file_name,'rb') as f:
    r = f.read()
    
bytes_arr = converter.bytes_to_arr(r)

base_pass = password.encode('utf-8')
base_pass = converter.bytes_to_arr(base_pass)
base_pass = key_gen.base_key_2048(base_pass)
second_step_base_keys = key_gen.second_step_base_key_320x8(base_pass)
second_step_block_keys = key_gen.second_step_blocks_keys(second_step_base_keys,int(bytes_arr.size/64))
third_step_keys = key_gen.third_step_base_key(base_pass,int(bytes_arr.size/128))
fourth_step_key = key_gen.fourth_step_base(base_pass,int(bytes_arr.size/8))

# fourth key decrypter
third_step_encrypted = decryptor.fourth_step_decryption(fourth_step_key,bytes_arr)

# third step decrypter
second_step_decrypted = decryptor.third_step_decryption(third_step_keys,third_step_encrypted)

# second step decrypter
plain_data = decryptor.second_step_decryptor(second_step_block_keys,second_step_decrypted)

# short data
short_arr = converter.shorter(plain_data)

output_name = input('Please Enter Output File Name : ')
output = converter.arr_to_bytes(short_arr)

with open(output_name,'wb') as f:
    f.write(output)