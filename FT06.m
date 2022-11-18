function FT06
clear;clc;close all
tic
FT={[11 3 1;12 1 3;13 2 6;14 4 7;15 6 3;16 5 6]
    [21 2 8;22 3 5;23 5 10;24 6 10;25 1 10;26 4 4]
    [31 3 5;32 4 4;33 6 8;34 1 9;35 2 1;36 5 7]
    [41 2 5;42 1 5;43 3 5;44 4 3;45 5 8;46 6 9]
    [51 3 9;52 2 3;53 5 5;54 6 4;55 1 3;56 4 1]
    [61 2 3;62 4 3;63 6 9;64 1 10;65 5 4;66 3 1]};
% FT={[11 0 29;12 1 78;13 2  9;14 3 36;15 4 49;16 5 11;17 6 62;18 7 56;19 8 44;110 9 21]
% [21 0 43;22 2 90;23 4 75;24 9 11;25 3 69;26 1 28;27 6 46;28 5 46;29 7 72;210 8 30]
% [31 1 91;32 0 85;33 3 39;34 2 74;35 8 90;36 5 10;37 7 12;38 6 89;39 9 45;310 4 33]
% [41 1 81;42 2 95;43 0 71;44 4 99;45 6  9;46 8 52;47 7 85;48 3 98;49 9 22;410 5 43]
% [51 2 14;52 0  6;53 1 22;54 5 61;55 3 26;56 4 69;57 8 21;58 7 49;59 9 72;510 6 53]
% [61 2 84;62 1  2;63 5 52;64 3 95;65 8 48;66 9 72;67 0 47;68 6 65;69 4  6;610 7 25]
% [71 1 46;72 0 37;73 3 61;74 2 13;75 6 32;76 5 21;77 9 32;78 8 89;79 7 30;710 4 55]
% [81 2 31;82 0 86;83 1 46;84 5 74;85 4 32;86 6 88;87 8 19;88 9 48;89 7 36;810 3 79]
% [91 0 76;92 1 69;93 3 76;94 5 51;95 2 85;96 9 11;97 6 40;98 7 89;99 4 26;910 8 74]
% [101 1 85;102 0 13;103 2 61;104 6  7;105 8 64;106 9 76;107 5 47;108 3 52;109 4 90;1010 7 45]};
% FT={[11 1 1;12 2 3;13 3 6;14 4 7;15 5 3;16 6 6]
%     [21 1 8;22 2 5;23 3 10;24 4 10;25 5 10;26 6 4]
%     [31 1 5;32 2 4;33 3 8;34 4 9;35 5 1;36 6 7]
%     [41 1 5;42 2 5;43 3 5;44 4 3;45 5 8;46 6 9]
%     [51 1 9;52 2 3;53 3 5;54 4 4;55 5 3;56 6 1]
%     [61 1 3;62 2 3;63 3 9;64 4 10;65 5 4;66 6 1]};
seed=JOB_PRO(FT);%种子
seed_length=length(seed);
Chrom=zeros(20,seed_length);%预定义零矩阵，用于存数染色体
NIND=size(Chrom,1);%种群大小20
WNumber=seed_length;%染色体长度为36
XOVR=0.7;%交叉概率=0.2
MUTR=0.1;
for i=1:NIND
    Chrom(i,:)=seed(randperm(numel(seed)));%生成染色体并赋到矩阵各行
end
time_opt=zeros(NIND,400);  % 预定义20*100的矩阵存储100代种群中的各个个体时间
generations=400;
PP=zeros(NIND,WNumber);  % 工序数，每个染色体的各工序
MM=zeros(NIND,WNumber);  % 机器，每个种群染色体的各工序加工位置
TT=zeros(NIND,WNumber);  % 时间
T_qunti=zeros(NIND,1);  % 每条染色体的适应度
for generation=1:generations
    for i=1:NIND
        [P,M,T]=PMT1(Chrom(i,:),WNumber,FT);
        T_qunti(i)=Calculate(P,M,T,WNumber,FT);
        PP(i,:)=P;
        MM(i,:)=M;
        TT(i,:)=T;
    end
    time_add=sum(T_qunti); %计算出种群中各个染色体总时间和
    time_indiv=T_qunti/time_add; %计算每一个个体与总时间的比值
    [min_time,index]=min(T_qunti);%该代种群中时间最短的个体时间
    P_best=PP(index,:);
    M_best=MM(index,:);
    T_best=TT(index,:);
    [Chrom,best_flag]=Copy(Chrom,NIND,T_qunti,min_time,time_indiv);
    Chrom=Cross(Chrom,best_flag,NIND,XOVR,WNumber);
    Chrom=Mutation(Chrom,best_flag,NIND,MUTR,WNumber);
    time_opt(:,generation)=T_qunti;%时间矩阵，用来存储N代种群中各个染色体的时间
    pp=T_qunti==min_time;%pp记录T_qunti中与最小时间个体相同的个体数量（为20*1的矩阵）
    min_Time(generation)=min_time;
    pingjun(generation)=mean(T_qunti);
    zonghe(generation)=sum(pp);
end
toc
%% 绘图
figure()% 定义figure1 绘图窗口，显示群体进化过程中时间的平均值变换
hold on
%        plot(zonghe(:),'k-')
%        plot(pingjun(:),'k-')
plot(min_Time(:),'k-')
xlabel('iterations');
ylabel('time');
%  legend('种群中含有最优值的个数','均值的变化','最优值的变化');
disp('最优加工时间为:')
min_Time(generations)
disp('解码后对应最优个体的加工顺序为：')
P_best
P=P_best;
M=M_best;
T=T_best;
draw_fig(P,M,T,WNumber,FT)
