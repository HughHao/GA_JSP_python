function fit=Calculate(P,M,T,pro_length,FT)
job_num=size(FT,1);
t=zeros(max(M),1);
t_bz=cell(job_num,1);
for i=1:job_num
    t_bz{i}=i*ones(1,size(FT{i},1));
end
for k=1:pro_length
    x=floor(P(k)/10);% xΪ������
    y=rem(P(k),10);% yΪ�����
    if y==0
        x=floor(P(k)/100);
        y=rem(P(k),100);
    end
    if y==1%��Ȼ������ù���Ϊ��һ��������M1����ʱ��t1ֱ��Ϊ��ǰʱ����ϸù����ʱ��
%         disp([M(k),k])
        t(M(k))=t(M(k))+T(k);%t1��ʾ���豸1�ϼӹ���ʱ��
        t_bz{x}(y)=t(M(k));%��x�����ĵ�y���������ʱ��ʱ�䡣��32��,�ڳ����ʼ���������Ѿ�Ԥ����t_bz=zeros(3,3);
        %t_bz��Ϊ3*3����������ڴ洢���������ڻ����϶�Ӧ�Ļ���ʱ�䣬�����������ţ�����������
    else %����ù����ǵ�һ������temp1Ϊһ���м������Ԫ��Ϊ�û�����ǰ��ʱ��t1���Լ��ù�����һ�������ڻ����Ķ�Ӧ����ʱ��
        temp1=[t(M(k)) t_bz{x}(y-1)];
        t(M(k))=max(temp1)+T(k);%ѡ������֮�еĽϴ�ֵ����Ϊ�ù�����1�����ϣ�2 3����ͬ���϶�Ӧ�Ļ���ʱ��
        t_bz{x}(y)=t(M(k));%����ʱ�丳ֵ��ʱ�����
    end
end
fit=max(t);
