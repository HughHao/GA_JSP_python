function Chrom=Mutation(Chrom,best_flag,NIND,MUTR,WNumber)
ChromNew=Chrom;

for i=best_flag+1:NIND  %�Ƿ����
    mt=rand;
    if MUTR>mt
        Pos1=unidrnd(WNumber);%����λ��
        Pos2=unidrnd(WNumber);
        
        %����λ�ò���ͬ
        while Pos1==Pos2
            Pos2=unidrnd(WNumber);
        end
        
        %ȡ����
        S=Chrom(i,:);
        
        %����
        temp=S(Pos1);
        S(Pos1)=S(Pos2);
        S(Pos2)=temp;
        
        ChromNew(i,:)=S;
    end
end
Chrom=ChromNew;