function []=draw_fig(P,M,T,pro_length,FT)
job_num=size(FT,1);
t=zeros(max(M),1);  % MΪ��������ļӹ�λ��
t_bz=cell(job_num,1);
for i=1:job_num
    t_bz{i}=i*ones(1,size(FT{i},1));
end
D=cell(pro_length,1);
for m=1:pro_length
    D{m}=zeros(1,2);
end
for k=1:pro_length
    x=floor(P(k)/10);% xΪ������
    y=rem(P(k),10);% yΪ�����
    if y==0
        x=floor(P(k)/100);
        y=rem(P(k),100);
    end
    if y==1%��Ȼ������ù���Ϊ��һ��������M1����ʱ��t1ֱ��Ϊ��ǰʱ����ϸù����ʱ��
        D{k}(1,1)=t(M(k));
        t(M(k))=t(M(k))+T(k);%t1��ʾ����1�ӹ������������ʱ��
        D{k}(1,2)=t(M(k));
        t_bz{x}(y)=t(M(k));%��x�����ĵ�y���������ʱ��ʱ�䡣�µ�����ʼʱ��
        %t_bz��Ϊ3*3����������ڴ洢���������ڻ����϶�Ӧ�Ļ���ʱ�䣬�����������ţ�����������
    else %����ù����ǵ�һ������temp1Ϊһ���м������Ԫ��Ϊ�û�����ǰ��ʱ��t1���Լ��ù�����һ�������ڻ����Ķ�Ӧ����ʱ��
        temp1=[t(M(k)) t_bz{x}(y-1)];%���������ǰһ������ͱ�������ǰһ������ʱ������ֵ
        D{k}(1,1)=max(temp1);
        t(M(k))=D{k}(1,1)+T(k);%ѡ������֮�еĽϴ�ֵ����Ϊ�ù�����1�����ϣ�2 3����ͬ���϶�Ӧ�Ļ���ʱ��
        D{k}(1,2)=t(M(k));
        t_bz{x}(y)=t(M(k));%����ʱ�丳ֵ��ʱ�����
    end
end
T_MAX=max(t);
figure(2);clf
w=0.8; % �������
set(gcf,'color','w');
A=cell(pro_length,1);
for jj=1:pro_length
    A(jj)={[M(jj) P(jj) D{jj}(1,1) D{jj}(1,2)]};
end
for ii=1:pro_length
    B=A{ii};
    x=B(1,[3 3 4 4]);
    y=B(1,1)+[-w/2 w/2 w/2 -w/2];
    patch('xdata',x,'ydata',y,'facecolor','none','edgecolor','k');
    text(B(1,3),B(1,1),num2str(B(1,2)));
end
xlabel('processing time(s)');
ylabel('Machine');
axis([0  T_MAX+5 0.5 job_num+0.5]);
set(gca,'Box','on')
