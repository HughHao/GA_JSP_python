# -*- coding: utf-8 -*-
# @Time : 2021/12/12 16:58
# @Author : hhq
# @File : New_JSP.py

'''1.3 车间状态和动作（Job_shop）'''
import numpy as np
import random
from Instance_Generator import Processing_time, A, D, M_num, Op_num, J, O_num, J_num
from Object_for_FJSP import Object


class Situation:  # 环境
    def __init__(self, J_num, M_num, O_num, J, Processing_time, D, Ai):  #
        self.Ai = Ai  # 工件到达时间
        self.D = D  # 交货期
        self.O_num = O_num  # 工序总数
        self.M_num = M_num  # 机器数
        self.J_num = J_num  # 工件数
        self.J = J  # 工件对应的工序数字典
        self.Processing_time = Processing_time  # 加工时间

        self.CTK = [0 for i in range(M_num)]  # 各机器上最后一道工序的完工时间列表
        self.OP = [0 for i in range(J_num)]  # 各工件的已加工工序数列表
        self.UK = [0 for i in range(M_num)]  # 各机器的实际使用率
        self.CRJ = [0 for i in range(J_num)]  # 工件完工率
        self.CTI = [0 for i in range(J_num)]  # 每个工件的已加工的最后工序结束时间

        # 工件集：
        self.Jobs = []
        for i in range(J_num):
            F = Object(i)  #
            self.Jobs.append(F)  # 工件（包含已加工工序的开始、结束、加工时间、位置属性）集合
        # 机器集
        self.Machines = []
        for i in range(M_num):
            F = Object(i)
            self.Machines.append(F)

    # 更新基础数据（用以计算状态特征）
    def _Update(self, Job, Machine):  # 参数：工件索引，机器索引
        self.CTK[Machine] = max(self.Machines[Machine].End)  # 每台机器加工过的最后一道工序的结束时间
        self.CTI[Job] = max(self.Jobs[Job].End)  # 该工序加工结束的时间
        self.OP[Job] += 1  # 工件已加工的工序数量集合
        self.UK[Machine] = sum(self.Machines[Machine].T) / self.CTK[Machine]  # 单台设备利用率 = 工件需要在机器加工时间之和/当前已结束工序的完工时间
        self.CRJ[Job] = self.OP[Job] / self.J[Job]  # 工件Job的完工率=已加工数/总工序数

    # 机器平均使用率
    def Features(self):

        # 1 设备平均利用率
        U_ave = sum(self.UK) / self.M_num   # 初始为0
        # 设备
        # 2 机器的使用率标准差
        K = 0
        for uk in self.UK:
            K += np.square(uk - U_ave)
        U_std = np.sqrt(K / self.M_num)  # 初始为0
        # 3 平均工序完成率
        CRO_ave = sum(self.OP) / self.O_num  # 已加工工序平均数， # 初始为0
        # 4 平均工件工序完成率
        CRJ_ave = sum(self.CRJ) / self.J_num  # 平均工件的工序完成率，# 初始为0

        # 5 工件工序完成率标准差
        K = 0
        for uk in self.CRJ:
            K += np.square(uk - CRJ_ave)
        CRJ_std = np.sqrt(K / self.J_num)  # 初始为0

        # 6 Estimated tardiness Tard_e

        Tard_e,TARD,TLEFT = 0,0,0
        for i in range(self.J_num):  # 对每个工件计算

            if J[i] > self.OP[i]:  # 总工序数大于已加工工序数，未完成加工的工件
                T_left = 0  # 该工件剩余时间
                for j in range(self.OP[i] + 1, self.J[i]):  # 剩余工序遍历索引
                    M_ij = [k for k in self.Processing_time[i][j] if k > 0]  # 剩余工序加工时间集合
                    T_left += (sum(M_ij) / len(M_ij))  # 剩余工序在可用机器的平均加工时间
                if self.CTI[i] < D[i] and T_left + self.CTI[i] > self.D[i]:  # 剩余平均加工时间与当前结束时间之和大于截止时间
                    Tard_e += (T_left + self.CTI[i] - self.D[i])  # 所有工件的延迟时间
                TLEFT += T_left  # 所有工件的剩余加工时间
        if TLEFT > 0:
            TARD = (Tard_e / TLEFT)  # 预计所有工件的延期程度


        # 7 Actual tardiness rate Tard_a
        N_tard, Tard_a, N_left = 0, 0, 0
        for i in range(self.J_num):  # 工件遍历
            if self.J[i] > self.OP[i]:  # 工件未完成
                N_left += self.J[i] - self.OP[i]  # 剩余未加工工序数
                if self.CTI[i] > self.D[i]:  # 每台机器最后一道工序结束
                        N_tard += self.J[i] - self.OP[i] + 1  # 延期数量
        if N_left > 0:
            Tard_a = N_tard / N_left

        return U_ave, U_std, CRO_ave, CRJ_ave, CRJ_std, TARD, Tard_a

    # Composite dispatching rule 1
    # return Job,Machine
    def rule1(self):
        # T_cur:平均每台机器的完工时间
        T_cur = sum(self.CTK) / self.M_num
        # Tard_Job:不能按期完成的工件  --》估计 索引
        Tard_Job = [i for i in range(self.J_num) if self.OP[i] < self.J[i] and self.D[i] < T_cur]  # 预计会延期的工件索引列表
        UC_Job = [j for j in range(self.J_num) if self.OP[j] < self.J[j]]  # 还没有完工的工件索引列表
        if Tard_Job == []:  # 如果延期工件集合为空
            Job_i = UC_Job[np.argmin([(self.D[i] - T_cur) / (self.J[i] - self.OP[i]) for i in UC_Job])]  # 剩余完工时间最小工件索引
        else:
            T_ijave = []  # 平均延期工件
            for i in Tard_Job:  # 对每个延期工件
                Tad = []
                for j in range(self.OP[i], self.J[i]):  # 未完成的工件
                    '''原语句：for j in range(self.OP[i] + 1, self.J[i]):  # 未完成的工件'''
                    T_ijk = [k for k in self.Processing_time[i][j] if k != -1]  # 可用机器各自的加工时间
                    Tad.append(sum(T_ijk) / len(T_ijk))  # 可用机器的平均加工时间
                T_ijave.append(T_cur + sum(Tad) - self.D[i])  # 每个工件的延期程度，剩余平均加工时间与平均结束时间之和减去截止时间
            Job_i = Tard_Job[np.argmax(T_ijave)]  # 预计延期最大的工件
        '''选出工件，接下来选取机器'''
        try:  # 若此句出现问题
            C_ij = max(self.Jobs[Job_i].End)  # 找出选出工件的结束时间（各工序的最大结束时间）
        except:  # 执行下句
            C_ij = self.Ai[Job_i]  # 工件i的arrival time的最大值

        A_ij = self.Ai[Job_i]  # 工件i的arrival time
        # print(A_ij)
        On = len(self.Jobs[Job_i].End)  # 工序数？含有结束时间工序的个数
        Mk = []
        for i in range(len(self.CTK)):  # 机器数遍历
            if self.Processing_time[Job_i][On][i] != -1:  # 该机器可用
                # C_ij += self.Processing_time[Job_i][On][i]  # 该工序每次结束时间计算，直至最后一道工序
                Mk.append(max(C_ij, A_ij, self.CTK[i]))  # 可用机器k的最早开始时间
            # else:
            #     Mk.append(9999)
        # print('This is from rule 1:',Mk)
        Machine = np.argmin(Mk)  # 最早可用机器的索引号
        # print('This is from rule 1:',Machine)
        return Job_i, Machine

    # Composite dispatching rule 2
    # return Job,Machine
    def rule2(self):
        # T_cur:平均完工时间
        T_cur = sum(self.CTK) / self.M_num
        # Tard_Job:不能按期完成的工件
        Tard_Job = [i for i in range(self.J_num) if self.OP[i] < self.J[i] and self.D[i] < T_cur]  # 预计有延期的工件
        UC_Job = [j for j in range(self.J_num) if self.OP[j] < self.J[j]]  # 还有工序未完成的工件索引
        T_ijave = []  #
        for i in range(self.J_num):
            Tad = []
            for j in range(self.OP[i], self.J[i]):  # 剩余工序遍历
                T_ijk = [k for k in self.Processing_time[i][j] if k != -1]
                Tad.append(sum(T_ijk) / len(T_ijk))  # 剩余每个工序的平均加工时间
            T_ijave.append(sum(Tad))  # 未加工工序时间之和
        if Tard_Job == []:  # 没有延期工件
            Job_i = UC_Job[np.argmin([(self.D[i] - T_cur) / T_ijave[i] for i in UC_Job])]
        else:
            Job_i = Tard_Job[np.argmax([T_cur + T_ijave[i] - self.D[i] for i in Tard_Job])]
        try:
            C_ij = max(self.Jobs[Job_i].End)
        except:
            C_ij = self.Ai[Job_i]  # 工件i的arrival time
        A_ij = self.Ai[Job_i]  # 工件i的arrival time
        # print(A_ij)
        On = len(self.Jobs[Job_i].End)
        Mk = []
        for i in range(len(self.CTK)):
            Mk.append(max(C_ij, A_ij, self.CTK[i]))  # 机器可以开始时间

        # print('This is from rule 2:',Mk)
        Machine = np.argmin(Mk)
        # print('This is from rule 2:',Machine)
        return Job_i, Machine

    # Composite dispatching rule 3
    def rule3(self):
        # T_cur:平均完工时间
        T_cur = sum(self.CTK) / self.M_num
        # Tard_Job:不能按期完成的工件
        UC_Job = [j for j in range(self.J_num) if self.OP[j] < self.J[j]]
        T_ijave = []
        for i in UC_Job:
            Tad = []
            for j in range(self.OP[i], self.J[i]):
                T_ijk = [k for k in self.Processing_time[i][j] if k != -1]
                Tad.append(sum(T_ijk) / len(T_ijk))
            T_ijave.append(T_cur + sum(Tad) - self.D[i])
        Job_i = UC_Job[np.argmax(T_ijave)]
        On = len(self.Jobs[Job_i].End)
        if random.random() < 0.5:
            U = []
            for i in range(len(self.UK)):
                if self.Processing_time[Job_i][On][i] == -1:
                    U.append(9999)
                else:
                    U.append(self.UK[i])
            Machine = np.argmin(U)
        else:
            MT = []
            for j in range(self.M_num):
                if self.Processing_time[Job_i][On][j] == -1:
                    MT.append(9999)
                else:
                    MT.append(sum(self.Machines[j].T))
            Machine = np.argmin(MT)
        # print('This is from rule 3:',Machine)
        return Job_i, Machine

    # Composite dispatching rule 4
    def rule4(self):
        UC_Job = [j for j in range(self.J_num) if self.OP[j] < self.J[j]]
        Job_i = random.choice(UC_Job)
        try:
            C_ij = max(self.Jobs[Job_i].End)
        except:
            C_ij = self.Ai[Job_i]  # 工件i的arrival time
        A_ij = self.Ai[Job_i]  # 工件i的arrival time
        On = len(self.Jobs[Job_i].End)
        Mk = []
        for i in range(len(self.CTK)):
            if self.Processing_time[Job_i][On][i] != -1:
                Mk.append(max(C_ij, A_ij, self.CTK[i]))  # 机器可以开始时间

        # print('This is from rule 4:',Mk)
        Machine = np.argmin(Mk)
        # print('This is from rule 4:',Machine)
        return Job_i, Machine

    # Composite dispatching rule 5
    def rule5(self):

        # T_cur:平均完工时间
        T_cur = sum(self.CTK) / self.M_num
        # Tard_Job:不能按期完成的工件
        Tard_Job = [i for i in range(self.J_num) if self.OP[i] < self.J[i] and self.D[i] < T_cur]
        UC_Job = [j for j in range(self.J_num) if self.OP[j] < self.J[j]]
        if Tard_Job == []:
            Job_i = UC_Job[np.argmin([self.CRJ[i] * (self.D[i] - T_cur) for i in UC_Job])]
        else:
            T_ijave = []
            for i in Tard_Job:
                Tad = []
                for j in range(self.OP[i], self.J[i]):
                    T_ijk = [k for k in self.Processing_time[i][j] if k != -1]
                    Tad.append(sum(T_ijk) / len(T_ijk))
                T_ijave.append(1 / (self.CRJ[i] + 1) * (T_cur + sum(Tad) - self.D[i]))
            Job_i = Tard_Job[np.argmax(T_ijave)]
        try:
            C_ij = max(self.Jobs[Job_i].End)
        except:
            C_ij = self.Ai[Job_i]  # 工件i的arrival time
        A_ij = self.Ai[Job_i]  # 工件i的arrival time
        On = len(self.Jobs[Job_i].End)
        Mk = []
        for i in range(len(self.CTK)):
            if self.Processing_time[Job_i][On][i] != -1:
                Mk.append(max(C_ij, A_ij, self.CTK[i]))  # 机器可以开始时间

        # print('This is from rule 5:',Mk)
        Machine = np.argmin(Mk)
        # print('This is from rule 5:',Machine)
        return Job_i, Machine

    # Composite dispatching rule 6
    # return Job,Machine
    def rule6(self):
        # T_cur:平均完工时间
        T_cur = sum(self.CTK) / self.M_num
        UC_Job = [j for j in range(self.J_num) if self.OP[j] < self.J[j]]
        T_ijave = []
        for i in UC_Job:
            Tad = []
            for j in range(self.OP[i], self.J[i]):
                T_ijk = [k for k in self.Processing_time[i][j] if k != -1]
                Tad.append(sum(T_ijk) / len(T_ijk))
            T_ijave.append(T_cur + sum(Tad) - self.D[i])
        Job_i = UC_Job[np.argmax(T_ijave)]
        try:
            C_ij = max(self.Jobs[Job_i].End)
        except:
            C_ij = self.Ai[Job_i]  # 工件i的arrival time
        A_ij = self.Ai[Job_i]  # 工件i的arrival time
        On = len(self.Jobs[Job_i].End)
        Mk = []
        for i in range(len(self.CTK)):
            if self.Processing_time[Job_i][On][i] != -1:
                Mk.append(max(C_ij, A_ij, self.CTK[i]))
            else:
                Mk.append(9999)
        Machine = np.argmin(Mk)
        # print('this is from rule 6:',Mk)
        # print('This is from rule 6:',Machine)
        return Job_i, Machine

    def scheduling(self, action):  # 根据行动（选择的工件，机器），将加工工序所在工件、加工位置、加工时间开始、结束均存储起来
        Job, Machine = action[0], action[1]
        O_n = len(self.Jobs[Job].End)  # 目前已加工工件包含的工序数

        # print(Job, Machine,O_n)
        Idle = self.Machines[Machine].idle_time()  # 被选择的机器的闲置时间区间集合
        try:
            last_ot = max(self.Jobs[Job].End)  # 上道工序加工结束时间
        except:
            last_ot = 0
        try:
            last_mt = max(self.Machines[Machine].End)  # 所在机器最后完工时间
        except:
            last_mt = 0
        Start_time = max(last_ot, last_mt, self.Ai[Job])  # 开始时间
        PT = self.Processing_time[Job][O_n][Machine]  # 即将加工(目前工序号+1,python)的工序加工时间
        for i in range(len(Idle)):  # 多少个闲时间区间  Idle为空闲时段集合
            if Idle[i][1] - Idle[i][0] > PT:  # 大于该工序时间
                if Idle[i][0] > last_ot:
                    Start_time = Idle[i][0]
                    pass
                if Idle[i][0] < last_ot and Idle[i][1] - last_ot > PT:
                    Start_time = last_ot
                    pass
        end_time = Start_time + PT
        self.Machines[Machine]._add(Start_time, end_time, Job, PT)
        self.Jobs[Job]._add(Start_time, end_time, Machine, PT)
        self.Machines[Machine].idle_time()
        self.Jobs[Job].idle_time()
        self._Update(Job, Machine)

    def reward(self, obs, obs_t):
        #  obs[0-6]:设备平均利用率，设备利用率标准差、所有工序完成率、每个工件工序完成率平均值、平均工件工序完成率标准差、预估延迟程度(下一状态更好-小)、当前已延迟数量比例

        # print([Ta_t, Te_t, Ta_t1, Te_t1, U_t, U_t1])
        # rt = np.exp(Te_t)/np.exp(Te_t1) + np.exp(Ta_t)/np.exp(Ta_t1) + np.exp(U_t1)/np.exp(U_t)
        if obs[0] > 0:
            r1 = np.exp(obs_t[0]/obs[0])
        else:
            r1 = np.exp((obs_t[0]-obs[0]))  # 平均设备利用率的奖励
        if obs_t[1] > 0:
            r2 = np.exp(obs[1]/obs_t[1])
        else:
            r2 = np.exp((obs[1]-obs_t[1]))
        if obs_t[5] > 0:
            r3 = np.exp(obs[5]/obs_t[5])
        else:
            r3 = np.exp((obs[5]-obs_t[5]))  # 下个延迟程度更小的话更好
        if obs_t[6]>0:
            r4 = np.exp(obs[6]/obs_t[6])
        else:
            r4 = np.exp(obs[6]-obs_t[6])
        rt = r1 + r2 + r3 + r4
        return rt


Sit = Situation(J_num, M_num, O_num, J, Processing_time, D, A)