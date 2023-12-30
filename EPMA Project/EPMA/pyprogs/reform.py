from os import listdir

def m2p(x):
    return(x*2.83465)

def number(x):
    return(int(x) if x==int(x) else x)

def main():
    files = listdir()
    file = "95_22_6.svg" # replace this line by a for loop (i.e.) for file in files:

    writeList = []

    with open(f"./{file}","r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.replace('"','$')
        if(("width=$" in line) and ("mm$" in line) and ("inkscape" not in line) and ("stroke" not in line)):
            before = line[:line.index("=$")+2]
            after = line[line.index("mm$"):].replace("mm","pt")
            w = line[line.index("=$")+2:]
            w = w[:w.index("mm$")]
            line = (before + str(number(m2p(float(w)))) + after)
        elif(("height=$" in line) and ("mm$" in line) and ("inkscape" not in line) and ("stroke" not in line)):
            before = line[:line.index("=$")+2]
            after = line[line.index("mm$"):].replace("mm","pt")
            w = line[line.index("=$")+2:]
            w = w[:w.index("mm$")]
            line = (before + str(number(m2p(float(w)))) + after)
        elif("viewBox" in line):
            before = line[:line.index("viewBox=$0 0 ")+13]
            after = "$\n"
            x,y = (line[line.index("viewBox=$0 0 ")+13:line.index("$\n")]).split(" ")
            x = str(number(m2p(float(x))))
            y = str(number(m2p(float(y))))
            line = f"{before}{x} {y}{after}"
        elif("transform=$translate" in line):
            before = line[:line.index("(")+1]            
            after = line[line.index(")"):]
            x,y = (line[line.index("(")+1:line.index(")")]).split(",")
            x = str(number(m2p(float(x))))
            y = str(number(m2p(float(y))))
            line = f"{before}{x},{y}{after}"
        elif(("cx=$" in line) and ("inkscape" not in line)):
            before = line[:line.index("$")+1]
            cx = line[line.index("$")+1:]
            after = cx[cx.index("$"):]
            cx = cx[:cx.index("$")]
            line = before+str(number(m2p(float(cx))))+after
        elif(("cy=$" in line) and ("inkscape" not in line)):
            before = line[:line.index("$")+1]
            cy = line[line.index("$")+1:]
            after = cy[cy.index("$"):]
            cy = cy[:cy.index("$")]
            line = before+str(number(m2p(float(cy))))+after
        elif(("r=$" in line) and ("inkscape" not in line) and ("color" not in line)):
            before = line[:line.index("$")+1]
            r = line[line.index("$")+1:]
            after = r[r.index("$"):]
            r = r[:r.index("$")]
            line = before+str(number(m2p(float(r))))+after

        writeList.append(line.replace("$",'"'))

    with open(f"./{file}","w") as f:
        f.write(''.join(writeList))

main()

'''
Solution convert all handmade svg to pts
this includes 

                width 
                height
                viewBox
                transform values
cx
cy
r
'''