import ctypes, os, sys

libname = "native.dll" if sys.platform == "win32" else "libnative.so"
lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), libname))

lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int

lib.greet.argtypes = [ctypes.c_char_p]
lib.greet.restype = ctypes.c_char_p

assert lib.add(2, 3) == 5
assert lib.greet(b"hello") == b"Hello, hello"
assert lib.greet(b"world") == b"Hello, world"

print("OK")
