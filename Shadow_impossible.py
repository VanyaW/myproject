
PP=['2103'] #the permutation
import time
import os
import dcp_model as Shadow
import math
import signal


def find_impossible_differential(cd):
    statement=''
    var_str = {
        "round_input": "x",
        "and_output":"z",
        "xor_input":"r",
        "dinput": "din",
        "doutput": "dout",

    }
    x=[]
    z=[]
    r=[]

    for ml in range(cd["ch"]):
        x.append(["P{}_{}_{}_{}".format(ml, "x", i, j) for i in range(cd["rounds"] + 1) for j in range(cd["branch"]*2)])
        z.append(["P{}_{}_{}_{}".format(ml, "z", i, j) for i in range(cd["rounds"]) for j in range(cd["branch"])])
        r.append(["P{}_{}_{}_{}".format(ml, "r", i, j) for i in range(cd["rounds"]) for j in range(cd["branch"])])
    din = ["{}_{}".format("din", i) for i in range(cd["branch"])]
    dout = ["{}_{}".format("dout", i) for i in range(cd["branch"])]

    #setup variable bitnum-1bit
    for ml in range(cd["ch"]):
        statement += Shadow.setupVariables(x[ml], 1)
        statement += Shadow.setupVariables(z[ml], 1)
        statement += Shadow.setupVariables(r[ml], 1)
    statement += Shadow.setupVariables(din, 1)
    statement += Shadow.setupVariables(dout, 1)



    for rou in range(cd["rounds"]):
        for ml in range(cd["ch"]):
            ii = 0
            ij = 1
            for start in range(0,cd["branch"]*2,16): #notice x is 64bit ,z and r is 32 bit
                statement+=Shadow.And_operation(var_str,rou,ml,start) #include shift operation
                statement+=Shadow.Xor_operation1(var_str,rou,ml,start) #the fist XOR opeartion
                if start<=16:
                    statement+=Shadow.Xor_operation2(var_str,rou,ml,start)
                    statement+=Shadow.Branch_operation(var_str,rou,ml,start)
                if start>16:
                    statement+=Shadow.Branch_operation2(var_str,rou,ml,start,int(cd["per"][ii]))
                    statement += Shadow.Xor_operation3(var_str, rou, ml, start,int(cd["per"][ij]))
                    ii+=2
                    ij+=2

    statement += Shadow.constraint(var_str, cd["branch"], cd["rounds"],cd["a"],cd["b"])
    statement += Shadow.setupQuery()

    if os.path.exists(cd["solve_file"]):
        os.remove(cd["solve_file"])
    f = open(cd["solve_file"], "w")
    f.write(statement)
    f.close()



if __name__ == "__main__":
    start=time.time()
    cd = dict()
    cd["ch"]=2
    cd["branch"]=32

    Space = ['' for j in range(cd["branch"])]
    tu = '00000000000000000000000000000000'
    Space[0] = '10000000000000000000000000000000'

    for i in range(1, cd["branch"]):
        Space[i] = tu[:i] + '1' + tu[i + 1:]

    for k in range(0,1):

        cd["per"] = PP[k] ##the permutation

        cd["structure"] = "Shadow_{0}".format(cd["per"])
        folder = cd["structure"]
        if not os.path.exists(folder):
            os.mkdir(folder)
        cd["record_file"] = folder + "////" + cd["structure"] + "_result_{0}.txt".format(cd["per"])


        all_rounds = 17

        for rou in range(1, all_rounds):
            start2=time.time()
            tag = 0
            cd["rounds"] = rou
            cd["solve_file"] = folder + "////" + cd["structure"] + "_rou{}.stp".format(rou)

            for i in range(len(Space)):
                for j in range(len(Space)):
                    cd["a"] = Space[i]
                    cd["b"] = Space[j]

                    find_impossible_differential(cd)
                    fl, res = Shadow.solver1(cd["solve_file"])


                    if not fl:
                        continue
                    if fl:
                        tag = 1
                        end = time.time()
                        print(
                            '****************************************found one of {} rounds*******************************!!!\n'.format(
                                rou))
                        f2 = open(cd["record_file"], "a")
                        f2.write("Using the permutation of {0},\na impossible differential of {1} rounds is {2} and {3},\nthe time is {4}.\n".format(cd["per"],
                                                                                                                                                    rou,Space[i],Space[j],
                                                                                                                                                    end-start2))

                    if tag == 1: break
                if tag == 1: break
















