from TuringMachine import TuringMachine

def otcamino(x,y,f):
    if y=="q1":
        return {"M":["R",x],"V":["L",x],"P":["R"],"S":["L"]}
    elif y=="q2":
        return {"P":["R",x],"S":["L",x],"M":["R"],"V":["L"]}
    elif y=="q3":
        return {"P":["R",x],"V":["L",x],"M":["R"],"S":["L"]}
    
def camino(x,y):
    if y=="q01":
        return {"M":["R",x],"V":["L",x],"P":["R"],"S":["L"]}
    elif y=="q02":
        return {"P":["R",x],"S":["L",x],"M":["R"],"V":["L"]}
    elif y=="q34":
        return {"P":["R",x],"V":["L",x],"M":["R"],"S":["L"]}
    
def distancia(lista,listaestados,dist):
    v1=""
    v2=""
    di=0
    for x in lista:
        if x in listaestados:
            if v1!="" and x!=v1:
                v2=x
                di=di+dist[v1][v2]
                v1=v2
                v2=""
            else:
                v1=x
    return di
    


#M=Empinado,P=plano,V=con vista,S=Sin vista
f=""
salida=""
candist=[]
puntos=0
alph=("M","V","P","S","_")
listaestados=["q0","q1","q2","q3","q4"]
dist={"q0":{"q1":230,"q2":1000},
      "q1":{"q0":230,"q3":700,},
      "q3":{"q1":700,"q2":25},
      "q2":{"q0":1000,"q3":25,"q4":20},
      "q4":{"q3":20}}


start="q0"
f="q4"
input="PV"







#q0 a q4
vals=["q2","q1"]
for x in vals:

    states={

        "q0":otcamino("q01","q1",f),
        "q1":otcamino("q01nd","q1",f),
        "q2":otcamino("q02","q2",f),
        "q3":otcamino("q34","q3",f),
        "q4":otcamino("q34","q3",f),
        "q01":camino(x,"q01"),
        "q01nd":camino("q3","q01"),
        "q02":camino("q4","q02"),
        "q34":camino("q2","q34")

    }
    states[f]="E"
    #print(states,"\n")
    lista,puntos=TuringMachine(states,input,start,alph)
    print(lista,puntos)
    candist.append(distancia(lista,listaestados,dist))

print(candist)
    


    


#q1={"M":["R","q01"],"V":["L","q01"],"P":["R"],"S":[f]}#q0,q1
#q2={"P":["R","q02"],"S":["L","q2"],"M":["R"],"V":[f]}#q2
#q3={"P":["R","q34"],"V":["L","q34"],"M":["R"],"S":[f]}#q3,q4
#q01={"M":["R"],"V":["L",x],"P":["R"],"S":["L"]}#q0,q1
#q34={"P":["R"],"V":["L",x],"M":["R"],"S":["L"]}#q3,q4
#q02={"P":["R"],"S":["L",x],"M":["R"],"V":["L"]}#q2  