# Brief Analysis of Byterun

This is a simple file recording my understanding of the structure and principles of Byterun.
Just for self-learning.

## Components of Byterun

* Virtual Machine: Manage all the objects, control the operations of frames and finish operations of bytecode.
* Frame: Each function call has its own frame. A frame acts like a independent scope and has local_variables
* Block: Record and control loops, try-ifs, with, pop ect. statements
* Function: 
* main:

## Virtual Machine

variables:
  * frames: calling stack
  * frame: current frame
  * return_value
  * last_exception

methods:
  * \_\_init\_\_: Initialize the variables above.
  * make_frame: Set locals, globals, builtins and finally make frame.
  * push_frame: Push a new frame into frames and set the self.frame as frame.
  * pop_frame: Pop a frame from frames and judge if it's empty. Update the self.frame.
  * print_frames: Print the information of each frame in frames.
  * resume_frame: 
  * run_frame: Push and run a frame until it returns. Always try to run the code if there is any.
  * run_code: The beginning of a program. Call make_frame and run_frame and check the frames finally.
  * parse_byte_and_args: Parse the binary code to byteCode and arguments and call the dispatch method.
  * dispatch: Dispatch the byteCode and arguments to the corresponding methods and catch exceptions and return why.
  * log: Record the log for each opcode.

## Frame

The Frame class is mainly used to store the propurties of each example.
Operations are in Virtual Machine.

variables:  
  * f_code: the code to be executed
  * f_locals: local variables belonging to this frame
  * f_globals: global variables
  * f_back: last frame
  * f_builtins: builtins
  * stack: data stack
  * f_lineno: the first line in Python source code
  * f_lasti: bytecode pointer
  * f_back.cells: cells
  * block_stack

methods:
  * \_\_init\_\_: Initialize code, globals and locals, back, block_stack, cell, builtins.
  * \_\_repr\_\_: Rewrite the introduction of Frame
  * line_number: Get the current line number the frame is executing

## Block

Block = collections.namedtuple("Block", "type, handler, level")

The block is not created as a class separately. Like the data stack, block stack
is also an essential part of a frame.The corresponding methods are in Virtual Machine.

variables:
  * type:
  * handler
  * level

methods:
  * push_block: Push a block into the block stack.
  * pop_block: Pop a block from the block stack.
  * unwind_block
  * manage_block_stack
  * byte_SETUP_LOOP: self.push_block('loop', dest)
  * byte_GET_ITER: self.push(iter(self.pop()))
