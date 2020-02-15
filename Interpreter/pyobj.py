"""Some essential object of interpreter"""

import collections


class Frame(object):
    """

    The frame object that deals with function calls

    """
    def __init__(self, f_code, f_globals, f_locals, f_back):
        self.f_code = f_code
        self.f_globals = f_globals
        self.f_locals = f_locals
        self.f_back = f_back
        self.stack = []
        self.block_stack = []
        self.f_lasti = 0

        # Builtins
        try:
            self.f_builtins = f_globals["__builtins__"]
            if hasattr(self.f_builtins, "__dict__"):
                self.f_builtins = self.f_builtins.__dict__
        except KeyError:
            # No builtins
            self.f_builtins = {"None": None}


"""

    The block object that deals with special statements
    such as if-statement, loops and so on.

"""
Block = collections.namedtuple("Block", "type, handler, level")
