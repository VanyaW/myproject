
import os
import subprocess
import copy
import math
#import  numpy

def setupVariables(variables, wordsize):
    """
    Adds a list of variables to the stp stpfile.
    """
    return getStringForVariables(variables, wordsize) + "\n"

def getStringForVariables(variables, wordsize):
    """
    Takes as input the variable name, number of variables and the wordsize
    and constructs for instance a string of the form:
    x00, x01, ..., x30: BITVECTOR(wordsize);
    """
    command = ""
    for var in variables:
        command += var + ","

    command = command[:-1]
    command += ": BITVECTOR({0});".format(wordsize)
    return command

def setupQuery():
    """
    Adds the query and printing of counterexample to the stp stpfile.
    """
    return "QUERY(FALSE);\nCOUNTEREXAMPLE;\n"

def solver1(solve_file):
    res = subprocess.getoutput("stp --cryptominisat --thread 5 --CVC " + solve_file)
    print(res)
    if res == "Valid.":
        return True, res
    else:
        return False, res

def And_operation(var,round,m,start):
    statement = ""
    i=start
    j=start//2
    statement+="ASSERT(P{0}_{1}_{2}_{12}@P{0}_{1}_{2}_{13}@P{0}_{1}_{2}_{14}@P{0}_{1}_{2}_{15}@P{0}_{1}_{2}_{16}@P{0}_{1}_{2}_{17}@P{0}_{1}_{2}_{18}@P{0}_{1}_{2}_{19}=(P{0}_{3}_{2}_{5}@P{0}_{3}_{2}_{6}@P{0}_{3}_{2}_{7}@P{0}_{3}_{2}_{8}@P{0}_{3}_{2}_{9}@P{0}_{3}_{2}_{10}@P{0}_{3}_{2}_{11}@P{0}_{3}_{2}_{4})&(P{0}_{3}_{2}_{11}@P{0}_{3}_{2}_{4}@P{0}_{3}_{2}_{5}@P{0}_{3}_{2}_{6}@P{0}_{3}_{2}_{7}@P{0}_{3}_{2}_{8}@P{0}_{3}_{2}_{9}@P{0}_{3}_{2}_{10}));\n".format(m,
                                                                                                                                                                                                                                                                                                                                                                                                        var["and_output"],round,var["round_input"],
                                                                                                                                                                                                                                                                                                                                                                                                       i,i+1,i+2,i+3,i+4,i+5,i+6,i+7,
                                                                                                                                                                                                                                                                                                                                                                                                       j,j+1,j+2,j+3,j+4,j+5,j+6,j+7)
    return statement
def Xor_operation1(var,round,m,start):
    statement=""
    i=start//2
    j=start+8
    statement+="ASSERT(P{0}_{1}_{2}_{5}@P{0}_{1}_{2}_{6}@P{0}_{1}_{2}_{7}@P{0}_{1}_{2}_{8}@P{0}_{1}_{2}_{9}@P{0}_{1}_{2}_{10}@P{0}_{1}_{2}_{11}@P{0}_{1}_{2}_{12}=BVXOR(P{0}_{3}_{2}_{13}@P{0}_{3}_{2}_{14}@P{0}_{3}_{2}_{15}@P{0}_{3}_{2}_{16}@P{0}_{3}_{2}_{17}@P{0}_{3}_{2}_{18}@P{0}_{3}_{2}_{19}@P{0}_{3}_{2}_{20},P{0}_{4}_{2}_{5}@P{0}_{4}_{2}_{6}@P{0}_{4}_{2}_{7}@P{0}_{4}_{2}_{8}@P{0}_{4}_{2}_{9}@P{0}_{4}_{2}_{10}@P{0}_{4}_{2}_{11}@P{0}_{4}_{2}_{12}));\n".format(m,var["xor_input"],round,var["round_input"],var["and_output"],
                                                                                                                                                                                                             i,i+1,i+2,i+3,i+4,i+5,i+6,i+7,
                                                                                                                                                                                                             j,j+1,j+2,j+3,j+4,j+5,j+6,j+7)

    return statement

def Xor_operation2(var,round,m,start):
    statement=""
    i=start
    j=start//2
    k=start+32
    statement+="ASSERT(P{0}_{1}_{2}_{4}@P{0}_{1}_{2}_{5}@P{0}_{1}_{2}_{6}@P{0}_{1}_{2}_{7}@P{0}_{1}_{2}_{8}@P{0}_{1}_{2}_{9}@P{0}_{1}_{2}_{10}@P{0}_{1}_{2}_{11}=BVXOR(P{0}_{1}_{2}_{14}@P{0}_{1}_{2}_{15}@P{0}_{1}_{2}_{16}@P{0}_{1}_{2}_{17}@P{0}_{1}_{2}_{18}@P{0}_{1}_{2}_{19}@P{0}_{1}_{2}_{12}@P{0}_{1}_{2}_{13},P{0}_{3}_{2}_{20}@P{0}_{3}_{2}_{21}@P{0}_{3}_{2}_{22}@P{0}_{3}_{2}_{23}@P{0}_{3}_{2}_{24}@P{0}_{3}_{2}_{25}@P{0}_{3}_{2}_{26}@P{0}_{3}_{2}_{27}));\n".format(m,var["round_input"],round,var["xor_input"],k,k+1,k+2,k+3,k+4,k+5,k+6,k+7,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                i,i+1,i+2,i+3,i+4,i+5,i+6,i+7,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                j,j+1,j+2,j+3,j+4,j+5,j+6,j+7)

    return  statement

def Branch_operation(var,round,m,start):
    statement=""
    i=start
    j=start+8+32
    statement+="ASSERT(P{0}_{1}_{2}_{3}@P{0}_{1}_{2}_{4}@P{0}_{1}_{2}_{5}@P{0}_{1}_{2}_{6}@P{0}_{1}_{2}_{7}@P{0}_{1}_{2}_{8}@P{0}_{1}_{2}_{9}@P{0}_{1}_{2}_{10}=P{0}_{1}_{2}_{11}@P{0}_{1}_{2}_{12}@P{0}_{1}_{2}_{13}@P{0}_{1}_{2}_{14}@P{0}_{1}_{2}_{15}@P{0}_{1}_{2}_{16}@P{0}_{1}_{2}_{17}@P{0}_{1}_{2}_{18});\n".format(m,var["round_input"],round,j,j+1,j+2,j+3,j+4,j+5,j+6,j+7,i,i+1,i+2,i+3,i+4,i+5,i+6,i+7)

    return statement

def Xor_operation3(var,round,m,start,st):
    statement = ""
    st=st*8
    i = start
    j = start // 2
    k = st
    statement += "ASSERT(P{0}_{1}_{28}_{4}@P{0}_{1}_{28}_{5}@P{0}_{1}_{28}_{6}@P{0}_{1}_{28}_{7}@P{0}_{1}_{28}_{8}@P{0}_{1}_{28}_{9}@P{0}_{1}_{28}_{10}@P{0}_{1}_{28}_{11}=BVXOR(P{0}_{1}_{2}_{14}@P{0}_{1}_{2}_{15}@P{0}_{1}_{2}_{16}@P{0}_{1}_{2}_{17}@P{0}_{1}_{2}_{18}@P{0}_{1}_{2}_{19}@P{0}_{1}_{2}_{12}@P{0}_{1}_{2}_{13},P{0}_{3}_{2}_{20}@P{0}_{3}_{2}_{21}@P{0}_{3}_{2}_{22}@P{0}_{3}_{2}_{23}@P{0}_{3}_{2}_{24}@P{0}_{3}_{2}_{25}@P{0}_{3}_{2}_{26}@P{0}_{3}_{2}_{27}));\n".format(
        m, var["round_input"], round, var["xor_input"], k, k + 1, k + 2, k + 3, k + 4, k + 5, k + 6, k + 7,
        i, i + 1, i + 2, i + 3, i + 4, i + 5, i + 6, i + 7,
        j, j + 1, j + 2, j + 3, j + 4, j + 5, j + 6, j + 7,round+1)

    return statement

def Branch_operation2(var,round,m,start,st):
    statement=""
    st=st*8
    if start==32:
        j=st
        i=start
        statement+="ASSERT(P{0}_{1}_{19}_{3}@P{0}_{1}_{19}_{4}@P{0}_{1}_{19}_{5}@P{0}_{1}_{19}_{6}@P{0}_{1}_{19}_{7}@P{0}_{1}_{19}_{8}@P{0}_{1}_{19}_{9}@P{0}_{1}_{19}_{10}=P{0}_{1}_{2}_{11}@P{0}_{1}_{2}_{12}@P{0}_{1}_{2}_{13}@P{0}_{1}_{2}_{14}@P{0}_{1}_{2}_{15}@P{0}_{1}_{2}_{16}@P{0}_{1}_{2}_{17}@P{0}_{1}_{2}_{18});\n".format(m,var["round_input"],round,j,j+1,j+2,j+3,j+4,j+5,j+6,j+7,i,i+1,i+2,i+3,i+4,i+5,i+6,i+7,round+1)

    if start==48:
        j=st
        i=start
        statement+="ASSERT(P{0}_{1}_{19}_{3}@P{0}_{1}_{19}_{4}@P{0}_{1}_{19}_{5}@P{0}_{1}_{19}_{6}@P{0}_{1}_{19}_{7}@P{0}_{1}_{19}_{8}@P{0}_{1}_{19}_{9}@P{0}_{1}_{19}_{10}=P{0}_{1}_{2}_{11}@P{0}_{1}_{2}_{12}@P{0}_{1}_{2}_{13}@P{0}_{1}_{2}_{14}@P{0}_{1}_{2}_{15}@P{0}_{1}_{2}_{16}@P{0}_{1}_{2}_{17}@P{0}_{1}_{2}_{18});\n".format(m,var["round_input"],round,j,j+1,j+2,j+3,j+4,j+5,j+6,j+7,i,i+1,i+2,i+3,i+4,i+5,i+6,i+7,round+1)

    return statement





def constraint(var_str,branch,rounds,a,b):
    statement=''
    P0X=''
    P1X=''
    P0Y = ''
    P1Y = ''
    din=''
    dout = ''

    for i in range(0,branch-1):
        P0X+="P{}_{}_{}_{}@".format(0,var_str['round_input'],0,i)
        P1X += "P{}_{}_{}_{}@".format(1, var_str['round_input'], 0, i)
        P0Y += "P{}_{}_{}_{}@".format(0, var_str['round_input'], rounds, i)
        P1Y += "P{}_{}_{}_{}@".format(1, var_str['round_input'], rounds, i)
        din += "{}_{}@".format(var_str['dinput'], i)
        dout += "{}_{}@".format(var_str['doutput'], i)

    P0X+="P{}_{}_{}_{}".format(0,var_str['round_input'],0,branch-1)
    P1X += "P{}_{}_{}_{}".format(1, var_str['round_input'], 0, branch - 1)
    P0Y += "P{}_{}_{}_{}".format(0, var_str['round_input'], rounds, branch-1)
    P1Y += "P{}_{}_{}_{}".format(1, var_str['round_input'], rounds, branch-1)
    din += "{}_{}".format(var_str['dinput'], branch-1)
    dout += "{}_{}".format(var_str['doutput'], branch - 1)

    statement+='ASSERT({0}=BVXOR({1},{2}));\n'.format(din,P0X,P1X)
    statement += 'ASSERT({0}=BVXOR({1},{2}));\n'.format(dout, P0Y, P1Y)
    statement+='ASSERT({0}=0bin{1});\n'.format(din,a)
    statement += 'ASSERT({0}=0bin{1});\n'.format(dout, b)

    return statement





# if __name__ == "__main__":





















