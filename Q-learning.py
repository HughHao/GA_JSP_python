# -*- coding: utf-8 -*-
# @Time : 2021/11/8 19:51
# @Author : hhq
# @File : Q-learning.py
import numpy as np
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import random
from collections import deque
from tensorflow.keras import layers, models
import tensorflow as tf
from JSP import Situation
from tensorflow.keras.optimizers import Adam
from Instance_Generator import Processing_time, A, D, M_num, Op_num, J, O_num, J_num
import matplotlib.pyplot as plt


class DQN:
    def __init__(self, ):
        self.Hid_Size = 30

        # ------------Hidden layer=5   30 nodes each layer--------------
        model = models.Sequential()
        model.add(layers.Input(shape=(7,)))
        model.add(layers.Dense(self.Hid_Size, name='l1'))
        model.add(layers.Dense(self.Hid_Size, name='l2'))
        model.add(layers.Dense(self.Hid_Size, name='l3'))
        model.add(layers.Dense(self.Hid_Size, name='l4'))
        model.add(layers.Dense(self.Hid_Size, name='l5'))
        model.add(layers.Dense(6, name='l6'))
        model.compile(loss='mse',
                      optimizer=Adam(learning_rate=0.001))
        # # model.summary()
        self.model = model

        # ------------Q-network Parameters-------------
        self.act_dim = [1, 2, 3, 4, 5, 6]  # 神经网络的输出节点
        self.obs_n = [0, 0, 0, 0, 0, 0, 0]  # 神经网路的输入节点
        self.gama = 0.95  # γ经验折损率
        # self.lr = 0.001  # 学习率
        self.global_step = 0
        self.update_target_steps = 200  # 更新目标函数的步长
        self.target_model = self.model  # 目标Q初始化为Q

        # -------------------Agent-------------------
        self.e_greedy = 0.6
        self.e_greedy_decrement = 0.0001
        self.L = 40  # Number of training episodes L

        # ---------------Replay Buffer---------------
        self.buffer = deque(maxlen=2000)  # 类似于list的容器，可以快速的在队列头部和尾部添加、删除元素  存储（
        self.Batch_size = 10  # Batch Size of Samples to perform gradient descent

    def replace_target(self):  # 重置目标函数，将其按照
        # self.target_model.get_layer(name='l1').set_weights(self.model.get_layer(name='l1').get_weights())
        # self.target_model.get_layer(name='l2').set_weights(self.model.get_layer(name='l2').get_weights())
        # self.target_model.get_layer(name='l3').set_weights(self.model.get_layer(name='l3').get_weights())
        # self.target_model.get_layer(name='l4').set_weights(self.model.get_layer(name='l4').get_weights())
        # self.target_model.get_layer(name='l5').set_weights(self.model.get_layer(name='l5').get_weights())
        # self.target_model.get_layer(name='l6').set_weights(self.model.get_layer(name='l6').get_weights())
        self.target_model = self.model
        # print(self.target_model == self.model)

    def replay(self):
        if self.global_step % self.update_target_steps == 0:  # 更新步长200
            self.replace_target()  # 更新目标Q的参数
        # replay the history and train the model
        minibatch = random.sample(self.buffer, self.Batch_size)  # 从buffer中随机取出Batch_size个样本
        for state, action, reward, next_state, done in minibatch:  # (obs, at, r_t, obs_t, done)
            target = reward  # 如果最终状态
            if not done:
                k = np.argmax(self.model.predict(next_state))  # state：U_ave, U_std, CRO_ave, CRJ_ave, CRJ_std, Tard_e, Tard_a
                # target = (reward + self.gama *
                #           np.argmax(self.target_model.predict(next_state)))
                target = (reward + self.gama *
                          self.target_model.predict(next_state)[0][k])
            target_f = self.model.predict(state)  # 模型输入s输出Q(s,a)  [[ 0.11677918  0.09287173 -0.3526993   0.0677374   0.12638253 -0.01366934]]
            '''target_f用于训练Q'''
            # print(target_f)
            # print('aa')
            target_f[0][action] = target  # 更新yj  action=0,1,...,5
            '''target_f输出看看是什么，如何根据state得到预测值'''
            self.model.fit(state, target_f, epochs=1, verbose=0)  # 模型训练
        self.global_step += 1

    def Select_action(self, obs):  # 根据observation进行决策，obs相当于state
        # obs=np.expand_dims(obs,0)
        if random.random() < self.e_greedy:
            act = random.randint(0, 5)  # 包括0和5，numpy.random.randint(a,b)  ~[a,b)
        else:
            act = np.argmax(self.model.predict(obs))
        self.e_greedy = max(
            0.01, self.e_greedy - self.e_greedy_decrement)  # 随着训练逐步收敛，探索的程度慢慢降低
        return act

    def _append(self, exp):
        self.buffer.append(exp)

    def main(self, J_num, M_num, O_num, J, Processing_time, D, A):
        '''
        :param J_num: 工件数
        :param M_num: 机器数
        :param O_num: 工序总数
        :param J: {工件索引：工序数}
        :param Processing_time: 加工时间（包含同工序的不同机器）
        :param D: 所有工件的紧急程度
        :param A: 所有工件的到达时间
        :return:
        '''
        k = 0
        x = []
        Total_tard = []  # 延期程度
        TR = []  # 序列奖励

        for i in range(self.L):
            Total_reward = 0
            x.append(i + 1)  # episode_num
            print('-----------------------开始第', i + 1, '次训练------------------------------')
            done = False
            Sit = Situation(J_num, M_num, O_num, J, Processing_time, D, A)  # Processing_time由案例生成得到
            # obs = [0 for i in range(7)]  # 7种观察-状态特征 np.expand_dims:用于扩展数组的形状
            obs = Sit.Features()  # 初始是否为0？？？
            obs = np.expand_dims(obs, 0)  # 将obs扩展为二维array数组,存储特征数据
            ''' 初始状态 '''
            for j in range(O_num):  # 对工序遍历
                k += 1  # 即将加工工序数
                # print(obs)
                '''选择动作'''
                at = self.Select_action(obs)  # 选择工件和机器
                # print(at)
                if at == 0:
                    at_trans = Sit.rule1()
                if at == 1:
                    at_trans = Sit.rule2()
                if at == 2:
                    at_trans = Sit.rule3()
                if at == 3:
                    at_trans = Sit.rule4()
                if at == 4:
                    at_trans = Sit.rule5()
                if at == 5:
                    at_trans = Sit.rule6()
                # at_trans=self.act[at]
                # ？？？？？原有：？？？print('这是第', j, '道工序>>', '执行action:', at, ' ', '将工件', at_trans[0], '安排到机器', at_trans[1])
                '''每经过一次工序（包含工件及机器）更新学习状态和调度进程'''
                if j == O_num - 1:
                    done = True
                Sit.scheduling(at_trans)  # 选择机器和工件后更新调度以及计算状态特征的数据
                obs_t = Sit.Features()  # 更新7个状态特征，U_ave, U_std, CRO_ave, CRJ_ave, CRJ_std, Tard_e, Tard_a
                obs_t = np.expand_dims(obs_t, 0)
                # obs = obs_t
                # obs = np.expand_dims(obs, 0)
                # print(obs,obs_t)
                '''执行动作后，根据新状态获得奖励'''
                r_t = Sit.reward(obs[0][6], obs[0][5], obs_t[0][6], obs_t[0][5], obs[0][0], obs_t[0][0])  # 根据新的状态获得奖励
                '''将此数据记录'''
                self._append((obs, at, r_t, obs_t, done))  # 将词条数据（状态特征、动作选择、奖励、下个状态、结束标志）存储
                '''记录大小为Batch_size的数据,训练数据，更新Q'''
                if k > self.Batch_size:
                    # batch_obs, batch_action, batch_reward, batch_next_obs, done= self.sample()
                    self.replay()  #
                Total_reward += r_t
                obs = obs_t
            total_tardiness = 0
            Job = Sit.Jobs
            # E = 0
            # K = [i for i in range(len(Job))]  # 工件遍历
            End = []
            for Ji in range(len(Job)):
                End.append(max(Job[Ji].End))
                if max(Job[Ji].End) > D[Ji]:
                    total_tardiness += abs(max(Job[Ji].End) - D[Ji])
            print('<<<<<<<<<-----------------total_tardiness:', total_tardiness, '------------------->>>>>>>>>>')
            Total_tard.append(total_tardiness)
            print('<<<<<<<<<-----------------reward:', Total_reward, '------------------->>>>>>>>>>')
            TR.append(Total_reward)
            # plt.plot(K,End,color='y')
            # plt.plot(K,D,color='r')
            # plt.show()
        plt.figure(1)
        plt.plot(x, Total_tard)
        plt.figure(2)
        plt.plot(x, TR)
        plt.show()
        return Total_reward


d = DQN()
d.main(J_num, M_num, O_num, J, Processing_time, D, A)