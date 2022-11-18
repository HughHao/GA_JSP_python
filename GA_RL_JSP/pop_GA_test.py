# -*- coding: utf-8 -*-
# @Time : 2022/1/2 12:45
# @Author : hhq
# @File : pop_GA_test.py
import copy
import datetime
import numpy as np
import random
import re
import matplotlib.pyplot as plt
import math
from matplotlib import rcParams

jobs = 6  # 工件数
machines = 6  # 机器数
t_table = [[1, 3, 6, 7, 3, 6], [8, 5, 10, 10, 10, 4], [5, 4, 8, 9, 1, 7], [5, 5, 5, 3, 8, 9], [9, 3, 5, 4, 3, 1],
           [3, 3, 9, 10, 4, 1]]
# 加工位置初始化，每个工序一个位置
m_table = [[3, 1, 2, 4, 6, 5], [2, 3, 5, 6, 1, 4], [3, 4, 6, 1, 2, 5], [2, 1, 3, 4, 5, 6], [3, 2, 5, 6, 1, 4],
           [2, 4, 6, 1, 5, 3]]


# jobs = 10  # 工件数
# machines = 10  # 机器数
# # [['c2_1_1', [0.0, 43.0]], ['c8_1_3', [0.0, 31.0]], ['c4_1_2', [0.0, 81.0]], ['c7_1_2', [81.0, 127.0]], ['c9_1_1', [43.0, 119.0]], ['c2_2_3', [43.0, 133.0]], ['c8_2_1', [119.0, 205.0]], ['c1_1_1', [205.0, 234.0]], ['c4_2_3', [133.0, 228.0]], ['c9_2_2', [127.0, 196.0]], ['c6_1_3', [228.0, 312.0]], ['c8_3_2', [205.0, 251.0]], ['c1_2_2', [251.0, 329.0]], ['c5_1_3', [312.0, 326.0]], ['c9_3_4', [196.0, 272.0]], ['c7_2_1', [234.0, 271.0]], ['c2_3_5', [133.0, 208.0]], ['c4_3_1', [271.0, 342.0]], ['c5_2_1', [342.0, 348.0]], ['c7_3_4', [272.0, 333.0]], ['c4_4_5', [342.0, 441.0]], ['c6_2_2', [329.0, 331.0]], ['c8_4_6', [251.0, 325.0]], ['c2_4_10', [208.0, 219.0]], ['c6_3_6', [331.0, 383.0]], ['c3_1_2', [331.0, 422.0]], ['c7_4_3', [333.0, 346.0]], ['c7_5_7', [346.0, 378.0]], ['c5_3_2', [422.0, 444.0]], ['c7_6_6', [383.0, 404.0]], ['c7_7_10', [404.0, 436.0]], ['c4_5_7', [441.0, 450.0]], ['c9_4_6', [404.0, 455.0]], ['c9_5_3', [455.0, 540.0]], ['c1_3_3', [540.0, 549.0]], ['c10_1_2', [444.0, 529.0]], ['c8_5_5', [441.0, 473.0]], ['c6_4_4', [383.0, 478.0]], ['c10_2_1', [529.0, 542.0]], ['c2_5_4', [478.0, 547.0]], ['c8_6_7', [473.0, 561.0]], ['c4_6_9', [450.0, 502.0]], ['c10_3_3', [549.0, 610.0]], ['c1_4_4', [549.0, 585.0]], ['c5_4_6', [455.0, 516.0]], ['c9_6_10', [540.0, 551.0]], ['c9_7_7', [561.0, 601.0]], ['c7_8_9', [502.0, 591.0]], ['c2_6_2', [547.0, 575.0]], ['c10_4_7', [610.0, 617.0]], ['c1_5_5', [585.0, 634.0]], ['c8_7_9', [591.0, 610.0]], ['c4_7_8', [502.0, 587.0]], ['c7_9_8', [591.0, 621.0]], ['c6_5_9', [610.0, 658.0]], ['c3_2_1', [542.0, 627.0]], ['c5_5_4', [585.0, 611.0]], ['c8_8_10', [610.0, 658.0]], ['c3_3_4', [627.0, 666.0]], ['c10_5_9', [658.0, 722.0]], ['c3_4_3', [666.0, 740.0]], ['c4_8_4', [666.0, 764.0]], ['c2_7_7', [617.0, 663.0]], ['c6_6_10', [658.0, 730.0]], ['c5_6_5', [634.0, 703.0]], ['c9_8_8', [621.0, 710.0]], ['c10_6_10', [730.0, 806.0]], ['c1_6_6', [634.0, 645.0]], ['c9_9_5', [710.0, 736.0]], ['c6_7_1', [730.0, 777.0]], ['c5_7_9', [722.0, 743.0]], ['c8_9_8', [710.0, 746.0]], ['c4_9_10', [806.0, 828.0]], ['c1_7_7', [663.0, 725.0]], ['c6_8_7', [777.0, 842.0]], ['c10_7_6', [806.0, 853.0]], ['c3_5_9', [743.0, 833.0]], ['c1_8_8', [746.0, 802.0]], ['c3_6_6', [853.0, 863.0]], ['c5_8_8', [802.0, 851.0]], ['c6_9_5', [842.0, 848.0]], ['c8_10_4', [764.0, 843.0]], ['c10_8_4', [853.0, 905.0]], ['c7_10_5', [848.0, 903.0]], ['c2_8_6', [863.0, 909.0]], ['c1_9_9', [833.0, 877.0]], ['c5_9_10', [851.0, 923.0]], ['c3_7_8', [863.0, 875.0]], ['c6_10_8', [875.0, 900.0]], ['c9_10_9', [877.0, 951.0]], ['c2_9_8', [909.0, 981.0]], ['c4_10_6', [909.0, 952.0]], ['c3_8_7', [875.0, 964.0]], ['c2_10_9', [981.0, 1011.0]], ['c10_9_5', [905.0, 995.0]], ['c3_9_10', [964.0, 1009.0]], ['c5_10_7', [964.0, 1017.0]], ['c3_10_5', [1009.0, 1042.0]], ['c1_10_10', [1009.0, 1030.0]], ['c10_10_8', [995.0, 1040.0]]]
#
# t_table = [[29,78,9,36,49,11,62,56,44,21],[43,90,75,11,69,28,46,46,72,30],[91,85,39,74,90,10,12,89,45,33],
#            [81,95,71,99,9,52,85,98,22,43],[14,6,22,61,26,69,21,49,72,53],[84,2,52,95,48,72,47,65,6,25],
#            [46,37,61,13,32,21,32,89,30,55],[31,86,46,74,32,88,19,48,36,79],[76,69,76,51,85,11,40,89,26,74],
#            [85,13,61,7,64,76,47,52,90,45]]
# m_table = [[1,2,3,4,5,6,7,8,9,10],[1,3,5,10,4,2,7,6,8,9],[2,1,4,3,9,6,8,7,10,5],[2,3,1,5,7,9,8,4,10,6],
#            [3,1,2,6,4,5,9,8,10,7],[3,2,6,4,9,10,1,7,5,8],[2,1,4,3,7,6,10,9,8,5],[3,1,2,6,5,7,9,10,8,4],
#            [1,2,4,6, 3, 10,7,8,5,9],[2,1,3,7,9,10,6,4,5,8]]
# jobs = 20
# machines = 5
#
# t_table = [[29,9,49,62,44],[43,75,69,46,72],[91,39,90,12,45],[81,71,9,85,22],[14,22,26,21,72],[84,52,48,47,6],
#            [46,61,32,32,30],[31,46,32,19,36],[76,76,85,40,26],[85,61,64,47,90],[78,36,11,56,21],[90,11,28,46,30],
#            [85,74,10,89,33],[95,99,52,98,43],[6,61,69,49,53],[2,95,72,65,29],[37,13,21,89,55],[86,74,88,48,79],
#            [69,51,11,89,74],[13,7,76,52,45]]
# m_table = [[1,2,3,4,5],[1,2,4,3,5],[2,1,3,5,4],[2,1,5,3,4],[3,2,1,4,5],[3,2,5,1,4],[2,1,3,4,5],[3,2,1,4,5],
#            [1,4,3,2,5],[2,3,1,4,5],[2,4,1,5,3],[3,1,2,4,5],[1,3,2,4,5],[3,1,2,4,5],[1,2,5,3,4],[2,1,4,5,3],
#            [1,3,2,4,5],[1,2,5,3,4],[2,3,1,4,5],[1,2,3,4,5]]
# 处理以上数据为染色体形式，一行只含有工序不含机器
# from case_generated import jobs, machines, m_table, t_table
# jobs = 6
# machines = 6
# t_table = [[10, 43, 18, 94, 42, 9], [64, 83, 49, 14, 89, 90], [62, 32, 1, 11, 3, 26], [4, 33, 5, 87, 88, 2], [93, 10, 66, 22, 51, 83], [1, 30, 26, 92, 46, 51]]
# m_table = [[2, 6, 1, 3, 5, 4], [6, 5, 1, 3, 4, 2], [4, 5, 3, 6, 2, 1], [2, 4, 5, 1, 3, 6], [4, 6, 3, 1, 5, 2], [2, 4, 6, 3, 1, 5]]
# jobs = 6
# machines = 10
# t_table = [[82, 91, 88, 72, 28, 29, 82, 99, 8, 81], [82, 51, 28, 3, 72, 9, 65, 29, 93, 8], [40, 48, 29, 16, 48, 20, 56, 40, 11, 71], [43, 67, 81, 45, 81, 99, 50, 89, 38, 60], [67, 26, 27, 78, 88, 43, 16, 53, 62, 15], [92, 11, 78, 13, 69, 54, 67, 75, 56, 68]]
# m_table=[[2, 7, 10, 6, 1, 9, 5, 8, 3, 4], [10, 4, 7, 6, 3, 9, 5, 1, 8, 2], [7, 3, 1, 2, 9, 4, 10, 6, 5, 8], [2, 9, 8, 1, 4, 7, 6, 10, 5, 3], [2, 1, 5, 10, 4, 7, 8, 3, 9, 6], [4, 6, 10, 3, 8, 5, 9, 1, 2, 7]]
# jobs = 10
# machines = 6
# t_table = [[72, 14, 48, 3, 65, 55], [86, 1, 89, 33, 15, 6], [81, 51, 4, 85, 18, 80], [92, 35, 49, 26, 24, 90], [80, 58, 86, 20, 11, 83], [80, 88, 37, 79, 32, 57], [53, 25, 64, 19, 86, 14], [77, 15, 48, 16, 49, 79], [97, 58, 24, 81, 90, 94], [25, 85, 6, 57, 20, 24]]
# m_table = [[2, 5, 4, 6, 3, 1], [1, 3, 2, 5, 6, 4], [1, 3, 4, 5, 6, 2], [2, 4, 6, 1, 5, 3], [6, 5, 4, 1, 3, 2], [4, 5, 2, 3, 6, 1], [3, 4, 2, 1, 6, 5], [2, 5, 6, 3, 4, 1], [2, 4, 5, 1, 6, 3], [6, 3, 1, 5, 4, 2]]
# jobs = 10
# machines = 10
#
# t_table = [[21, 19, 66, 38, 65, 21, 71, 40, 78, 93], [45, 73, 74, 25, 2, 95, 99, 99, 64, 19], [20, 66, 21, 36, 92, 95, 74, 32, 81, 2], [35, 20, 27, 63, 40, 52, 55, 22, 63, 81], [64, 8, 30, 54, 99, 96, 98, 59, 12, 46], [55, 23, 35, 66, 26, 25, 72, 60, 66, 28], [46, 57, 17, 5, 43, 13, 26, 24, 16, 12], [72, 62, 29, 55, 20, 50, 97, 32, 10, 14], [86, 87, 58, 66, 91, 46, 56, 20, 86, 21], [30, 3, 52, 35, 68, 46, 64, 26, 68, 44]]
# m_table = [[6, 1, 10, 2, 8, 7, 9, 4, 3, 5], [9, 8, 6, 1, 2, 5, 10, 3, 4, 7], [5, 10, 3, 2, 1, 6, 7, 9, 4, 8], [10, 8, 9, 5, 3, 6, 7, 2, 4, 1], [3, 10, 5, 2, 8, 7, 1, 6, 4, 9], [2, 7, 6, 10, 4, 1, 5, 9, 8, 3], [9, 4, 10, 7, 5, 2, 6, 8, 3, 1], [7, 4, 2, 5, 10, 1, 3, 9, 8, 6], [4, 7, 9, 8, 3, 6, 10, 2, 5, 1], [5, 1, 10, 2, 7, 8, 3, 9, 4, 6]]
# jobs = 20
# machines = 6
# t_table = [[53, 4, 34, 59, 16, 98], [57, 33, 35, 19, 47, 12], [30, 93, 89, 66, 62, 80], [90, 10, 60, 54, 53, 31], [68, 92, 99, 11, 20, 50], [14, 89, 32, 91, 85, 10], [72, 71, 60, 11, 48, 78], [20, 82, 77, 60, 60, 93], [71, 45, 78, 64, 20, 28], [13, 42, 55, 54, 37, 53], [80, 37, 93, 94, 50, 66], [57, 10, 81, 3, 14, 68], [10, 64, 77, 87, 34, 3], [58, 11, 72, 47, 5, 83], [22, 29, 59, 47, 56, 73], [8, 30, 18, 23, 39, 45], [80, 16, 6, 87, 69, 20], [25, 11, 75, 62, 30, 4], [33, 50, 23, 50, 90, 9], [36, 75, 55, 7, 52, 46]]
# m_table = [[6, 2, 5, 3, 1, 4], [3, 5, 1, 6, 4, 2], [1, 5, 4, 3, 2, 6], [5, 3, 4, 1, 2, 6], [6, 5, 4, 2, 1, 3], [3, 6, 4, 5, 1, 2], [5, 6, 2, 1, 3, 4], [6, 2, 4, 3, 1, 5], [2, 1, 5, 6, 4, 3], [6, 4, 1, 2, 3, 5], [6, 2, 5, 3, 4, 1], [3, 5, 1, 4, 6, 2], [6, 5, 2, 1, 4, 3], [2, 1, 6, 3, 5, 4], [1, 4, 6, 3, 5, 2], [4, 6, 1, 3, 2, 5], [4, 2, 3, 6, 5, 1], [3, 4, 2, 1, 5, 6], [2, 5, 1, 6, 4, 3], [5, 3, 4, 1, 6, 2]]
# jobs = 20
# machines = 10
#
# t_table = [[18, 20, 59, 91, 77, 16, 24, 97, 40, 77], [87, 37, 60, 88, 94, 14, 72, 59, 76, 77], [47, 29, 20, 35, 5, 25, 17, 45, 74, 8], [46, 20, 63, 32, 72, 86, 13, 79, 84, 30], [15, 6, 52, 60, 56, 64, 62, 76, 73, 4], [7, 3, 29, 63, 53, 5, 18, 63, 62, 57], [6, 27, 87, 72, 24, 75, 11, 66, 39, 20], [73, 85, 99, 11, 15, 14, 98, 21, 25, 69], [67, 6, 57, 98, 79, 37, 56, 85, 92, 64], [62, 4, 83, 35, 18, 46, 8, 37, 48, 8], [23, 83, 31, 96, 69, 29, 47, 18, 35, 96], [75, 18, 14, 38, 45, 60, 18, 61, 94, 32], [52, 80, 24, 22, 58, 86, 21, 5, 98, 42], [95, 7, 95, 55, 98, 67, 75, 40, 72, 33], [60, 46, 3, 85, 16, 22, 74, 35, 51, 3], [64, 35, 49, 89, 76, 48, 26, 67, 29, 16], [17, 86, 89, 84, 1, 74, 73, 99, 12, 3], [62, 19, 88, 37, 87, 5, 80, 8, 84, 39], [34, 61, 2, 81, 29, 29, 24, 98, 60, 69], [14, 69, 3, 18, 44, 10, 47, 75, 73, 37]]
# m_table = [[1, 9, 3, 6, 8, 4, 10, 7, 5, 2], [9, 2, 1, 8, 3, 5, 4, 6, 10, 7], [8, 4, 2, 5, 10, 9, 7, 1, 3, 6], [6, 4, 5, 10, 3, 7, 8, 2, 9, 1], [2, 4, 3, 8, 5, 10, 6, 1, 9, 7], [7, 10, 3, 1, 6, 8, 9, 2, 5, 4], [1, 6, 3, 2, 9, 7, 10, 4, 5, 8], [1, 9, 8, 4, 5, 6, 3, 7, 2, 10], [10, 6, 7, 4, 3, 1, 8, 9, 2, 5], [7, 8, 9, 4, 1, 10, 6, 3, 2, 5], [10, 1, 5, 2, 3, 7, 4, 8, 6, 9], [6, 7, 4, 2, 5, 3, 1, 8, 9, 10], [2, 1, 6, 8, 7, 5, 4, 3, 10, 9], [9, 7, 1, 10, 8, 3, 5, 2, 4, 6], [4, 7, 9, 3, 10, 5, 6, 8, 1, 2], [8, 10, 3, 5, 2, 1, 6, 9, 7, 4], [7, 10, 5, 8, 6, 2, 1, 4, 9, 3], [1, 9, 3, 2, 4, 7, 10, 6, 5, 8], [4, 7, 5, 6, 2, 3, 8, 10, 9, 1], [5, 6, 8, 2, 3, 4, 9, 7, 1, 10]]


def com_tr(t_table):
    topo_order = []
    for j_num, o_num in enumerate(t_table):  # 根据时间表获取工件数索引和其工序列表
        topo_order = topo_order + (np.ones([1, len(o_num)], int) * (j_num + 1)).tolist()
    combin = []
    for li in topo_order:  # 将列表中各工件独立列表加起来
        combin = combin + li

    random.shuffle(combin)  # 随机打乱列表中元素
    return combin


class Cij:
    def __init__(self, name, StartTime, LoadTime):
        self.name = name
        self.StartTime = StartTime
        self.LoadTime = LoadTime
        self.EndTime = StartTime + LoadTime


# 定义最大流程时间函数
def c_max(combin):  # n根据下文应该是单条染色体
    # 循环赋值函数，将工件数，机器数与加工时间进行绑定
    # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列
    for i in range(len(combin)):  # i为工件索引
        job = combin[i]  # 工件
        no_job = combin[:i + 1].count(job)  # 工序
        machine = m_table[job - 1][no_job - 1]  # 机器号
        loadtime = t_table[job - 1][no_job - 1]  # 该工序加工时间
        locals()['c{}_{}_{}'.format(job, no_job, machine)] = Cij(name='c{}_{}_{}'.format(job, no_job, machine),
                                                                 StartTime=0, LoadTime=loadtime, )
        # Python locals() 函数会以字典类型返回当前位置的全部局部变量。
    load_time_tables = []
    # M_time = np.zeros(max(max(m_table)))  # 初始化所有机器当前加工时刻为0
    M_time = np.zeros(machines)
    for i in range(len(combin)):  # combin为数值编号，代表工件及其工序数量
        job = combin[i]  # 工件号
        no_job = combin[:i + 1].count(job)  # 工序
        machine = m_table[job - 1][no_job - 1]  # 注意python索引
        if no_job == 1:  # 工序号，开始时间为机器完成上个工件任务的时间或0
            locals()['c{}_{}_{}'.format(job, no_job, machine)].StartTime = M_time[machine - 1]
        else:
            locals()['c{}_{}_{}'.format(job, no_job, machine)].StartTime = max(
                M_time[machine - 1],  # 该工序所在加工位置机器的时间
                locals()['c{}_{}_{}'.format(job, no_job - 1, m_table[job - 1][no_job - 2])].EndTime)  # 该工序的前道工序的完工时间
        locals()['c{}_{}_{}'.format(job, no_job, machine)].EndTime = locals()['c{}_{}_{}'.format(job, no_job,
                                                                                                 machine)].StartTime + \
                                                                     locals()['c{}_{}_{}'.format(job, no_job,
                                                                                                 machine)].LoadTime
        M_time[machine - 1] = locals()['c{}_{}_{}'.format(job, no_job, machine)].EndTime
        load_time_tables.append([locals()['c{}_{}_{}'.format(job, no_job, machine)].name, [
            locals()['c{}_{}_{}'.format(job, no_job, machine)].StartTime,
            locals()['c{}_{}_{}'.format(job, no_job, machine)].EndTime]])
        T = []
        for i in load_time_tables:
            T.append(i[-1][-1])
    # print(load_time_tables)
    return load_time_tables, max(T)  # load_time_tables 代表所有工件每个工序加工位置及其开始和结束加工时间


# 种群初始化
def init_population(pop_size, chrom):
    pop = []
    for i in range(pop_size):
        c = copy.deepcopy(chrom)
        random.shuffle(c)
        pop.append(c)
    return pop


# 计算适应度
def fitness(combin):
    return c_max(combin)[1]


class node:
    def __init__(self, state):
        self.state = state
        self.load_table = c_max(state)[0]  # 求出染色体上每个工序所在机器的开始结束时间表
        self.makespan = c_max(state)[1]  # 染色体的时间跨度
        self.fitness = fitness(state)


'''
出问题的地方,交叉错误
'''


def two_points_cross(chro1, chro2):
    # 不改变原始数据进行操作
    chro1_1 = copy.deepcopy(chro1)
    chro2_1 = copy.deepcopy(chro2)
    # 交叉位置，point1<point2
    point1 = random.randint(0, len(chro1_1))
    point2 = random.randint(0, len(chro1_1))
    while point1 > point2 or point1 == point2:
        point1 = random.randint(0, len(chro1_1))
        point2 = random.randint(0, len(chro1_1))

    # 记录交叉片段
    frag1 = chro1[point1:point2]
    frag2 = chro2[point1:point2]
    random.shuffle(frag1)
    random.shuffle(frag2)
    # 交叉
    chro1_1[point1:point2], chro2_1[point1:point2] = chro2_1[point1:point2], chro1_1[point1:point2]

    child1 = chro1_1[:point1] + frag1 + chro1_1[point2:]
    child2 = chro2_1[:point1] + frag2 + chro2_1[point2:]

    return child1, child2


# 交换变异
def gene_exchange(n):
    point1 = random.randint(0, len(n) - 1)
    point2 = random.randint(0, len(n) - 1)
    while point1 == point2 or point1 > point2:
        point1 = random.randint(0, len(n) - 1)
        point2 = random.randint(0, len(n) - 1)
    n[point1], n[point2] = n[point2], n[point1]
    return n


# 插入变异
def gene_insertion(n):
    point1 = random.randint(0, len(n) - 1)
    point2 = random.randint(0, len(n) - 1)
    while point1 == point2:
        point1 = random.randint(0, len(n) - 1)
        point2 = random.randint(0, len(n) - 1)
    x = n.pop(point1)
    n.insert(point2, x)
    return n


# 局部逆序变异
def gene_reverse(n):
    point1 = random.randint(0, len(n) - 1)
    point2 = random.randint(0, len(n) - 1)
    while point1 == point2 or point1 > point2:
        point1 = random.randint(0, len(n) - 1)
        point2 = random.randint(0, len(n) - 1)
    ls_res = n[point1:point2]
    ls_res.reverse()
    l1 = n[:point1]
    l2 = n[point2:]
    n_res_end = l1 + ls_res + l2
    return n_res_end


def select(population):
    pop_fit = []
    for i in population:
        pop_fit.append(fitness(i))
    best_chrom = min(pop_fit)

    return best_chrom


def update_AK(A0, r0, K, t, c_r0, mu0):  # 更新参数
    A = K / (1 + (K / A0 - 1) * np.exp(-r0 * t))
    r = r0 * (1 - A / K)
    c_r = c_r0 * (1 - A / K)
    mu = mu0 * (1 - A / K)
    # pop_size = 10
    pop_size = math.ceil(math.log(K / A))+4  # 种群规模
    return A, r, c_r, mu, pop_size


def update_solution(population):
    solution_list = []
    # 可行解集，包含开始结束时间等信息
    for i in population:
        # locals()['solution{}'.format(population.index(i))] = node(i)  # i为染色体,node为类包含makespan属性
        solution_list.append(node(i))
    # solution_list.sort(key=lambda x: x.makespan)  # 排序后首个染色体为最佳解
    pops = [i.state for i in solution_list]  # 相当于把solution_list的染色体复制到pops中
    f_list = [i.makespan for i in solution_list]
    Xb, fb, fave = pops[0], f_list[0], np.mean(f_list)  # 最佳个体与平均适应度
    return solution_list, Xb, fb, fave, f_list


# 进行遗传算法实现
# 入侵改进GA算法
A0 = 100
r0 = 0.01
K = 10000
t = 1
c_r0 = 0.8  # 交叉概率
mu0 = 0.9  # 变异概率
select_r = 0.8
A, r, c_r, mu, pop_size = update_AK(A0, r0, K, t, c_r0, mu0)
target_points = [1, 2, 3]
p_size = 2
# 开始求解
combin = com_tr(t_table)  # 转化成工件号编码
# population = init_population(pop_size, combin)
# 开始循环
start = datetime.datetime.now()
best_fit, best_fit_global, mean_ave = [], [], []
# iters=100
population = init_population(pop_size, combin)
solution_list = [node(i) for i in population]
# solution_list.sort(key=lambda x: x.makespan)
pops = [i.state for i in solution_list]  # 相当于把solution_list的染色体复制到pops中  pops = copy.deepcopy(population)
f_list = [i.makespan for i in solution_list]  # 计算该种群各适应度
Xb, fb, fave = pops[0], f_list[0], np.mean(f_list)  # 最佳个体与平均适应度
pop2 = pops[:p_size]
Xb_global, fb_global = Xb, fb
best_fit.append(fb)
best_fit_global.append(fb_global)
# 也可以用argmin获取最小值索引
while A < K * 0.95:
    if t % 10 == 0:
        print('第{}次进化后的最优加工时间为{}'.format(t, fb_global))  # 首个染色体的结束时间, solution_list含makespan函数和方法
    f_ave = []
    for k in range(pop_size):
        Xk, fk = pops[k], f_list[k]
        pk = np.exp(-(fk - fb) / (A * r))  # 适应度越小越好
        if pk > max(select_r, A / K):
            Xb, fb = Xk, fk
            if fk < fb_global:
                Xb_global, fb_global = Xk, fk
            pop2 = [Xb, Xb_global]
            random.shuffle(pops[k])
        else:
            random.shuffle(Xk)
            target = random.choice(target_points)  # ???三种编译策略
            xb = random.choice(list(range(p_size)))
            # target = 3
            if target == 1:
                pops[k] = gene_exchange(pop2[xb])
            elif target == 2:
                pops[k] = gene_insertion(pop2[xb])
            else:
                pops[k] = gene_reverse(pop2[xb])
            # elif c_r < random.random():
            pops[k], X = two_points_cross(Xk, pop2[xb])
        # else:
        #     Xk = copy.deepcopy(Xb)
        #     random.shuffle(Xk)
        fk = node(Xk).makespan
        f_ave.append(fk)
    mean_f = np.mean(f_ave)  # 种群的平均适应度
    mean_ave.append(mean_f)  # 存储平均值
    f_list = [node(i).makespan for i in pops]  # 计算该种群各适应度
    # Xb, fb, fave = pops[0], f_list[0], np.mean(f_list)  # 最佳个体与平均适应度
    t += 1
    best_fit.append(fb)
    best_fit_global.append(fb_global)
    A, r, c_r, mu, pop_size = update_AK(A0, r0, K, t, c_r0, mu0)
print('进化完成，最终最优加工时间为：', fb_global)
end = datetime.datetime.now()
print('耗时{}'.format(end - start))
print(node(Xb).load_table)
# config = {
#             "font.family": 'serif',
#             "font.size": 20,
#             "mathtext.fontset": 'stix',
#             "font.serif": ['SimSun'],
#          }
# rcParams.update(config)
# plt.figure(1)
# # 绘制甘特图
# def color():# 甘特图颜色生成函数
#     color_ls = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
#     col = ''
#     for i in range(6):  # 6种颜色数字字母组合
#         col += random.choice(color_ls)
#     return '#'+col
# colors = [color() for i in range(len(t_table))]  # 甘特图颜色列表,每个工件一个颜色
# for i in node(Xb_global).load_table:  # 对最佳染色体进行遍历，做出甘特图
#     # print(i)  # 每个工件
#     y = eval(re.findall('_(\d+)', i[0])[1])  # 正则表达式匹配工件数,找到_后面内部整数个数，机器号=工序号
#     """
#     i = ['c24_9', [1715, 1736]]  # 9
#     # \d匹配任何十进制数，它相当于类[0-9]
#     # \d+如果需要匹配一位或者多位数的数字时用
#     a = re.search("(a4)+", "a4a4a4a4a4dg4g654gb")   # 匹配一个或多个a4
#     a = re.findall(r"你|好", "a4a4a你4aabc4a4dgg好dg4g654g")   #|或，或就是前后其中一个符合就匹配  #打印出 ['你', '好']
#     """
#     # eval() 函数用来执行一个字符串表达式，并返回表达式的值。
#     label=re.findall(r'(\d*?)_', i[0])[0]  # 正则表达式匹配机器数
#     plt.barh(y=y, left=i[1][0], width=i[1][-1] - i[1][0], height=0.5, color=colors[eval(label) - 1],
#              label=f'job{label}')
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
# plt.rcParams['font.serif'] = ['KaiTi']
# plt.rcParams['axes.unicode_minus'] = False
# plt.title('gantt chart of the best schedule for ft06')
# plt.xlabel('working time')
# plt.ylabel('machine')
# handles, labels = plt.gca().get_legend_handles_labels()  # 标签去重
# from collections import OrderedDict  # ：字典的子类，保留了他们被添加的顺序
# by_label = OrderedDict(zip(labels, handles))
# plt.legend(by_label.values(), by_label.keys())
# config = {
#             "font.family": 'serif',
#             "font.size": 20,
#             "mathtext.fontset": 'stix',
#             "font.serif": ['SimSun'],
#          }
# rcParams.update(config)
# plt.figure(2)
# # plt.plot(best_fit[:])
# # plt.plot(best_fit_global[:])
# # plt.plot(mean_ave[:])
# plt.title('variation of makespan with LBIGA')
# plt.xlabel('iteration')
# plt.ylabel('working time')
# p1, = plt.plot(best_fit_global[:], label='best_fit')
# p2, = plt.plot(best_fit[:], label='fit_ave', linestyle='--')
# # p3, = plt.plot(mean_ave[:], label='mean_ave')
# # p3, = plt.plot(mean_ave[:])
# l1 = plt.legend([p1, p2], ["whole optimization", "accepted optimization"], loc='upper right')
# plt.show()