function [new_Chrom,best_flag]=Copy(old_Chrom,NIND,T_qunti,min_time,time_indiv)
next_pop=old_Chrom;%初始化群体
best_flag=0;
for tt=1:NIND
    if T_qunti(tt)==min_time %如果该个体为截止到当前代最好的个体，则保留
        best_flag=best_flag+1;
        next_pop(best_flag,:)=old_Chrom(tt,:);
        time_indiv(tt)=2;% 如果该个体为该代中最优，则将该个体直接复制到下一代，然后将time_indiv赋值为2，以避开交叉和变异
    end
end
flag=best_flag;
% while flag<NIND
for z=1:NIND %下一代群体的前flag个个体直接取上一带的最佳个体，剩下的个体用随即方法选择
    if flag<NIND
        sj=rand;
        if  time_indiv(z)<sj %如果随机数大于第i个染色体的概率，认为该染色体较好，保留
            next_pop(flag+1,:)=old_Chrom(z,:);
            flag=flag+1;
        end
    end
end
new_Chrom=next_pop;