import sys
from collections import deque


def getcode(zerosones, start, length=5):
    return zerosones.strip()[start:(start+length)]


def twoscomp(zerosones):
    flip = ""
    comp = []
    add1 = True
    for zeroone in zerosones:
        if zeroone == "0":
            flip += "1"
        elif zeroone == "1":
            flip += "0"

    for i in reversed(flip):
        if add1 == False:
            comp.append(i)
        elif i == "1":
            comp.append("0")
        elif i == "0":
            comp.append("1")
            add1 = False
    return ''.join(reversed(comp))


def getaddress(add, SimulatorHelper):
    # print(f'{add, SimulatorHelper} \n')
    if SimulatorHelper[add][0] == 'beq':
        imm = SimulatorHelper[add][3]
        if SimulatorHelper[add][4] == 1:
            imm = (-1)*imm
        if register[SimulatorHelper[add][1]] == register[SimulatorHelper[add][2]]:
            imm = imm << 1
            add += imm
            return add
        else:
            add = add + 4
            return add

    elif SimulatorHelper[add][0] == 'bne':

        imm = SimulatorHelper[add][3]
        if SimulatorHelper[add][4] == 1:
            imm = (-1)*imm
        if register[SimulatorHelper[add][1]] != register[SimulatorHelper[add][2]]:
            imm = imm << 1
            add += imm
            return add
        else:
            add = add + 4
            return add

    elif SimulatorHelper[add][0] == 'blt':

        imm = SimulatorHelper[add][3]
        if SimulatorHelper[add][4] == 1:
            imm = (-1)*imm
        if register[SimulatorHelper[add][1]] < register[SimulatorHelper[add][2]]:
            imm = imm << 1
            add += imm

            return add
        else:
            add = add + 4
            return add

    elif (SimulatorHelper[add][0] == 'jal'):
        jimm = SimulatorHelper[add][3]
        check = SimulatorHelper[add][1]
        register[SimulatorHelper[add][2]] = add + 4
        a = add + 4
        b = SimulatorHelper[add][2]
        if check == 1:
            jimm = jimm * (-1)
        add = add + (jimm << 1)

        return add, a, b


def Simulator(ifile, disfile, simfile):
    add = 256
    breakpoint = False
    addressreg = []
    valuemem = []
    memory = {}
    SimulatorHelper = {}
    instructions = deque([])
    s = ""
    change = 0
    change2 = 0
    for line in ifile:
        lin = line.strip()
        if breakpoint == False:
            LSB = line.strip()[-2:]
            if LSB == "00":
                opcode = getcode(line, -7)
                imm1 = getcode(line, -12)
                reg1 = getcode(line, -20)
                reg2 = getcode(line, -25)
                imm = getcode(line, 0, 7) + imm1

                if opcode == "00000":  # for BEQ
                    if imm[0] == '0':
                        s = f'beq x{int(reg1,2)}, x{int(reg2,2)}, #{int(imm,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = ['beq', int(
                            reg1, 2), int(reg2, 2), int(imm, 2), 0, 1, s]
                        instructions.append(s)
                    else:
                        a = twoscomp(imm)
                        s = f'beq x{int(reg1,2)}, x{int(reg2,2)}, #-{int(a,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = ['beq', int(
                            reg1, 2), int(reg2, 2), int(a, 2), 1, 1, s]
                        instructions.append(s)
                if opcode == "00001":  # for BNE
                    if imm[0] == '0':
                        s = f'bne x{int(reg1,2)}, x{int(reg2,2)}, #{int(imm,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = ['bne', int(
                            reg1, 2), int(reg2, 2), int(imm, 2), 0, 1, s]
                        instructions.append(s)
                    else:
                        a = twoscomp(imm)
                        s = f'bne x{int(reg1,2)}, x{int(reg2,2)}, #-{int(a,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = ['bne', int(
                            reg1, 2), int(reg2, 2), int(a, 2), 1, 1, s]
                        instructions.append(s)
                if opcode == "00010":  # for BLT
                    if imm[0] == '0':
                        s = f'blt x{int(reg1,2)}, x{int(reg2,2)}, #{int(imm,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = ['blt', int(
                            reg1, 2), int(reg2, 2), int(imm, 2), 0, 1, s]
                        instructions.append(s)
                    else:
                        a = twoscomp(imm)
                        s = f'blt x{int(reg1,2)}, x{int(reg2,2)}, #-{int(a,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = ['blt', int(
                            reg1, 2), int(reg2, 2), int(a, 2), 1, 1, s]
                        instructions.append(s)
                if opcode == "00011":  # for SW
                    s = f'sw x{int(reg1,2)}, {int(imm,2)}(x{int(reg2,2)})'
                    disfile.write(f'{lin}\t{add}\t{s}\n')
                    SimulatorHelper[add] = [
                        'sw', int(reg1, 2), int(reg2, 2), int(imm, 2), 0, s]
                    instructions.append(s)
            if LSB == "01":
                opcode = getcode(line, -7)
                regD = getcode(line, -12)
                reg1 = getcode(line, -20)
                reg2 = getcode(line, -25)

                if opcode == "00000":  # for ADD
                    s = f'add x{int(regD,2)}, x{int(reg1,2)}, x{int(reg2,2)}'
                    disfile.write(f'{lin}\t{add}\t{s}\n')
                    SimulatorHelper[add] = ['add', int(
                        regD, 2), int(reg1, 2), int(reg2, 2), 0, s]
                    instructions.append(s)
                if opcode == "00001":  # for SUB
                    s = f'sub x{int(regD,2)}, x{int(reg1,2)}, x{int(reg2,2)}'
                    disfile.write(f'{lin}\t{add}\t{s}\n')
                    SimulatorHelper[add] = ['sub', int(
                        regD, 2), int(reg1, 2), int(reg2, 2), 0, s]
                    instructions.append(s)
                if opcode == "00010":  # for AND
                    s = f'and x{int(regD,2)}, x{int(reg1,2)}, x{int(reg2,2)}'
                    disfile.write(f'{lin}\t{add}\t{s}\n')
                    SimulatorHelper[add] = ['and', int(
                        regD, 2), int(reg1, 2), int(reg2, 2), 0, s]
                    instructions.append(s)
                if opcode == "00011":  # for OR
                    s = f'or x{int(regD,2)}, x{int(reg1,2)}, x{int(reg2,2)}'
                    disfile.write(f'{lin}\t{add}\t{s}\n')
                    SimulatorHelper[add] = ['or', int(
                        regD, 2), int(reg1, 2), int(reg2, 2), 0, s]
                    instructions.append(s)
            if LSB == "10":
                opcode = getcode(line, -7)
                regD = getcode(line, -12)
                reg1 = getcode(line, -20)
                imm = getcode(line, 0, 12)

                if opcode == "00000":  # for ADDI
                    if imm[0] == '0':
                        s = f'addi x{int(regD,2)}, x{int(reg1,2)}, #{int(imm,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = ['addi', int(
                            regD, 2), int(reg1, 2), int(imm, 2), 0, 0, s]
                        instructions.append(s)
                    else:
                        a = twoscomp(imm)
                        s = f'addi x{int(regD,2)}, x{int(reg1,2)}, #-{int(a,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = ['addi', int(
                            regD, 2), int(reg1, 2), int(a, 2), 1, 0, s]
                        instructions.append(s)
                if opcode == "00001":  # for ANDI
                    if imm[0] == '0':
                        s = f'andi x{int(regD,2)}, x{int(reg1,2)}, #{int(imm,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = ['andi', int(
                            regD, 2), int(reg1, 2), int(imm, 2), 0, 0, s]
                        instructions.append(s)
                    else:
                        a = twoscomp(imm)
                        s = f'andi x{int(regD,2)}, x{int(reg1,2)}, #-{int(a,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = ['andi', int(
                            regD, 2), int(reg1, 2), int(a, 2), 1, 0, s]
                        instructions.append(s)

                if opcode == "00010":  # for ORI
                    if imm[0] == '0':
                        s = f'ori x{int(regD,2)}, x{int(reg1,2)}, #{int(imm,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = ['ori', int(
                            regD, 2), int(reg1, 2), int(imm, 2), 0, 0, s]
                        instructions.append(s)
                    else:
                        a = twoscomp(imm)
                        s = f'ori x{int(regD,2)}, x{int(reg1,2)}, #-{int(a,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = ['ori', int(
                            regD, 2), int(reg1, 2), int(a, 2), 1, 0, s]
                        instructions.append(s)

                if opcode == "00011":  # for SLL
                    s = f'sll x{int(regD,2)}, x{int(reg1,2)}, #{int(imm,2)}'
                    disfile.write(f'{lin}\t{add}\t{s}\n')
                    SimulatorHelper[add] = ['sll', int(
                        regD, 2), int(reg1, 2), int(imm, 2), 0, s]
                    instructions.append(s)
                if opcode == "00100":  # for SRA
                    s = f'sra x{int(regD,2)}, x{int(reg1,2)}, #{int(imm,2)}'
                    disfile.write(f'{lin}\t{add}\t{s}\n')
                    SimulatorHelper[add] = ['sra', int(
                        regD, 2), int(reg1, 2), int(imm, 2), 0, s]
                    instructions.append(s)
                if opcode == "00101":  # for LW
                    s = f'lw x{int(regD,2)}, {int(imm,2)}(x{int(reg1,2)})'
                    disfile.write(f'{lin}\t{add}\t{s}\n')
                    SimulatorHelper[add] = [
                        'lw', int(regD, 2), int(reg1, 2), int(imm, 2), 0, s]
                    instructions.append(s)
            if LSB == "11":
                opcode = getcode(line, -7)
                regD = getcode(line, -12)
                imm = getcode(line, 0, 20)

                if opcode == "00000":  # for JAL
                    if (imm[0] == "0"):
                        s = f'jal x{int(regD,2)}, #{int(imm,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = [
                            'jal', 0, int(regD, 2), int(imm, 2), 1, s]
                        instructions.append(s)
                    else:
                        a = twoscomp(imm)
                        s = f'jal x{int(regD,2)}, #-{int(a,2)}'
                        disfile.write(f'{lin}\t{add}\t{s}\n')
                        SimulatorHelper[add] = [
                            'jal', 1, int(regD, 2), int(a, 2), 0, s]
                        instructions.append(s)

                if opcode == "11111":  # for BREAK
                    s = 'break'
                    disfile.write(f'{lin}\t{add}\tbreak\n')
                    breakpoint = True
                    SimulatorHelper[add] = [0, s]
                    instructions.append(s)
        else:
            if line[0] == "0":
                disfile.write(f'{lin}\t{add}\t{int(line.strip(),2)}\n')
                addressreg.append(add)
                valuemem.append(int(f'{int(line.strip(),2)}'))
            else:
                a = twoscomp(line.strip())
                disfile.write(f'{lin}\t{add}\t-{int(a,2)}\n')
                valuemem.append(int(f'-{int(a,2)}'))
                addressreg.append(add)
        add = add + 4
    memorydis = {addressreg[i]: valuemem[i] for i in range(len(addressreg))}
    duplimemorydis = memorydis
    # print (instructions)
    add = 256
    cycle = 1
    maxissue = 2
    Preissue = {0: "",
                1: "",
                2: "",
                3: ""
                }
    PreALU1 = {0: "",
               1: ""
               }
    IfUnit = {0: "",
              1: ""
              }
    MemQ = {0: "",
            1: ""}
    ALU2 = {0: "",
            1: ""}
    ALU3 = {0: "",
            1: ""}

    breakfaced = False
    rd = 0

    while breakfaced == False:
    # while cycle != 15:
        stopissue = 1
        system = [Preissue, PreALU1, IfUnit, MemQ, ALU2, ALU3]
        systemfree = all(
            all(inst == "" for inst in sys.values()) for sys in system)
        if add in SimulatorHelper.keys():
            s = SimulatorHelper[add][-1]
            isif = SimulatorHelper[add][-2]

            if SimulatorHelper[add][-1] == "break":
                IfUnit[1] = "[break]"
                breakfaced = True

            if IfUnit[1] != "":
                IfUnit[1] = ""

            if IfUnit[0] != "" and IfUnit[1] == "":
                if IfUnit[0][0] == 'jal' and UsedRegisterb[IfUnit[0][1]] == 0:
                    IfUnit[1] = IfUnit[0]
                    IfUnit[0] = ""
                    # print(add)
                    add, a, b = getaddress(add, SimulatorHelper)
                    dupliregister[b] = a
                    change = 1
                    # print(add)

                if UsedRegisterb[IfUnit[0][1]] == 0 and UsedRegisterb[IfUnit[0][2]] == 0:
                    IfUnit[1] = IfUnit[0]
                    IfUnit[0] = ""
                    # print(add)
                    add = getaddress(add, SimulatorHelper)
                    # print(add)

            if change == 1:
                for i in range(len(dupliregister)):
                    register[i] = dupliregister[i]
                memorydis = duplimemorydis
                change2 = 1
                change = 0
            # if SimulatorHelper[add][0] == 'beq':
            #     UsedRegister[SimulatorHelper[add][1]] = 1
            #     imm = SimulatorHelper[add][3]
            #     if SimulatorHelper[add][4] == 1:
            #         imm = (-1)*imm
            #     if register[SimulatorHelper[add][1]] == register[SimulatorHelper[add][2]]:
            #         imm = imm << 1
            #         add += imm
            #     else:
            #         add = add + 4

            # elif SimulatorHelper[add][0] == 'bne':
            #     UsedRegister[SimulatorHelper[add][1]] = 1
            #     imm = SimulatorHelper[add][3]
            #     if SimulatorHelper[add][4] == 1:
            #         imm = (-1)*imm
            #     if register[SimulatorHelper[add][1]] != register[SimulatorHelper[add][2]]:
            #         imm = imm << 1
            #         add += imm
            #     else:
            #         add = add + 4

            # elif SimulatorHelper[add][0] == 'blt':
            #     UsedRegister[SimulatorHelper[add][1]] = 1
            #     imm = SimulatorHelper[add][3]
            #     if SimulatorHelper[add][4] == 1:
            #         imm = (-1)*imm
            #     if register[SimulatorHelper[add][1]] < register[SimulatorHelper[add][2]]:
            #         imm = imm << 1
            #         add += imm
            #     else:
            #         add = add + 4

            # if SimulatorHelper[add][0] == 'sw':
            #     imm = SimulatorHelper[add][3]
            #     memorydis[imm+register[SimulatorHelper[add][2]]
            #               ] = register[SimulatorHelper[add][1]]
            #     add = add + 4

            # elif SimulatorHelper[add][0] == 'add':
            #     UsedRegister[SimulatorHelper[add][1]] = 1
            #     register[SimulatorHelper[add][1]] = register[SimulatorHelper[add]
            #                                                  [2]] + register[SimulatorHelper[add][3]]
            #     add = add + 4
            # elif SimulatorHelper[add][0] == 'sub':
            #     UsedRegister[SimulatorHelper[add][1]] = 1
            #     register[SimulatorHelper[add][1]] = register[SimulatorHelper[add]
            #                                                  [2]] - register[SimulatorHelper[add][3]]
            #     add = add + 4
            # elif SimulatorHelper[add][0] == 'and':
            #     UsedRegister[SimulatorHelper[add][1]] = 1
            #     register[SimulatorHelper[add][1]] = register[SimulatorHelper[add]
            #                                                  [2]] & register[SimulatorHelper[add][3]]
            #     add = add + 4

            # elif SimulatorHelper[add][0] == 'or':
            #     UsedRegister[SimulatorHelper[add][1]] = 1
            #     register[SimulatorHelper[add][1]] = register[SimulatorHelper[add]
            #                                                  [2]] | register[SimulatorHelper[add][3]]
            #     add = add + 4

            # elif SimulatorHelper[add][0] == 'addi':
            #     UsedRegister[SimulatorHelper[add][1]] = 1
            #     imm = SimulatorHelper[add][3]
            #     if SimulatorHelper[add][4] == 1:
            #         imm = (-1) * SimulatorHelper[add][3]
            #     register[SimulatorHelper[add][1]
            #              ] = register[SimulatorHelper[add][2]] + imm
            #     add = add + 4
            # elif SimulatorHelper[add][0] == 'andi':
            #     UsedRegister[SimulatorHelper[add][1]] = 1
            #     imm = SimulatorHelper[add][3]
            #     if SimulatorHelper[add][4] == 1:
            #         imm = (-1) * SimulatorHelper[add][3]
            #     register[SimulatorHelper[add][1]
            #              ] = register[SimulatorHelper[add][2]] & imm
            #     add = add + 4
            # elif SimulatorHelper[add][0] == 'ori':
            #     UsedRegister[SimulatorHelper[add][1]] = 1
            #     imm = SimulatorHelper[add][3]
            #     if SimulatorHelper[add][4] == 1:
            #         imm = (-1) * SimulatorHelper[add][3]
            #     register[SimulatorHelper[add][1]
            #              ] = register[SimulatorHelper[add][2]] | imm
            #     add = add + 4
            # elif SimulatorHelper[add][0] == 'sll':
            #     UsedRegister[SimulatorHelper[add][1]] = 1
            #     register[SimulatorHelper[add][1]] = register[SimulatorHelper[add]
            #                                                  [2]] << SimulatorHelper[add][3]
            #     add = add + 4

            # elif SimulatorHelper[add][0] == 'sra':
            #     UsedRegister[SimulatorHelper[add][1]] = 1
            #     register[SimulatorHelper[add][1]] = register[SimulatorHelper[add]
            #                                                  [2]] >> SimulatorHelper[add][3]
            #     add = add + 4

            # elif SimulatorHelper[add][0] == 'lw':
            #     UsedRegister[SimulatorHelper[add][1]] = 1
            #     register[SimulatorHelper[add][1]] = memorydis[SimulatorHelper[add]
            #                                                   [3] + register[SimulatorHelper[add][2]]]
            #     add = add + 4

            # # elif (SimulatorHelper[add][0] == 'jal'):
            # #     jimm = SimulatorHelper[add][3]
            # #     check = SimulatorHelper[add][1]
            # #     register[SimulatorHelper[add][2]] = add + 4
            # #     if check == 1:
            # #         jimm = jimm * (-1)
            # #     add = add + (jimm << 1)

            # if (SimulatorHelper[add][-1] == 'break'):
            #     simfile.write('--------------------\n')
            #     simfile.write(f'Cycle {cycle}:{s}\n\n')
            #     simfile.write('IF Unit:\n')
            #     simfile.write(f'\tWaiting:{IfUnit[0]}\n')
            #     simfile.write(f'\tExecuted:[break]\n')
            #     simfile.write('Pre-Issue Queue:\n')
            #     simfile.write(f'\tEntry 0:{Preissue[0]}\n')
            #     simfile.write(f'\tEntry 1:{Preissue[1]}\n')
            #     simfile.write(f'\tEntry 2:{Preissue[2]}\n')
            #     simfile.write(f'\tEntry 3:{Preissue[3]}\n')
            #     simfile.write('Pre-ALU1 Queue:\n')
            #     simfile.write(f'\tEntry 0:{PreALU1[0]}\n')
            #     simfile.write(f'\tEntry 1:{PreALU1[1]}\n')
            #     simfile.write(f'Pre-MEM Queue:{MemQ[0]}\n')
            #     simfile.write(f'Post-MEM Queue{MemQ[1]}\n')
            #     simfile.write(f'Pre-ALU2 Queue:{ALU2[0]}\n')
            #     simfile.write(f'Post-ALU2 Queue:{ALU2[1]}\n')
            #     simfile.write(f'Pre-ALU3 Queue:{ALU3[0]}\n')
            #     simfile.write(f'Post-ALU3 Queue:{ALU3[1]}\n\n')
            #     simfile.write('Registers\n')
            #     simfile.write(
            #         f'x00:\t{register[0]}\t{register[1]}\t{register[2]}\t{register[3]}\t{register[4]}\t{register[5]}\t{register[6]}\t{register[7]}\n')
            #     simfile.write(
            #         f'x08:\t{register[8]}\t{register[9]}\t{register[10]}\t{register[11]}\t{register[12]}\t{register[13]}\t{register[14]}\t{register[15]}\n')
            #     simfile.write(
            #         f'x16:\t{register[16]}\t{register[17]}\t{register[18]}\t{register[19]}\t{register[20]}\t{register[21]}\t{register[22]}\t{register[23]}\n')
            #     simfile.write(
            #         f'x24:\t{register[24]}\t{register[25]}\t{register[26]}\t{register[27]}\t{register[28]}\t{register[29]}\t{register[30]}\t{register[31]}\n\n')
            #     simfile.write('Data\n')
            #     valuem = list(memorydis.values())
            #     addressr = list(memorydis.keys())
            #     for i in range(0, len(addressr), 8):
            #         data = valuem[i:i+8]
            #         memory = addressr[i]
            #         simfile.write(f'{memory}:\t')
            #         for d in data:
            #             simfile.write(f'{d}\t')
            #         simfile.write('\n')
            #     break

            if MemQ[1] != "":
                if MemQ[1][0] == 'lw':
                    # UsedRegister[MemQ[1][1]] = 0
                    UsedRegisterb[MemQ[1][1]] = 0
                    register[MemQ[1][1]] = memorydis[MemQ[1]
                                                     [3] + register[MemQ[1][2]]]
                    dupliregister[MemQ[1][1]] = memorydis[MemQ[1]
                                                          [3] + register[MemQ[1][2]]]
                    change = 1
                    change2 = 1
                    rd = MemQ[1][1]
                    MemQ[1] = ""

            if MemQ[0] != "":
                if MemQ[0][0] == "lw":
                    MemQ[1] = MemQ[0]
                    MemQ[0] = ""

                elif MemQ[0][0] == "sw":
                    imm = MemQ[0][3]
                    duplimemorydis[imm+register[MemQ[0][2]]
                                   ] = register[MemQ[0][1]]
                    change = 1
                    rd = -1
                    MemQ[0] = ""

            if PreALU1[0] != "":
                MemQ[0] = PreALU1[0]
                PreALU1[0] = PreALU1[1]
                PreALU1[1] = ""

            # elif (PreALU1[0] == "" and Preissue[0] != "" and (Preissue[0][0]=="lw" or Preissue[0][0]=="sw" )):
            #     PreALU1[0] = Preissue[0]
            #     Preissue[0] = Preissue[1]
            #     Preissue[1] = Preissue[2]
            #     Preissue[2] = Preissue[3]
            #     Preissue[3] = ""

            # elif (PreALU1[0] != "" and PreALU1[1] == "" and Preissue[0] != "" and (Preissue[0][0]=="lw" or Preissue[0][0]=="sw" )):
            #     PreALU1[1] = Preissue[0]
            #     Preissue[0] = Preissue[1]
            #     Preissue[1] = Preissue[2]
            #     Preissue[2] = Preissue[3]
            #     Preissue[3] = ""

            if ALU2[1] != "":
                # UsedRegister[ALU2[1][1]] = 0
                UsedRegisterb[ALU2[1][1]] = 0
                ALU2[1] = ""

            if ALU2[0] != "":
                if ALU2[0][0] == 'add':
                    dupliregister[ALU2[0][1]] = register[ALU2[0]
                                                         [2]] + register[ALU2[0][3]]
                    change = 1
                    rd = ALU2[0][1]
                    # print(add)
                elif ALU2[0][0] == 'sub':
                    dupliregister[ALU2[0][1]] = register[ALU2[0]
                                                         [2]] - register[ALU2[0][3]]
                    change = 1
                    rd = ALU2[0][1]
                elif ALU2[0][0] == 'addi':

                    imm = ALU2[0][3]
                    if ALU2[0][4] == 1:
                        imm = (-1) * ALU2[0][3]
                    dupliregister[ALU2[0][1]
                                  ] = register[ALU2[0][2]] + imm
                    change = 1
                    rd = ALU2[0][1]
                ALU2[1] = ALU2[0]
                ALU2[0] = ""

            # if (ALU2[0] == "" and ALU2[1] == "" and Preissue[0] != "" and (Preissue[0][0]=="add" or Preissue[0][0]=="sub" or Preissue[0][0]=="addi")):
            #     ALU2[0] = Preissue[0]
            #     Preissue[0] = Preissue[1]
            #     Preissue[1] = Preissue[2]
            #     Preissue[2] = Preissue[3]
            #     Preissue[3] = ""

            if ALU3[1] != "":
                # UsedRegister[ALU3[1][1]] =0
                UsedRegisterb[ALU3[1][1]] = 0
                ALU3[1] = ""

            if ALU3[0] != "":
                if ALU3[0][0] == 'and':
                    dupliregister[ALU3[0][1]] = register[ALU3[0]
                                                         [2]] & register[ALU3[0][3]]
                    change = 1
                    rd = ALU3[0][1]
                elif ALU3[0][0] == 'or':
                    dupliregister[ALU3[0][1]] = register[ALU3[0]
                                                             [2]] | register[ALU3[0][3]]
                    change = 1
                    rd = ALU3[0][1]
                elif ALU3[0][0] == 'andi':

                    imm = ALU3[0][3]
                    if ALU3[0][4] == 1:
                        imm = (-1) * ALU3[0][3]
                    dupliregister[ALU3[0][1]
                                  ] = register[ALU3[0][2]] & imm
                    change = 1
                    rd = ALU3[0][1]
                elif ALU3[0][0] == 'ori':

                    imm = ALU3[0][3]
                    if SimulatorHelper[add][4] == 1:
                        imm = (-1) * ALU3[0][3]
                    dupliregister[ALU3[0][1]
                                  ] = register[ALU3[0][2]] | imm
                    change = 1
                    rd = ALU3[0][1]
                elif ALU3[0][0] == 'sll':

                    dupliregister[ALU3[0][1]] = register[ALU3[0]
                                                         [2]] << ALU3[0][3]
                    change = 1
                    rd = ALU3[0][1]
                elif ALU3[0][0] == 'sra':

                    dupliregister[ALU3[0][1]] = register[ALU3[0]
                                                         [2]] >> ALU3[0][3]
                    change = 1
                    rd = ALU3[0][1]

                ALU3[1] = ALU3[0]
                ALU3[0] = ""

            # elif (ALU3[0] == "" and Preissue[0] != "" and (Preissue[0][0]=="andi" or Preissue[0][0]=="ori" or Preissue[0][0]=="sll" or Preissue[0][0]=="sra"or Preissue[0][0]=="and"or Preissue[0][0]=="or")):
            #     ALU3[0] = Preissue[0]
            #     Preissue[0] = Preissue[1]
            #     Preissue[1] = Preissue[2]
            #     Preissue[2] = Preissue[3]
            #     Preissue[3] = ""
            if Preissue[3] != "":
                stopissue = 0
            here = 0
            # LPI = len([x for x in Preissue.values() if x != ""])
            # for i in range(LPI):
            #     if (ALU2[0] == "" and ALU2[1] == "" and Preissue[i] != "" and (Preissue[i][0]=="add" or Preissue[i][0]=="sub" or Preissue[i][0]=="addi")):
            #             if  UsedRegister[Preissue[i][2]] == 0 and UsedRegister[Preissue[i][3]] == 0:
            #                 UsedRegister[Preissue[i][1]] = 1
            #                 ALU2[0] = Preissue[i]
            #                 here = 1

            #     elif (ALU3[0] == "" and ALU3[1] == "" and Preissue[i] != "" and (Preissue[i][0]=="andi" or Preissue[i][0]=="ori" or Preissue[i][0]=="sll" or Preissue[i][0]=="sra"or Preissue[i][0]=="and"or Preissue[i][0]=="or")):
            #             if  UsedRegister[Preissue[i][2]] == 0:
            #                 UsedRegister[Preissue[i][1]] = 1
            #                 ALU3[0] = Preissue[i]
            #                 here =1

            #     elif ((PreALU1[0] == "" or PreALU1[1] == "") and Preissue[i] != "" and (Preissue[i][0]=="lw" or Preissue[i][0]=="sw" )):
            #             if ((Preissue[i][0] == "lw" and UsedRegister[Preissue[i][2]] == 0) or Preissue[i][0]=="sw"):
            #                 if Preissue[i][0] == "lw":
            #                     UsedRegister[Preissue[i][1]] = 1
            #                     # UsedRegister[Preissue[1][1]] = 1
            #                 for space in range(2):
            #                     if PreALU1[space] == "":
            #                         PreALU1[space] = Preissue[i]
            #                         break
            #                 PreALU1[0] = Preissue[i]
            #                 here = 1
            # if here == 1:
            #     Preissue[0] = Preissue[1]
            #     Preissue[1] = Preissue[2]
            #     Preissue[2] = Preissue[3]
            #     Preissue[3] = ""
            # for i in range(2)
            # issue = [x for x in Preissue.values() if x != ""]
            # prealu =[]
            # a = 0
            # for i in issue:
            #     # print("")
            #     # print(UsedRegister)
            #     if (ALU2[0] == "" and ALU2[1] == "" and len(i)>0 and (i[0] == "add" or i[0] == "sub" or i[0] == "addi")):
            #         if UsedRegister[i[2]] == 0 and UsedRegister[i[3]] == 0:
            #             UsedRegister[i[1]] = 1
            #             ALU2[0] = i
            #             issue.pop(a)

            #     elif (ALU3[0] == "" and ALU3[1] == "" and len(i)>0 and (i[0] == "andi" or i[0] == "ori" or i[0] == "sll" or i[0] == "sra" or i[0] == "and" or i[0] == "or")):
            #         if UsedRegister[i[2]] == 0:
            #             UsedRegister[i[1]] = 1
                        
            #             ALU3[0] = i
            #             issue.pop(a)

            #     elif ((PreALU1[0] == "") and len(i)>0 and (i[0] == "lw" or i[0] == "sw")):
            #         if ((i[0] == "lw" and UsedRegister[i[2]] == 0) or i[0] == "sw"):
            #             if i[0] == "lw":
            #                 UsedRegister[i[1]] = 1
            #                 # UsedRegister[Preissue[1][1]] = 1
            #             # for space in range(2):
            #             #     if PreALU1[space] == "":
            #             #         PreALU1[space] = i
            #             #         break
            #             prealu.append(i)
            #             issue.pop(a)
            #     else:
            #         a = a+1
            # for i in range(len(prealu)):
            #     PreALU1[i] = prealu[i]

            # Preissue[0]=""
            # Preissue[1]=""
            # Preissue[2]=""
            # Preissue[3]=""

            # for i in range(len(issue)):
            #     Preissue[i] = issue[i]
            

            if (ALU2[0] == "" and ALU2[1] == "" and Preissue[0] != "" and (Preissue[0][0] == "add" or Preissue[0][0] == "sub" or Preissue[0][0] == "addi")):
                if UsedRegister[Preissue[0][2]] == 0 and UsedRegister[Preissue[0][3]] == 0:
                    UsedRegister[Preissue[0][1]] = 1
                    ALU2[0] = Preissue[0]
                    Preissue[0] = Preissue[1]
                    Preissue[1] = Preissue[2]
                    Preissue[2] = Preissue[3]
                    Preissue[3] = ""

            elif (ALU3[0] == "" and ALU3[1] == "" and Preissue[0] != "" and (Preissue[0][0] == "andi" or Preissue[0][0] == "ori" or Preissue[0][0] == "sll" or Preissue[0][0] == "sra" or Preissue[0][0] == "and" or Preissue[0][0] == "or")):
                if UsedRegister[Preissue[0][2]] == 0:
                    UsedRegister[Preissue[0][1]] = 1
                    ALU3[0] = Preissue[0]
  
                    Preissue[0] = Preissue[1]

                    Preissue[1] = Preissue[2]
                    Preissue[2] = Preissue[3]
                    Preissue[3] = ""

            elif ((PreALU1[0] == "" or PreALU1[1] == "") and Preissue[0] != "" and (Preissue[0][0] == "lw" or Preissue[0][0] == "sw")):
                if ((Preissue[0][0] == "lw" and UsedRegister[Preissue[0][2]] == 0) or Preissue[0][0] == "sw"):
                    if Preissue[0][0] == "lw":
                        UsedRegister[Preissue[0][1]] = 1
                        # UsedRegister[Preissue[1][1]] = 1
                    # for space in range(2):
                    #     if PreALU1[space] == "":
                    #         PreALU1[space] = Preissue[0]
                    #         break
                    PreALU1[0] = Preissue[0]
                    Preissue[0] = Preissue[1]
                    Preissue[1] = Preissue[2]
                    Preissue[2] = Preissue[3]
                    Preissue[3] = ""

            if (ALU2[0] == "" and ALU2[1] == "" and Preissue[0] != "" and (Preissue[0][0] == "add" or Preissue[0][0] == "sub" or Preissue[0][0] == "addi")):
                if UsedRegister[Preissue[0][1]] == 0 and UsedRegister[Preissue[0][3]] == 0:
                    UsedRegister[Preissue[0][2]] = 1
                    ALU2[0] = Preissue[0]
                    Preissue[0] = Preissue[1]
                    Preissue[1] = Preissue[2]
                    Preissue[2] = Preissue[3]
                    Preissue[3] = ""

            elif (ALU3[0] == "" and ALU3[1] == "" and Preissue[0] != "" and (Preissue[0][0] == "andi" or Preissue[0][0] == "ori" or Preissue[0][0] == "sll" or Preissue[0][0] == "sra" or Preissue[0][0] == "and" or Preissue[0][0] == "or")):
                if UsedRegister[Preissue[0][2]] == 0:
                    UsedRegister[Preissue[0][1]] = 1
                    ALU3[0] = Preissue[0]
                    Preissue[0] = Preissue[1]
                    Preissue[1] = Preissue[2]
                    Preissue[2] = Preissue[3]
                    Preissue[3] = ""

            elif ((PreALU1[0] == "" or PreALU1[1] == "") and Preissue[0] != "" and (Preissue[0][0] == "lw" or Preissue[0][0] == "sw")):
                if ((Preissue[0][0] == "lw" and UsedRegister[Preissue[0][2]] == 0) or Preissue[0][0] == "sw"):
                    if Preissue[0][0] == "lw":
                        UsedRegister[Preissue[0][1]] = 1
                        # UsedRegister[Preissue[1][1]] = 1
                    # for space in range(2):
                    #     if PreALU1[space] == "":
                    #         PreALU1[space] = Preissue[0]
                    #         break
                    if PreALU1[0] !="" and PreALU1[0][2]!=Preissue[0][2]:
                        PreALU1[1] = Preissue[0]
                    # elif PreALU1[0] =="":
                    #     PreALU1[0] = Preissue[0]
                        Preissue[0] = Preissue[1]
                        Preissue[1] = Preissue[2]
                        Preissue[2] = Preissue[3]
                        Preissue[3] = ""

            if (ALU2[0] == "" and ALU2[1] == "" and Preissue[0] != "" and (Preissue[0][0] == "add" or Preissue[0][0] == "sub" or Preissue[0][0] == "addi")):
                if UsedRegister[Preissue[0][2]] == 0 and UsedRegister[Preissue[0][3]] == 0:
                    UsedRegister[Preissue[0][1]] = 1
                    ALU2[0] = Preissue[0]
                    Preissue[0] = Preissue[1]
                    Preissue[1] = Preissue[2]
                    Preissue[2] = Preissue[3]
                    Preissue[3] = ""

            elif (ALU3[0] == "" and ALU3[1] == "" and Preissue[0] != "" and (Preissue[0][0] == "andi" or Preissue[0][0] == "ori" or Preissue[0][0] == "sll" or Preissue[0][0] == "sra" or Preissue[0][0] == "and" or Preissue[0][0] == "or")):
                if UsedRegister[Preissue[0][2]] == 0:
                    UsedRegister[Preissue[0][1]] = 1
                    ALU3[0] = Preissue[0]
                    Preissue[0] = Preissue[1]
                    Preissue[1] = Preissue[2]
                    Preissue[2] = Preissue[3]
                    Preissue[3] = ""

            elif ((PreALU1[0] == "" or PreALU1[1] == "") and Preissue[0] != "" and (Preissue[0][0] == "lw" or Preissue[0][0] == "sw")):
                if ((Preissue[0][0] == "lw" and UsedRegister[Preissue[0][2]] == 0) or Preissue[0][0] == "sw"):
                    if Preissue[0][0] == "lw":
                        UsedRegister[Preissue[0][1]] = 1
                        # UsedRegister[Preissue[1][1]] = 1
                    # for space in range(2):
                    #     if PreALU1[space] == "":
                    #         PreALU1[space] = Preissue[0]
                    #         break
                    if PreALU1[0] !="" and PreALU1[0][2]!=Preissue[0][2]:
                        PreALU1[1] = Preissue[0]
                    # elif PreALU1[0] =="":
                    #     PreALU1[0] = Preissue[0]
                        Preissue[0] = Preissue[1]
                        Preissue[1] = Preissue[2]
                        Preissue[2] = Preissue[3]
                        Preissue[3] = ""
            if (ALU2[0] == "" and ALU2[1] == "" and Preissue[0] != "" and (Preissue[0][0] == "add" or Preissue[0][0] == "sub" or Preissue[0][0] == "addi")):
                if UsedRegister[Preissue[0][2]] == 0 and UsedRegister[Preissue[0][3]] == 0:
                    UsedRegister[Preissue[0][1]] = 1
                    ALU2[0] = Preissue[0]
                    Preissue[0] = Preissue[1]
                    Preissue[1] = Preissue[2]
                    Preissue[2] = Preissue[3]
                    Preissue[3] = ""

            elif (ALU3[0] == "" and ALU3[1] == "" and Preissue[0] != "" and (Preissue[0][0] == "andi" or Preissue[0][0] == "ori" or Preissue[0][0] == "sll" or Preissue[0][0] == "sra" or Preissue[0][0] == "and" or Preissue[0][0] == "or")):
                if UsedRegister[Preissue[0][2]] == 0:
                    UsedRegister[Preissue[0][1]] = 1
                    ALU3[0] = Preissue[0]
                    Preissue[0] = Preissue[1]
                    Preissue[1] = Preissue[2]
                    Preissue[2] = Preissue[3]
                    Preissue[3] = ""

            elif ((PreALU1[0] == "" or PreALU1[1] == "") and Preissue[0] != "" and (Preissue[0][0] == "lw" or Preissue[0][0] == "sw")):
                if ((Preissue[0][0] == "lw" and UsedRegister[Preissue[0][2]] == 0) or Preissue[0][0] == "sw"):
                    if Preissue[0][0] == "lw":
                        UsedRegister[Preissue[0][1]] = 1
                        # UsedRegister[Preissue[1][1]] = 1
                    # for space in range(2):
                    #     if PreALU1[space] == "":
                    #         PreALU1[space] = Preissue[0]
                    #         break
                    if PreALU1[0] !="" and PreALU1[0][2] != Preissue[0][2]:
                        PreALU1[1] = Preissue[0]
                    # elif PreALU1[0] =="":
                    #     PreALU1[0] = Preissue[0]
                        Preissue[0] = Preissue[1]
                        Preissue[1] = Preissue[2]
                        Preissue[2] = Preissue[3]
                        Preissue[3] = ""



            if change2 == 1:
                if  rd!= -1:
                    UsedRegister[rd] = 0
                    # UsedRegisterb[rd] = 0
                change2 = 0

            for i in range(maxissue):
                if Preissue[i] != "":
                    UsedRegisterb[Preissue[i][1]] = 1
                if Preissue[i+1] != "":
                    UsedRegisterb[Preissue[i+1][1]] = 1
                if Preissue[i+2] != "":
                    UsedRegisterb[Preissue[i+2][1]] = 1

            if IfUnit[0] == "" and IfUnit[1] == "" and breakfaced == False and stopissue == 1:
                for i in range(maxissue):
                    if add in SimulatorHelper.keys():
                        if SimulatorHelper[add][0] == "jal":
                            if UsedRegisterb[SimulatorHelper[add][2]] == 1:
                                IfUnit[0] = SimulatorHelper[add]
                            else:
                                IfUnit[1] = SimulatorHelper[add]
                                add, a, b = getaddress(add, SimulatorHelper)
                                dupliregister[b] = a
                                change = 1
                            break

                        elif SimulatorHelper[add][0] == "beq" or SimulatorHelper[add][0] == "bne" or SimulatorHelper[add][0] == "blt":
                            if UsedRegisterb[SimulatorHelper[add][1]] == 0 and UsedRegisterb[SimulatorHelper[add][2]] == 0:
                                IfUnit[1] = SimulatorHelper[add]
                                add = getaddress(add, SimulatorHelper)
                            else:
                                # if SimulatorHelper[add][0] == "blt":
                                    # print(UsedRegister)
                                #     print (UsedRegister[SimulatorHelper[add][1]])
                                #     print (UsedRegister[SimulatorHelper[add][2]])
                                IfUnit[0] = SimulatorHelper[add]

                            break

                        else:
                            if all(value != "" for value in Preissue.values()):
                                break
                            for space in range(4):
                                if Preissue[space] == "":
                                    Preissue[space] = SimulatorHelper[add]
                                    add = add + 4
                                    break

                    if Preissue[i] != "":
                        UsedRegisterb[Preissue[i][1]] = 1
                    if Preissue[i+1] != "":
                        UsedRegisterb[Preissue[i+1][1]] = 1
                    if Preissue[i+2] != "":
                        UsedRegisterb[Preissue[i+2][1]] = 1

            # if (SimulatorHelper[add][-1] == 'break'):

            #     simfile.write('--------------------\n')
            #     simfile.write(f'Cycle {cycle}:\n\n')
            #     simfile.write('IF Unit:\n')
            #     simfile.write(f'\tWaiting:{[IfUnit[0]][-1]}\n')
            #     simfile.write(f'\tExecuted:[break]\n')
            #     simfile.write('Pre-Issue Queue:\n')
            #     simfile.write(f'\tEntry 0:{[Preissue[0]][-1]}\n')
            #     simfile.write(f'\tEntry 1:{[Preissue[1]][-1]}\n')
            #     simfile.write(f'\tEntry 2:{[Preissue[2]][-1]}\n')
            #     simfile.write(f'\tEntry 3:{[Preissue[3]][-1]}\n')
            #     simfile.write('Pre-ALU1 Queue:\n')
            #     simfile.write(f'\tEntry 0:{[PreALU1[0]][-1]}\n')
            #     simfile.write(f'\tEntry 1:{[PreALU1[1]][-1]}\n')
            #     simfile.write(f'Pre-MEM Queue:{[MemQ[0]][-1]}\n')
            #     simfile.write(f'Post-MEM Queue:{[MemQ[1]][-1]}\n')
            #     simfile.write(f'Pre-ALU2 Queue:{[ALU2[0]][-1]}\n')
            #     simfile.write(f'Post-ALU2 Queue:{[ALU2[1]][-1]}\n')
            #     simfile.write(f'Pre-ALU3 Queue:{[ALU3[0]][-1]}\n')
            #     simfile.write(f'Post-ALU3 Queue:{[ALU3[1]][-1]}\n\n')
            #     simfile.write('Registers\n')
            #     simfile.write(
            #         f'x00:\t{register[0]}\t{register[1]}\t{register[2]}\t{register[3]}\t{register[4]}\t{register[5]}\t{register[6]}\t{register[7]}\n')
            #     simfile.write(
            #         f'x08:\t{register[8]}\t{register[9]}\t{register[10]}\t{register[11]}\t{register[12]}\t{register[13]}\t{register[14]}\t{register[15]}\n')
            #     simfile.write(
            #         f'x16:\t{register[16]}\t{register[17]}\t{register[18]}\t{register[19]}\t{register[20]}\t{register[21]}\t{register[22]}\t{register[23]}\n')
            #     simfile.write(
            #         f'x24:\t{register[24]}\t{register[25]}\t{register[26]}\t{register[27]}\t{register[28]}\t{register[29]}\t{register[30]}\t{register[31]}\n\n')
            #     simfile.write('Data\n')
            #     valuem = list(memorydis.values())
            #     addressr = list(memorydis.keys())
            #     for i in range(0, len(addressr), 8):
            #         data = valuem[i:i+8]
            #         memory = addressr[i]
            #         simfile.write(f'{memory}:\t')
            #         for d in data:
            #             simfile.write(f'{d}\t')
            #         simfile.write('\n')
            #     break

            simfile.write('--------------------\n')
            simfile.write(f'Cycle {cycle}:\n\n')
            simfile.write('IF Unit:\n')
            if IfUnit[0] == "":
                simfile.write(f'\tWaiting: {IfUnit[0]}\n')
            else:
                simfile.write(f'\tWaiting: [{IfUnit[0][-1]}]\n')
            if breakfaced == True:
                simfile.write(f'\tExecuted: [break]\n')
            elif IfUnit[1] == "":
                simfile.write(f'\tExecuted: {IfUnit[1]}\n')
            else:
                simfile.write(f'\tExecuted: [{IfUnit[1][-1]}]\n')

            simfile.write('Pre-Issue Queue:\n')
            if Preissue[0] != "":
                simfile.write(f'\tEntry 0: [{Preissue[0][-1]}]\n')
            else:
                simfile.write(f'\tEntry 0: {Preissue[0]}\n')
            if Preissue[1] != "":
                simfile.write(f'\tEntry 1: [{Preissue[1][-1]}]\n')
            else:
                simfile.write(f'\tEntry 1: {Preissue[1]}\n')
            if Preissue[2] != "":
                simfile.write(f'\tEntry 2: [{Preissue[2][-1]}]\n')
            else:
                simfile.write(f'\tEntry 2: {Preissue[2]}\n')
            if Preissue[3] != "":
                simfile.write(f'\tEntry 3: [{Preissue[3][-1]}]\n')
            else:
                simfile.write(f'\tEntry 3: {Preissue[3]}\n')

            simfile.write('Pre-ALU1 Queue:\n')
            if PreALU1[0] != "":
                simfile.write(f'\tEntry 0: [{PreALU1[0][-1]}]\n')
            else:
                simfile.write(f'\tEntry 0: {PreALU1[0]}\n')
            if PreALU1[1] != "":
                simfile.write(f'\tEntry 1: [{PreALU1[1][-1]}]\n')
            else:
                simfile.write(f'\tEntry 1: {PreALU1[1]}\n')
            if MemQ[0] != "":
                simfile.write(f'Pre-MEM Queue: [{MemQ[0][-1]}]\n')
            else:
                simfile.write(f'Pre-MEM Queue:{MemQ[0]}\n')
            if MemQ[1] != "":
                simfile.write(f'Post-MEM Queue:[{MemQ[1][-1]}]\n')
            else:
                simfile.write(f'Post-MEM Queue: {MemQ[1]}\n')
            if ALU2[0] == "":
                simfile.write(f'Pre-ALU2 Queue: {ALU2[0]}\n')
            else:
                simfile.write(f'Pre-ALU2 Queue: [{ALU2[0][-1]}]\n')
            if ALU2[1] != "":
                simfile.write(f'Post-ALU2 Queue: [{ALU2[1][-1]}]\n')
            else:
                simfile.write(f'Post-ALU2 Queue: {ALU2[1]}\n')
            if ALU3[0] != "":
                simfile.write(f'Pre-ALU3 Queue: [{ALU3[0][-1]}]\n')
            else:
                simfile.write(f'Pre-ALU3 Queue: {ALU3[0]}\n')
            if ALU3[1] == "":
                simfile.write(f'Post-ALU3 Queue: {ALU3[1]}\n\n')
            else:
                simfile.write(f'Post-ALU3 Queue: [{ALU3[1][-1]}]\n\n')
            simfile.write('Registers\n')
            simfile.write(
                f'x00:\t{register[0]}\t{register[1]}\t{register[2]}\t{register[3]}\t{register[4]}\t{register[5]}\t{register[6]}\t{register[7]}\n')
            simfile.write(
                f'x08:\t{register[8]}\t{register[9]}\t{register[10]}\t{register[11]}\t{register[12]}\t{register[13]}\t{register[14]}\t{register[15]}\n')
            simfile.write(
                f'x16:\t{register[16]}\t{register[17]}\t{register[18]}\t{register[19]}\t{register[20]}\t{register[21]}\t{register[22]}\t{register[23]}\n')
            simfile.write(
                f'x24:\t{register[24]}\t{register[25]}\t{register[26]}\t{register[27]}\t{register[28]}\t{register[29]}\t{register[30]}\t{register[31]}\n\n')
            simfile.write('Data\n')
            valuem = list(memorydis.values())
            addressr = list(memorydis.keys())
            for i in range(0, len(addressr), 8):
                data = valuem[i:i+8]
                memory = addressr[i]
                simfile.write(f'{memory}:\t')
                for d in data:
                    simfile.write(f'{d}\t')
                simfile.write('\n')
            print(UsedRegister)
            cycle = cycle + 1


if __name__ == "__main__":
    inputfile = sys.argv[1]
    a = '.txt'
    if (a not in inputfile):
        inputfile = inputfile+a
    register = [0] * 32
    dupliregister = [0] * 32
    UsedRegister = [0] * 32
    UsedRegisterb = [0] * 32

    with open(inputfile, 'r') as inputfile, open('disassembly.txt', 'w') as disfile, open('simulation.txt', 'w') as simfile:
        Simulator(inputfile, disfile, simfile)

