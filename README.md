# **RISC-V Instruction Set Simulator**

## **Overview**
The RISC-V Instruction Set Simulator is a Python-based tool designed to decode, disassemble, and simulate a subset of the RISC-V instruction set architecture (ISA). This project helps developers and researchers understand RISC-V instructions by providing a step-by-step disassembly and execution simulation, along with comprehensive logs.

---

## **Features**
1. **Instruction Decoding and Disassembly**:
   - Supports key RISC-V instructions including branching (`beq`, `bne`, `blt`), arithmetic (`add`, `sub`, `and`, `or`), and memory operations (`lw`, `sw`).
   - Handles two's complement calculations for signed immediate values.
   - Converts binary instructions into human-readable assembly code.

2. **Pipeline Simulation**:
   - Implements stages of instruction execution: fetch, decode, execute, memory, and write-back.
   - Simulates a cycle-accurate pipeline for instruction execution.

3. **Memory and Register Management**:
   - Maintains a 32-register array and memory-mapped addresses for simulation.
   - Supports memory instructions with proper address calculations and updates.

4. **Logging**:
   - Outputs **disassembly logs** with memory addresses and instructions.
   - Generates **cycle-by-cycle simulation logs** showing register and memory updates.

---

## **How to Use**

### **Pre-requisites**
   - Python 3.x installed on your system.

### **Steps to Run**
   1. Place the RISC-V binary input file in the same directory as the script.
   2. Run the following command in the terminal:
      ```bash
      python vsim.py <input_file>
      ```
   3. Replace `<input_file>` with the name of your RISC-V binary input file (e.g., `input.txt`).

### **File Outputs**
   - **disassembly.txt**: Disassembled instructions with memory addresses.
   - **simulation.txt**: Cycle-by-cycle execution logs, including register and memory states.

---

## **Example**

### **Input Binary File**
00000000000000000000000010000011 00000000010000001000000010110011

markdown
Copy
Edit

### **Generated Disassembly (disassembly.txt)**
00000000000000000000000010000011 256 lw x1, 0(x0) 00000000010000001000000010110011 260 add x1, x2, x0

markdown
Copy
Edit

### **Generated Simulation Log (simulation.txt)**
Cycle 1: IF Unit: Waiting: Executed: [lw x1, 0(x0)]

Registers: x00: 0 0 0 0 0 0 0 0 x08: 0 0 0 0 0 0 0 0 ...

yaml
Copy
Edit

---

## **Code Highlights**
1. **Instruction Decoding**:
   - Functions like `getcode` extract binary fields for opcodes, registers, and immediate values.
   - `twoscomp` calculates two's complement for signed immediate values.

2. **Branching**:
   - Implements branching logic (`beq`, `bne`, `blt`) to update the program counter.

3. **Memory Operations**:
   - Handles `lw` and `sw` instructions, accurately calculating memory addresses and performing read/write operations.

4. **Simulation**:
   - Simulates execution stages (fetch, decode, execute, memory) and maintains a log of all operations.

---

## **Technologies Used**
- **Language**: Python 3.x
- **Data Structures**: Dictionaries, lists, queues for instruction and state management.

---

## **Future Improvements**
- Support additional RISC-V instructions and extensions.
- Add pipeline visualization to show instruction execution stages.
- Implement hazard detection and resolution for better pipeline accuracy.
- Expand functionality to handle floating-point operations.

---

## **Acknowledgments**
This project was developed as a self-initiated learning endeavor to explore the RISC-V instruction set architecture and gain hands-on experience in system simulation and pipeline design.

---
