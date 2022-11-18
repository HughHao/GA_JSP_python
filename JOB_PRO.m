function job_pro=JOB_PRO(FT)
job_num=size(FT,1);
job_pro=[];
for i=1:job_num
    pro=i*ones(1,size(FT{i},1));
    job_pro=[pro job_pro];
end
