"""The Virtual Machine of the interpreter"""

"""Acknowledgement: methods of parse_bytes_and__args, dispatch, operatiors and some details
are adopted from Byterun, Allison Kaptur and Ned Batchelder, licensed by MIT License"""

from __future__ import print_function, division
import dis
import linecache
import logging
import operator
import sys


class VirtualMachineError(Exception):
    """For raising errors in the operation of the VirtualMachine"""
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

    def parse_byte_and_args(self):
        """ Parse 1 - 3 bytes of bytecode into
        an instruction and optionally arguments."""
        f = self.frame
        opoffset = f.f_lasti
        byteCode = byteint(f.f_code.co_code[opoffset])
        f.f_lasti += 1
        byteName = dis.opname[byteCode]
        arg = None
        arguments = []
        if byteCode >= dis.HAVE_ARGUMENT:
            arg = f.f_code.co_code[f.f_lasti:f.f_lasti+2]
            f.f_lasti += 2
            intArg = byteint(arg[0]) + (byteint(arg[1]) << 8)
            if byteCode in dis.hasconst:
                arg = f.f_code.co_consts[intArg]
            elif byteCode in dis.hasfree:
                if intArg < len(f.f_code.co_cellvars):
                    arg = f.f_code.co_cellvars[intArg]
                else:
                    var_idx = intArg - len(f.f_code.co_cellvars)
                    arg = f.f_code.co_freevars[var_idx]
            elif byteCode in dis.hasname:
                arg = f.f_code.co_names[intArg]
            elif byteCode in dis.hasjrel:
                arg = f.f_lasti + intArg
            elif byteCode in dis.hasjabs:
                arg = intArg
            elif byteCode in dis.haslocal:
                arg = f.f_code.co_varnames[intArg]
            else:
                arg = intArg
            arguments = [arg]

        return byteName, arguments, opoffset

    def dispatch(self, byteName, arguments):
        """ Dispatch by bytename to the corresponding methods.
        Exceptions are caught and set on the virtual machine."""
        why = None
        try:
            if byteName.startswith('UNARY_'):
                self.unaryOperator(byteName[6:])
            elif byteName.startswith('BINARY_'):
                self.binaryOperator(byteName[7:])
            elif byteName.startswith('INPLACE_'):
                self.inplaceOperator(byteName[8:])
            elif 'SLICE+' in byteName:
                self.sliceOperator(byteName)
            else:
                # dispatch
                bytecode_fn = getattr(self, 'byte_%s' % byteName, None)
                if not bytecode_fn:            # pragma: no cover
                    raise VirtualMachineError(
                        "unknown bytecode type: %s" % byteName
                    )
                why = bytecode_fn(*arguments)

        except:
            # deal with exceptions encountered while executing the op.
            self.last_exception = sys.exc_info()[:2] + (None,)
            log.exception("Caught exception during execution")
            why = 'exception'

        return why

    def run_code(self, code, global_names=None, local_names=None):
        """Run the code and check if there any frame left after the code runs"""
        pass

    # The following methods consist of frame manipulation and data stack manipulation

    # Basic manipulation

    def top(self):
        """Return the value at the top of the stack"""
        return self.frame.stack.top()

    def pop(self, i=0):
        """Pop the ith value of the stack"""
        return self.frame.stack.pop(- i - 1)

    def popn(self, n):
        """Pop the top n values of the stack. Deepest first"""
        values = self.frame.stack[- n:]
        self.frame.stack[- n:] = []
        return values

    def push(self, *vals):
        """Push values into stack"""
        self.frame.stack.extend(list(vals))

    def peek(self, n):
        """Get the nth entry from the bottom of the stack"""
        return self.stack[n]

    def jump(self, jump):
        """Move the bytecode pointer to 'jump'"""
        pass

    # Stack manipulation

    def byte_LOAD_CONST(self, const):
        self.push(const)

    def byte_POP_TOP(self):
        self.pop()

    def byte_DUP_TOP(self):
        """Copy the top entry of the stack and push it into the stack"""
        self.push(self.top())

    def byte_DUP_TOPX(self, count):
        """Copy the top count entries of the stack and push them into the stack with the same order"""
        topx = self.popn(count)
        self.push(*topx)
        self.push(*topx)

    def byte_DUP_TOP_TWO(self):
        self.byte_DUP_TOPX(2)

    def byte_ROT_TWO(self):
        """Insert the top entry to the second place"""
        a, b = self.popn(2)
        self.push(b, a)

    def byte_ROT_THREE(self):
        """Insert the top entry to the third place"""
        a, b, c = self.popn(3)
        self.push(c, a, b)

    def byte_ROT_FOUR(self):
        """Insert the top entry to the fourth place"""
        a, b, c, d = self.popn(4)
        self.push(d, a, b, c)

    # Names

    def byte_LOAD_NAME(self, name):
        """Push the value of the name into stack.
        NameError raises when the name not defined."""
        if name in self.frame.f_locals:
            val = self.frame.f_locals[name]
        elif name in self.frame.f_globals:
            val = self.frame.f_globals[name]
        elif name in self.frame.f_builtins:
            val = self.frame.f_builtins[name]
        else:
            raise NameError("Name '{}' is not defined.".foramt(name))
        self.push(val)

    def byte_STORE_NAME(self, name):
        """Store the name to f_locals and give it a value from the top of stack"""
        self.frame.f_locals[name] = self.pop()

    def byte_DELETE_NAME(self, name):
        """Delete a local name"""
        del self.frame.f_locals[name]

    def byte_LOAD_FAST(self, name):
        """Load value of local variable to stack.
        UnboundLocalError raises when local variable has not been assigned."""
        if name in self.frame.f_locals:
            self.push(self.frame.f_locals[name])
        else:
            raise UnboundLocalError("Local name '{}' referenced\
                but not bound to a value.".format(name))

    def byte_STORE_FAST(self, name):
        """Store name to f_locals and assign it."""
        self.frame.f_locals[name] = self.pop()

    def byte_DELETE_FAST(self, name):
        """Delete this local variable"""
        del self.frame.f_locals[name]

    def byte_LOAD_GLOBAL(self, name):
        """Local a global variable"""
        if name in self.frame.f_globals[name]:
            self.push(self.frame.f_globals[name])

    def byte_STORE_GLOBAL(self, name):
        """Store a global variable"""
        self.frame.f_globals[name] = self.pop()

    def byte_LOAD_DEREF(self, name):
        """Push the value getting from the cell"""
        pass

    def byte_STORE_DEREF(self, name):
        """Store a value pop from stack to cell"""
        pass

    def byte_LOAD_LOCALS(self):
        """Load f_locals"""
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
        start = 0
        end = None
        op, count = op[:-2], int(op[-1])
        if count == 1:
            start = self.pop()
        elif count == 2:
            end = self.pop()
        elif count == 3:
            end = self.pop()
            start = self.pop()
        l = self.pop()
        if end is None:
            end = len(l)
        if op.startswith('STORE_'):
            l[start:end] = self.pop()
        elif op.startswith('DELETE_'):
            del l[start:end]
        else:
            self.push(l[start:end])

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
        """TOS1[TOS] = TOS2"""
        TOS2, TOS1, TOS = self.popn(3)
        TOS1[TOS] = TOS2
        self.push(TOS1)

    def byte_DELETE_SUBSCR(self):
        """delete TOS1[TOS]"""
        TOS1, TOS = self.popn(2)
        del TOS1[TOS]

    # Building

    def byte_BUILD_TUPLE(self, count):
        """Using the top 'count' data to build a tuple"""
        self.push(tuple(self.popn(count)))

    def byte_BUILD_LIST(self, count):
        """Using the top 'count' data to build a list"""
        self.push(list(self.popn(count)))

    def byte_BUILD_SET(self, count):
        """Using the top 'count' data to build a set"""
        self.push(set(self.pop(count)))

    def byte_BUILD_MAP(self, size):
        """Build an empty map, size is ignored"""
        self.push({})

    def byte_STORE_MAP(self):
        """Store a pair of key and value"""
        Map, value, key = self.popn(3)
        Map[key] = value
        self.push(Map)

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
