import ctypes, os, sys

libname = "native.dll" if sys.platform != "android" and sys.platform != "linux" else "libnative.so"
lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), libname))
