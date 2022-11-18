function Chrom=Cross(Chrom,best_flag,NIND,XOVR,WNumber)
ChromNew=Chrom;
for mm=best_flag+1:2:NIND-1%选择非最优染色体进行交叉
    rd=rand;
    if XOVR>rd %交叉概率=0.2
        
        %取交换的个体;
        if best_flag==NIND% 如果该种群最优个体达到最大，跳出交叉
            break
        end
        S1=Chrom(mm,:);
        S2=Chrom(mm+1,:);%mm+1开始的染色体
        A=S1;%A是Chrome中第mm个染色体
        B=S2;
        n=fix(WNumber*rand);%取较小值
        C=[A(1:n) B(n+1:WNumber)];%染色体长度为WNumber
        D=[B(1:n) A(n+1:WNumber)];%交叉后的初步染色体
        % 交换后半部分
        c1=sum(C(n+1:WNumber)==1);%工件1
        d1=sum(D(n+1:WNumber)==1);%
        c2=sum(C(n+1:WNumber)==2);%工件2
        d2=sum(D(n+1:WNumber)==2);
        c3=sum(C(n+1:WNumber)==3);%工件3
        d3=sum(D(n+1:WNumber)==3);
        c4=sum(C(n+1:WNumber)==4);%工件4
        d4=sum(D(n+1:WNumber)==4);
        c5=sum(C(n+1:WNumber)==5);%工件5
        d5=sum(D(n+1:WNumber)==5);
        c6=sum(C(n+1:WNumber)==6);%工件6
        d6=sum(D(n+1:WNumber)==6);
        % 交叉思想为对后面交叉部分进行统计，
        
        E=[ones(1,6-c1) 2*ones(1,6-c2) 3*ones(1,6-c3) 4*ones(1,6-c4) 5*ones(1,6-c5) 6*ones(1,6-c6) C(n+1:WNumber)];%重排C
        % 对C染色体进行补充
        F=[ones(1,6-d1) 2*ones(1,6-d2) 3*ones(1,6-d3) 4*ones(1,6-d4) 5*ones(1,6-d5) 6*ones(1,6-d6) D(n+1:WNumber)];%重排D
        ex1=E(1,1:n);%取出交叉位及其之前的元素放到ex1和ex2中
        % 
        % WNumber-c1-c2-c3-c4-c5-c6 == n
        ex2=F(1,1:n);
        ex1=ex1(randperm(numel(ex1)));
        ex2=ex2(randperm(numel(ex2)));
        E=[ex1 E(n+1:WNumber)];
        F=[ex2 F(n+1:WNumber)];
        %            %放入新群
        ChromNew(mm,:)=E;
        ChromNew(mm+1,:)=F;
    end
end% % %截止到该行语句 实现了交叉，以下进行变异操作
Chrom=ChromNew;