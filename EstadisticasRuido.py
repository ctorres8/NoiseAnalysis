# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 19:51:32 2021

@author: crist
"""

"""

** Baseline Wander **

Source: record nstdb/bw
val has 2 rows (signals) and 650000 columns (samples/signal)
Duration:    30:05
Sampling frequency: 360 Hz  Sampling interval: 0.002777777778 sec
Row	Signal	Gain	Base	Units
1	noise1	200	     0	     mV
2	noise2	200	     0	     mV

------------------------------------------

** Electrode Movement **

Source: record nstdb/em
val has 2 rows (signals) and 650000 columns (samples/signal)
Duration:    30:05
Sampling frequency: 360 Hz  Sampling interval: 0.002777777778 sec
Row	Signal	Gain	Base	Units
1	noise1	200	     0	     mV
2	noise2	200	     0	     mV

------------------------------------------

** Motion Artifacts **

Source: record nstdb/ma
val has 2 rows (signals) and 650000 columns (samples/signal)
Duration:    30:05
Sampling frequency: 360 Hz  Sampling interval: 0.002777777778 sec
Row	Signal	Gain	Base	Units
1	noise1	200	     0	     mV
2	noise2	200	     0	     mV

"""


import numpy as np
from scipy import signal as sig
import matplotlib.pyplot as plt
import scipy.io as sio
import pandas as pd
#import os

bw = sio.loadmat('bwm.mat')['val']
em = sio.loadmat('emm.mat')['val']
ma = sio.loadmat('mam.mat')['val']

"""
df_bw = pd.DataFrame(data=bw,index=['BW0','BW1'])
df_em = pd.DataFrame(data=em,index=['EM0','EM1'])
df_ma = pd.DataFrame(data=ma,index=['MA0','MA1'])

df_bw_mean = df_bw.mean(axis=1)
df_em_mean = df_em.mean(axis=1)
df_ma_mean = df_ma.mean(axis=1)

df_bw_mem = df_bw.abs().mean(axis=1)
df_em_mem = df_em.abs().mean(axis=1)
df_ma_mem = df_ma.abs().mean(axis=1)

#asd = df_bw.loc['BW0']

df_bw_std = df_bw.std(axis=1)
df_em_std = df_em.std(axis=1)
df_ma_std = df_ma.std(axis=1)

df_bw_var = df_bw.var(axis=1)
df_em_var = df_em.var(axis=1)
df_ma_var = df_ma.var(axis=1)
"""

fs = 360#Hz


#Media
bw_mean=[]
bw_mean.append(bw[0].mean())
bw_mean.append(bw[1].mean())

#bw_mean = [bw[0].mean(),bw[1].mean()]

em_mean=[]
em_mean.append(em[0].mean())
em_mean.append(em[1].mean())

ma_mean=[]
ma_mean.append(ma[0].mean())
ma_mean.append(ma[1].mean())

media =[bw_mean[0],bw_mean[1],em_mean[0],em_mean[1],ma_mean[0],ma_mean[1]]

#Media Absoluta
bw_absmean=[]
bw_absmean.append(abs(bw[0]).mean())
bw_absmean.append(abs(bw[1]).mean())

em_absmean=[]
em_absmean.append(abs(em[0]).mean())
em_absmean.append(abs(em[1]).mean())

ma_absmean=[]
ma_absmean.append(abs(ma[0]).mean())
ma_absmean.append(abs(ma[1]).mean())

####################

# Desviacion Standard

bw_std=[]
bw_std.append(bw[0].std())
bw_std.append(bw[1].std())

em_std=[]
em_std.append(em[0].std())
em_std.append(em[1].std())

ma_std=[]
ma_std.append(ma[0].std())
ma_std.append(ma[1].std())

std = [bw_std[0],bw_std[1],em_std[0],em_std[1],ma_std[0],ma_std[1]]
###################################

#Varianza

bw_var=[]
bw_var.append(bw[0].var())
bw_var.append(bw[1].var())

em_var=[]
em_var.append(em[0].var())
em_var.append(em[1].var())

ma_var=[]
ma_var.append(ma[0].var())
ma_var.append(ma[1].var())

####################################


filas =['BW0','BW1','EM0','EM1','MA0','MA1']

df = pd.DataFrame({'Media':media,
                   'STD':std
                   },index=filas)
#df = pd.DataFrame(data=datas,index=filas,columns=['Media','STD'])

#####################################

t1=80000
t2=200000

bw_w = bw[0][t1:t2+1],bw[1][t1:t2+1]
em_w = em[0][t1:t2+1],em[1][t1:t2+1]
ma_w = ma[0][t1:t2+1],ma[1][t1:t2+1]

n_win = len(bw_w)

n=14

Fxx_bw0,Pxx_bw0=sig.welch(bw_w[0],fs,window='hanning',nperseg=2**n,noverlap=(2**n)/4, nfft=2*(2**n))
Fxx_bw1,Pxx_bw1=sig.welch(bw_w[1],fs,window='hanning',nperseg=2**n,noverlap=(2**n)/4, nfft=2*(2**n))

Fxx_em0,Pxx_em0=sig.welch(em_w[0],fs,window='hanning',nperseg=2**n,noverlap=(2**n)/4, nfft=2*(2**n))
Fxx_em1,Pxx_em1=sig.welch(em_w[1],fs,window='hanning',nperseg=2**n,noverlap=(2**n)/4, nfft=2*(2**n))

Fxx_ma0,Pxx_ma0=sig.welch(ma_w[0],fs,window='hanning',nperseg=2**n,noverlap=(2**n)/4, nfft=2*(2**n))
Fxx_ma1,Pxx_ma1=sig.welch(ma_w[1],fs,window='hanning',nperseg=2**n,noverlap=(2**n)/4, nfft=2*(2**n))


"""
plt.figure("Densidad de potencia BW Noise")

plt.plot(Fxx_bw0,Pxx_bw0,label ='Potencia BW0')
plt.plot(Fxx_bw1,Pxx_bw1,label ='Potencia BW1')

plt.xlim(0,2,0.1)
plt.title('DEP')
plt.xlabel('Frecuencia')
plt.ylabel('Amplitud ')
plt.grid(which='both', axis='both')

axes_dep_bw = plt.gca()
axes_dep_bw.legend()




plt.figure("Densidad de potencia EM Noise")

plt.plot(Fxx_em0,Pxx_em0,label ='Potencia EM0')
plt.plot(Fxx_em1,Pxx_em1,label ='Potencia EM1')

plt.xlim(0,10,0.1)
plt.title('DEP')
plt.xlabel('Frecuencia')
plt.ylabel('Amplitud ')
plt.grid(which='both', axis='both')

axes_dep_em = plt.gca()
axes_dep_em.legend()


plt.figure("Densidad de potencia MA Noise")

plt.plot(Fxx_ma0,Pxx_ma0,label ='Potencia MA0')
plt.plot(Fxx_ma1,Pxx_ma1,label ='Potencia MA1')

plt.xlim(0,3,0.1)
plt.title('DEP')
plt.xlabel('Frecuencia')
plt.ylabel('Amplitud ')
plt.grid(which='both', axis='both')

axes_dep_ma = plt.gca()
axes_dep_ma.legend()
"""
#plt.figure("Baseline Wander")
#plt.plot(bw[0],label="BW Noise")
#plt.grid(True)