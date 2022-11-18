
import numpy as np
def update_AK(A0, r0, K, t):  # 更新参数
    A = K/(1+(K/A0-1)*np.exp(-r0*t))
    r = r0*(1-A/K)
    return A, r
A0=100
r0=0.015
K=10000
sita = 0.95
A=A0
r=r0
t=1
while A<sita*K:
    A,r = update_AK(A0,r0,K,t)
    t+=1
print(t)