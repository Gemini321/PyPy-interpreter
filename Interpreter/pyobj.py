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
        pass


"""

    The block object that deals with special statements
    such as if-statement, loops and so on.

"""
Block = collections.namedtuple("Block", "type, handler, level")
