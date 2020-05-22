import numpy as np
import matplotlib.pyplot as plt
import sys

from numba import jit,njit,float64,int32
import numba as nb

var = np.loadtxt('inputs.txt', delimiter=',')
n = int(var[0])
yr = var[1]
kr = var[2]
yp = var[3]
kp = var[4]
tmax = var[5]
@njit(nb.types.UniTuple(float64[:],2)(float64[:],float64[:],float64))
def promedios(xarg,yarg,dx):
    a=np.min(xarg)
    b=np.max(xarg)
    imax=0
    while (a+(imax+1)*dx < b):
        imax+=1
    
    promediosx=np.zeros(imax)
    promediosy=np.zeros(imax)
    for i in range(imax):
        mask=np.logical_and(a+i*dx<=xarg,xarg<=a+(i+1)*dx)
        promediosx[i]=np.mean(xarg[mask])
        promediosy[i]=np.mean(yarg[mask])
    return (promediosx,promediosy)

@njit
def Gillespie(γr, kr, γp, kp,tmax):
    p = [0.0]
    r = [0.0]
    t = [0.0]
    i = 0
    while t[i] <= tmax:
        s2 = γr*r[i]
        s3 = kp*r[i]
        s4 = γp*p[i]
        st = kr+s2+s3+s4
        τ = (-1/st)*np.log(np.random.rand())
        x = np.random.rand()
        if(x< kr/st):
            r.append(r[i]+1.0)
            p.append(p[i])
        elif(x < (kr+s2)/st):
            r.append(r[i]-1.0)
            p.append(p[i])
        elif(x<(kr+s2+s3)/st):
            r.append(r[i])
            p.append(p[i]+1.0)
        else:
            r.append(r[i])
            p.append(p[i]-1.0)
        t.append(t[i]+τ)
        i += 1
    return(t,p,r)

células = 300

T = []
P = []
R = []

for i in range(n):
    (t,p,r) = Gillespie(yr,kr,yp,kp,tmax)
    T.append(t)
    P.append(p)
    R.append(r)
    
(pt,pr) =  promedios(np.concatenate(T),np.concatenate(R), 2.0)
(pt,pp) =  promedios(np.concatenate(T),np.concatenate(P), 2.0)
fig,ax=plt.subplots(2,sharex=True, figsize=(12,12))
plt.xlabel('tiempo (UA)')
ax[0].set_title('Concentración en el tiempo')
for i in range(40 if n>40 else n):
    ax[0].step(T[i],R[i],alpha=0.2)
    ax[1].step(T[i],P[i],alpha=0.2)
ax[0].set_ylabel('[RNAm] (\u03BCM)')
ax[1].set_ylabel('[Proteínas] (\u03BCM)')
ax[0].plot(pt,pr, color='k')
ax[1].plot(pt,pp, color='k')
plt.savefig('Concentracion.png')

mask=55<=np.concatenate(T)
Rdata=np.concatenate(R)[mask]

fig = plt.figure(figsize=(12,12))
plt.title("Frecuencia de concentraciones RNAm")
plt.hist(Rdata,100);
plt.xlabel('[RNAm] (\u03BCM)')
plt.savefig('cRNA.png')
print(np.mean(Rdata))
print(np.std(Rdata))
print(np.std(Rdata)/np.mean(Rdata))

fig = plt.figure(figsize=(12,12))
Pdata=np.concatenate(P)[mask]
plt.hist(Pdata,100);
plt.title("Frecuencia de concentraciones Proteínas")
plt.xlabel('[Proteínas] (\u03BCM)')
plt.savefig('cProt.png')
print(np.mean(Pdata))
print(np.std(Pdata))
print(np.std(Pdata)/np.mean(Pdata))