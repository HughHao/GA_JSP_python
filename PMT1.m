function [P,M,T] = PMT1(job_pro,pro_length,FT)
job_num=size(FT,1);
a=ones(job_num,1);
P=zeros(pro_length,1);%工序
M=zeros(pro_length,1);%机床
T=zeros(pro_length,1);%时间
for j=1:pro_length
    P(j)=FT{job_pro(j)}(a(job_pro(j)),1);  % P为[11 21 33 23...]类列表
    M(j)=FT{job_pro(j)}(a(job_pro(j)),2)+1;
    T(j)=FT{job_pro(j)}(a(job_pro(j)),3);
    a(job_pro(j))=a(job_pro(j))+1;
end
