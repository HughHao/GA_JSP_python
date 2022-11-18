function Chrom=Mutation(Chrom,best_flag,NIND,MUTR,WNumber)
ChromNew=Chrom;

for i=best_flag+1:NIND  %是否变异
    mt=rand;
    if MUTR>mt
        Pos1=unidrnd(WNumber);%变异位置
        Pos2=unidrnd(WNumber);
        
        %变异位置不相同
        while Pos1==Pos2
            Pos2=unidrnd(WNumber);
        end
        
        %取数据
        S=Chrom(i,:);
        
        %交换
        temp=S(Pos1);
        S(Pos1)=S(Pos2);
        S(Pos2)=temp;
        
        ChromNew(i,:)=S;
    end
end
Chrom=ChromNew;