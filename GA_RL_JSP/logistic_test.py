# -*- coding: utf-8 -*-
# @Time : 2022/1/3 19:34
# @Author : hhq
# @File : logistic_test.py
import numpy as np

A0=100
K=10000
r0=0.015
nita=0.95
A=A0
r=r0
t=1
def update_AK(A0, r0, K, t):  # 更新参数
    A = K/(1+(K/A0-1)*np.exp(-r0*t))
    r = r0*(1-A/K)

    return A, r
while A<nita*K:
    t+=1
    A,r = update_AK(A0,r0,K,t)
print(t)