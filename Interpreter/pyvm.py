"""The Virtual Machine of the interpreter"""

"""Acknowledgement: methods of parse_bytes_and__args, dispatch, operatiors and some details
are adopted from Byterun, Allison Kaptur and Ned Batchelder, licensed by MIT License"""

class VirtualMachineError(Exception):
    """For raising errors in the operation of the VM"""
    pass

class VirtualMachine(object):
    def __init__(self):
        # The call stack of frames
        self.frames = []
        # The current frame
        self.frame = None

    def make_frame(self, code, callargs={}, global_names=None, local_names=None):
        """Focus on the global_names and local_names"""
        pass

    def run_frame(self, frame):
        pass

    def parse_bytes_and__args(self):
        pass

    def dispatch(self, byteName, arguments):
        pass

    def run_code(self, code, global_names=None, local_names=None):
        """Run the code and check if there any frame left after the code runs"""
        pass

    # The following methods consist of frame manipulation and data stack manipulation

    # basic manipulation

    def top(self):
        """Return the value at the top of the stack"""
        pass

    def pop(self, i=0):
        """Pop the ith value of the stack"""
        pass

    def popn(self, n):
        """Pop the top n values of the stack. Deepest first"""
        pass

    def push(self, *vals):
        """Push values into stack"""
        pass

    def peek(self, n):
        """Get the nth entry from the bottom of the stack"""
        pass

    def jump(self, jump):
        """Move the bytecode pointer to 'jump'"""
        pass

    # Stack manipulation

    def byte_LOAD_CONST(self, const): #
        pass

    def byte_POP_TOP(self):
        pass

    def byte_DUP_TOP(self):
        """Copy the top entry of the stack and push it into the stack"""
        pass

    def byte_DUP_TOPX(self, count):
        """Copy the top count entries of the stack and push them into the stack with the same order"""
        pass

    def byte_DUP_TOP_TWO(self):
        pass

    def byte_ROT_TWO(self):
        """Insert the top entry to the second place"""
        pass

    def byte_ROT_THREE(self):
        """Insert the top entry to the third place"""
        pass

    def byte_ROT_FOUR(self):
        """Insert the top entry to the fourth place"""
        pass

    # Names

    def byte_LOAD_NAME(self, name): #
        pass

    def byte_STORE_NAME(self, name): #
        pass

    def byte_DELETE_NAME(self, name):
        pass

    def byte_LOAD_FAST(self, name): #
        pass

    def byte_STORE_FAST(self, name): #
        pass

    def byte_DELETE_FAST(self, name):
        pass

    def byte_LOAD_GLOBAL(self, name):
        pass

    def byte_STORE_GLOBAL(self, name):
        pass

    def byte_LOAD_DEREF(self, name):
        pass

    def byte_STORE_DEREF(self, name):
        pass

    def byte_LOAD_LOCALS(self):
        pass

    # Operatiors(basically adopted from Byterun)

    UNARY_OPERATORS = {
        'POSITIVE': operator.pos,
        'NEGATIVE': operator.neg,
        'NOT':      operator.not_,
        'CONVERT':  repr,
        'INVEERT':  opeartor.invert,
    }

    def unaryOperator(self, op):
        x = self.pop()
        self.push(self.UNARY_OPERATORS[op](x))

    BINARY_OPERATORS = {
        'POWER':    pow,
        'MULTIPLY': operator.mul,
        'DIVIDE': getattr(operator, 'div', lambda x, y: None),
        'FLOOR_DIVIDE': operator.floordiv,
        'TRUE_DIVIDE':  operator.truediv,
        'MODULO':   operator.mod,
        'ADD':      operator.add,
        'SUBTRACT': operator.sub,
        'SUBSCR':   operator.getitem,
        'LSHIFT':   operator.lshift,
        'RSHIFT':   operator.rshift,
        'AND':      operator.and_,
        'XOR':      operator.xor,
        'OR':       operator.or_,
    }

    def biniaryOperator(self, op):
        x, y = self.popn(2)
        self.push(self.BINARY_OPERATORS[op](x, y))

    def inplaceOperator(self, op):
        x, y = self.popn(2)
        # Match op and its operator
        if op == 'POWER':
            x **= y
        elif op == 'MULTIPLY':
            x *= y
        elif op in ['DIVIDE', 'FLOOR_DIVIDE']:
            x //= y
        elif op == 'TRUE_DIVIDE':
            x /= y
        elif op == 'MODULO':
            x %= y
        elif op == 'ADD':
            x += y
        elif op == 'SUBTRACT':
            x -= y
        elif op == 'LSHIFT':
            x <<= y
        elif op == 'RSHIFT':
            x >>= y
        elif op == 'AND':
            x &= y
        elif op == 'XOR':
            x ^= y
        elif op == 'OR':
            x |= y
        else:           # pragma: cound not match
            raise VirtualMachineError("Unknown in-place operator: %r" % op)
        self.push(x)

    def sliceOperator(self, op):
        pass

    COMPARE_OPERATORS = [
        operator.lt,
        operator.le,
        operator.eq,
        operator.ne,
        operator.gt,
        operator.ge,
        lambda x, y: x in y,
        lambda x, y: x not in y,
        lambda x, y: x is y,
        lambda x, y: x is not y,
        lambda x, y: issubclass(x, Exception) and issubclass(x, y),
    ]

    def byte_COMPARE_OP(self, opnum):
        x, y = self.popn(2)
        self.push(self.COMPARE_OPERATORS[opnum](x, y))

    # Attributes and indexing

    def byte_LOAD_ATTR(self, attr):
        pass

    def byte_STORE_ATTR(self, name):
        pass

    def byte_DELETE_ATTR(self, name):
        pass

    def byte_STORE_SUBSCR(self):
        pass

    def byte_DELETE_SUBSCR(self):
        pass

    # Building

    def byte_BUILD_TUPLE(self, count):
        """Using the top 'count' data to build a tuple"""
        pass

    def byte_BUILD_LIST(self, count):
        """Using the top 'count' data to build a list"""
        pass

    def byte_BUILD_SET(self, count):
        """Using the top 'count' data to build a set"""
        pass

    def byte_BUILD_MAP(self, size):
        """Build an empty map, size is ignored"""
        pass

    def byte_STORE_MAP(self):
        """While the map is on the top of stack, pop it and add
        a pair of key and value"""
        pass

    def byte_UNPACK_SEQUENCE(self, count):
        """Unpack a sequence from the stack top, and push all the entries into the stack"""
        pass

    def byte_BUILD_SLICE(self, count):
        """Build a slice with 'count' number of entries"""
        pass

    def byte_LIST_APPEND(self, count):
        """Append the value at the top of the stack to a list from self.peek(count)"""
        pass

    def byte_SET_ADD(self, count):
        """Add the value at the top of the stack to a set from self.peek(count)"""
        pass

    def byte_MAP_ADD(self, count):
        """Add the value at the top of the stack to a map from self.peek(count)"""
        pass

    # Jumps

    def byte_JUMP_FORWARD(self, jump):
        self.jump(jump)

    def byte_JUMP_ABSOLUTE(self, jump):
        self.jump(jump)

    def byte_POP_JUMP_IF_TRUE(self, jump):
        """If the value at the top of the stack is true, jump to 'jump'"""
        pass

    def byte_POP_JUMP_IF_FALSE(self, jump):
        pass

    def byte_JUMP_IF_TRUE_OR_POP(self, jump):
        """If the value at the top of the stack is true, jump; Or pop it"""
        pass

    def byte_JUMP_IF_FALSE_OR_POP(self, jump):
        pass

    # Blocks

    def byte_SETUP_LOOP(self, dest):
        """Setup the state of loop, including the dest of this loop"""
        pass

    def byte_GET_ITER(self):
        """Make the top value as a lterator"""
        pass

    def byte_FOR_ITER(self, jump):
        """Get the next entry of a lterator and push it into the stack(if possible)"""
        pass

    def byte_BREAK_LOOP(self):
        return 'break'

    def byte_CONTINUE_LOOP(self, dest):
        self.return_value = dest
        return 'continue'

    def byte_SETUP_EXCEPT(self, dest):
        pass

    def byte_SETUP_FINALLY(self, dest):
        pass

    def byte_END_FINALLY(self):
        pass

    def byte_POP_BLOCK(self):
        pass

    # Raise

    def byte_RAISE_VARARGS(self, argc):
        """Raise with varargs"""
        pass

    def do_raise(self, exc, cause):
        pass

    def byte_POP_EXCEPT(self):
        pass

    # Functions(left out)
