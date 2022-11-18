# -*- coding: utf-8 -*-
# @Time : 2022/1/2 16:39
# @Author : hhq
# @File : IGA_storagetank.py
import copy
import random
N = random.choice([3, 4])  # 贮箱种类
u = [6, 8]
def init_num_N(N,u):  # 初始化各贮箱数量
    num_N=[]
    for i in range(N):
        num_N.append(random.choice(u))
    return num_N
M = random.choice([4,5])  # kinds of machines
m = [1, 2]
def init_num_M(M,m):  # initialize the machine num of each kind
    num_M = {}
    for j in range(M):
        num_M[j] = random.choice(m)
    return num_M

max_Parts = 5
def init_storage_part(N,max_Parts):  # 初始化各种贮箱包含的组件数量比例
    s_P = {}
    for i in range(N):
        part_r = []
        for j in range(3):
            part_r.append(random.randint(1,max_Parts))
        s_P[i] = part_r
    return s_P

# 工序数给定为4，随机选出4台机器作为加工位置
def init_operation(num_N, s_P,M):
    ope_ma, t_table = [], []
    for i in range(len(num_N)):
        ma_list = []  # 同贮箱组件的全部工序，初始化为一个矩阵，行数表示组件数量
        sub_t_table = []  # 同贮箱组件的全部工序加工时间
        for part_no in range(len(s_P[i])):  # 三种组件的数量 # 每种组件的数量初始化为一个矩阵，表示其特有的加工路线
            t_list = [random.randint(1, 30) for j in range(M)]  # 各工序加工时间初始化
            list_ma = list(range(M))
            random.shuffle(list_ma)
            for j in range(s_P[i][part_no]):  # 对每种组件进行加工位置初始化，每种组件数量不一定为1，part_list[no_p]
                ma_list.append(list_ma)  # 行数表示该种组件数量，列数表示工序数或机器位置
                sub_t_table.append(t_list)
        for k in range(num_N[i]):  # 表示贮箱i的数量
            ope_ma.append(ma_list)
            t_table.append(sub_t_table)
    return ope_ma, t_table
# num_N = init_num_N(N,u)
# num_M = init_num_M(M,m)
# s_P = init_storage_part(N,max_Parts)
# ope_ma, t_table = init_operation(num_N,s_P,M)
print()
def init_t_table(ope_ma):
    t_table = copy.deepcopy(ope_ma)
