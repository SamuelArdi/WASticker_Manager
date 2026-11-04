import ctypes, os, sys

def _lib_name() -> str:
  if sys.platform == "win32":
    return "native.dll"
  if sys.platform == "darwin":
    return "libnative.dylib"
  return "libnative.so"

try:
  lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), _lib_name()))
except OSError as exc:
  lib = None
  print(f"[backend] native library unavailable: {exc}")
