import sys
import ctypes

lib = ctypes.CDLL("./libsample.so")

lib.EncryptRC4.restype = ctypes.c_char_p
lib.EncryptRC4.argtypes = (ctypes.c_char_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint)

key_str = b"abcdefghijklmnop"
key_str_len = 16
in_str = b"test_abc"
in_str_len = 8
enc_str = ctypes.create_string_buffer(200)
enc_str_len = 200
dec_str = ctypes.create_string_buffer(200)
dec_str_len = 200

lib.EncryptRC4(key_str, key_str_len, in_str, in_str_len, enc_str, enc_str_len)
lib.DecryptRC4(key_str, key_str_len, enc_str, enc_str_len, dec_str, dec_str_len)

print(dec_str.value)