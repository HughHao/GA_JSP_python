function Chrom=Cross(Chrom,best_flag,NIND,XOVR,WNumber)
ChromNew=Chrom;
for mm=best_flag+1:2:NIND-1%ѡ�������Ⱦɫ����н���
    rd=rand;
    if XOVR>rd %�������=0.2
        
        %ȡ�����ĸ���;
        if best_flag==NIND% �������Ⱥ���Ÿ���ﵽ�����������
            break
        end
        S1=Chrom(mm,:);
        S2=Chrom(mm+1,:);%mm+1��ʼ��Ⱦɫ��
        A=S1;%A��Chrome�е�mm��Ⱦɫ��
        B=S2;
        n=fix(WNumber*rand);%ȡ��Сֵ
        C=[A(1:n) B(n+1:WNumber)];%Ⱦɫ�峤��ΪWNumber
        D=[B(1:n) A(n+1:WNumber)];%�����ĳ���Ⱦɫ��
        % ������벿��
        c1=sum(C(n+1:WNumber)==1);%����1
        d1=sum(D(n+1:WNumber)==1);%
        c2=sum(C(n+1:WNumber)==2);%����2
        d2=sum(D(n+1:WNumber)==2);
        c3=sum(C(n+1:WNumber)==3);%����3
        d3=sum(D(n+1:WNumber)==3);
        c4=sum(C(n+1:WNumber)==4);%����4
        d4=sum(D(n+1:WNumber)==4);
        c5=sum(C(n+1:WNumber)==5);%����5
        d5=sum(D(n+1:WNumber)==5);
        c6=sum(C(n+1:WNumber)==6);%����6
        d6=sum(D(n+1:WNumber)==6);
        % ����˼��Ϊ�Ժ��潻�沿�ֽ���ͳ�ƣ�
        
        E=[ones(1,6-c1) 2*ones(1,6-c2) 3*ones(1,6-c3) 4*ones(1,6-c4) 5*ones(1,6-c5) 6*ones(1,6-c6) C(n+1:WNumber)];%����C
        % ��CȾɫ����в���
        F=[ones(1,6-d1) 2*ones(1,6-d2) 3*ones(1,6-d3) 4*ones(1,6-d4) 5*ones(1,6-d5) 6*ones(1,6-d6) D(n+1:WNumber)];%����D
        ex1=E(1,1:n);%ȡ������λ����֮ǰ��Ԫ�طŵ�ex1��ex2��
        % 
        % WNumber-c1-c2-c3-c4-c5-c6 == n
        ex2=F(1,1:n);
        ex1=ex1(randperm(numel(ex1)));
        ex2=ex2(randperm(numel(ex2)));
        E=[ex1 E(n+1:WNumber)];
        F=[ex2 F(n+1:WNumber)];
        %            %������Ⱥ
        ChromNew(mm,:)=E;
        ChromNew(mm+1,:)=F;
    end
end% % %��ֹ��������� ʵ���˽��棬���½��б������
Chrom=ChromNew;