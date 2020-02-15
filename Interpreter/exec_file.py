"""The executive file of PyPy interpreter."""

from .pyvm import VirtualMachine, VirtualMachineError
from .pyobj import Frame, Block
import sys


def run_python_file(code):
    vm = VirtualMachine()
    vm.run_code(code)


def get_code_object():
    filename = sys.argv[1]
    try:
        fp = open(filename, "r")
        code = compile(fp, filename, "exec")
        return code
    except IOError:
        raise IOError("File opening fails.")


def get_start():
    code = get_code_object()
    run_python_file(code)
