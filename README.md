README for RISC-V Instruction Set Simulator
Project Overview
The RISC-V Instruction Set Simulator is a Python-based project designed to parse and simulate a subset of the RISC-V instruction set. It performs disassembly of binary instructions, simulates their execution in a pipeline, and logs results to text files.

Features
Instruction Parsing and Disassembly:

Supports key RISC-V instructions: branching (beq, bne, blt), arithmetic (add, sub, and, or), and memory operations (lw, sw).
Handles two's complement for signed values in immediate fields.
Pipeline Simulation:

Simulates instruction fetch, decode, execution, and memory access stages.
Maintains accurate register states and memory mapping.
Logging:

Outputs human-readable disassembly in disassembly.txt.
Outputs cycle-by-cycle execution logs in simulation.txt.
Getting Started
To run the simulator:

Ensure Python 3.x is installed on your system.
Place the RISC-V binary input file in the same directory.
Run the simulator with:
bash
Copy
Edit
python simulator.py <input_file>
File Outputs
disassembly.txt: Contains disassembled instructions along with their memory addresses.
simulation.txt: Detailed cycle-by-cycle logs including registers, memory, and instruction execution.
Key Code Features
Instruction Decoding:

Uses helper functions like getcode and twoscomp to decode binary fields.
Decodes opcode, registers, and immediate values.
Branching Support:

Implements branching logic (beq, bne, blt) and updates the program counter accordingly.
Memory and Register Management:

Maintains a memory dictionary and a 32-register array for simulation.
Implements memory instructions (lw, sw) with proper address calculations.
Technologies Used
Python 3.x
Data structures: dictionaries, lists, and queues
Future Improvements
Support for additional RISC-V instructions.
Implementation of pipelining and hazard detection.
Visualization of the simulation process.
