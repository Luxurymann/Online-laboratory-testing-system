import ctypes
import os
import platform


def _load_libparse():
    if platform.system() == "Windows":
        lib_path = "./libparse.dll"
    else:
        lib_path = "libparse.so"    
        if not os.path.exists(lib_path):
            lib_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "libparse.so"
            )
    
    return ctypes.CDLL(lib_path)


def calc_evaluation(evaluation: str) -> float:
    evaluation = evaluation.replace("**", "^")
    lib = _load_libparse()
    lib.calc_eval.argtypes = [ctypes.c_char_p]
    lib.calc_eval.restype = ctypes.c_double
    return lib.calc_eval(ctypes.c_char_p(evaluation.encode('utf-8')))


__all__ = ["calc_evaluation"]
