function [new_Chrom,best_flag]=Copy(old_Chrom,NIND,T_qunti,min_time,time_indiv)
next_pop=old_Chrom;%��ʼ��Ⱥ��
best_flag=0;
for tt=1:NIND
    if T_qunti(tt)==min_time %����ø���Ϊ��ֹ����ǰ����õĸ��壬����
        best_flag=best_flag+1;
        next_pop(best_flag,:)=old_Chrom(tt,:);
        time_indiv(tt)=2;% ����ø���Ϊ�ô������ţ��򽫸ø���ֱ�Ӹ��Ƶ���һ����Ȼ��time_indiv��ֵΪ2���Աܿ�����ͱ���
    end
end
flag=best_flag;
% while flag<NIND
for z=1:NIND %��һ��Ⱥ���ǰflag������ֱ��ȡ��һ������Ѹ��壬ʣ�µĸ������漴����ѡ��
    if flag<NIND
        sj=rand;
        if  time_indiv(z)<sj %�����������ڵ�i��Ⱦɫ��ĸ��ʣ���Ϊ��Ⱦɫ��Ϻã�����
            next_pop(flag+1,:)=old_Chrom(z,:);
            flag=flag+1;
        end
    end
end
new_Chrom=next_pop;