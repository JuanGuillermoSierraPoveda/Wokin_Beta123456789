import sys
def TuringMachine(states,input,start,alph):
    i=0
    actval=input[i]
    insidealph(actval,alph)
    puntos=0
    lop=True
    actval1=""
    change=False
    startcheck=""
    cont=0
    lista=[]
    while lop:
        lista.append(start)

        if start==startcheck:
            cont=cont+1
        else:
            cont=0

        if cont==10:
            print("No hay caminos disponibles")
            return lista
        
        if states[start]=="E":
                print("Resultado estado final")
                print(input)
                return lista,puntos
        #print("iteracion")
        if change:
            actval=actval1
            change=False
        startcheck=start
        input,start,actval,i,change,actval1,puntos=TuringLoop(states,input,start,alph,actval,i,change,puntos)
            
def TuringLoop(states,input,start,alph,actval,i,change,puntos):
    
    valu=["q01","q02","q34","q01nd"]
    actval1=""
    try:
        conde=len(states[start][actval])
    except KeyError:
        print("e")
        print(input)
        return
    for x in range(0,len(states[start][actval])):#start es el estado ejecutando, actval el valor activo
        print("\n",input,start,"valor",actval,"iteracion",x,"indice",i)
        
        if start in valu:
            #print("Hm?",start,actval,type(states[start][actval]))
            if states[start][actval]==['R'] or states[start][actval]==['L']:
                print("Resta")
                puntos=puntos-1

        try:
            debu=states[start][actval][x]
        except IndexError:
            print("Resultado final","e")
            print(input)
            return
        
        if states[start][actval][x] in states:
            #print("s")
            start=states[start][actval][x]
            if actval1!="":
                actval=actval1
            return input,start,actval,i,change,actval1,puntos

        if states[start][actval][x]=="w":
            #print("w",states[start][actval][x+1])
            #print("w")
            input=replacement(input,i,states[start][actval][x+1])
            #print(input)
            insidealph(actval,alph)
            if states[start][actval][-1] in states:
                actval1=blankswap(input,i)
            else:
                actval=blankswap(input,i)
        
        elif states[start][actval][x]=="R":
            #print("r")
            if states[start][actval][x]!=states[start][actval][-1]:# Si L Q1
                i=i+1
                insidealph(actval,alph)
                actval1=blankswap(input,i)
                #print("r especial")
                change=True
            else:#Si L
                i=i+1
                insidealph(actval,alph)
                actval=blankswap(input,i)

        elif states[start][actval][x]=="L":
            #print("l")

            if states[start][actval][x]!=states[start][actval][-1]:# Si L Q1
                i=i-1
                insidealph(actval,alph)
                actval1=blankswap(input,i)
                #print("l especial")
                change=True
            else:#Si L
                i=i-1
                insidealph(actval,alph)
                actval=blankswap(input,i)

    return input,start,actval,i,change,actval1,puntos

def blankswap(input,index):#input es el dato inicial, dat1 es el indice actual
    datoactual=""
    try:
        input[index]
    except IndexError:
        datoactual="_"
    else:
        datoactual=input[index]

    return datoactual #retorna el dato actualmente usado

def insidealph(value,alph):
    if value in alph:
        return
    else:
        print("El valor no esta en el alfabeto")
        return

def replacement(input,index,val):
    ninp=""
    added=""
    if index<0:
        for y in range(0,abs(index)):
            print(y)
            if y==0:
                ninp=val
            else:
                added=added+"_"
        ninp=val+added
        index=index-len(input)
            
    elif index>(len(input)-1):
        for y in range(0,(index-(len(input)-1))):
            if y==(index-(len(input))):
                ninp=val
            else:
                added=added+"_"
        ninp=added+ninp
    for x in range(0,len(input)):#input 1001, etc
        try:
            vo=input[index]
        except IndexError:
            if index<0:
                ninp=ninp+input
                return ninp
            elif index>(len(input)-1):
                ninp=input+ninp
                return ninp
        else:
            if x==index:
                ninp=ninp+val
            else:
                ninp=ninp+input[x]
    return ninp
if __name__ == "__main__":
    #Ejemplo inicial, suma +1 binario
    states={
        "q0":{"0":["R"],"1":["R"],"_":["L","q1"]},
        "q1":{"1":["w","0","L"],"0":["w","1","L","qf"],"_":["w","1","L","qf"]},
        "qf":"E"}
    #states={
    #    "q0":{"0":["R"],"1":["R","q1"],"_":["R","qf"]},
    #    "q1":{"0":["R","q2"],"1":["R","q0"],"#":["R"]},
    #    "q2":{"0":["R","q1"],"1":["R"],"#":["R"]},
    #    "qf":"E"}
    input="10"
    start="q0" 
    alph=["0","1","_","#"]
    print("inicio")
    TuringMachine(states,input,start,alph)
