import random

def _weighted1(S,a,yn_1=0):
    xn=random.random()
    yn=sum([int(xn<=((a*k)/(S-1))) for k in range(1,S)])+yn_1
    yn%=S
    return yn

def weighted1(N,S,a,yn_1=0):
    y=[]
    for n in range(N):
        yn_1=_weighted1(S,a,yn_1=yn_1)
        y.append(yn_1)
    return y
    
    
