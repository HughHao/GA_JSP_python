function []=draw_fig(P,M,T,pro_length,FT)
job_num=size(FT,1);
t=zeros(max(M),1);  % M为各个工序的加工位置
t_bz=cell(job_num,1);
for i=1:job_num
    t_bz{i}=i*ones(1,size(FT{i},1));
end
D=cell(pro_length,1);
for m=1:pro_length
    D{m}=zeros(1,2);
end
for k=1:pro_length
    x=floor(P(k)/10);% x为工件号
    y=rem(P(k),10);% y为工序号
    if y==0
        x=floor(P(k)/100);
        y=rem(P(k),100);
    end
    if y==1%显然，如果该工序为第一个工序，则M1机床时间t1直接为当前时间加上该工序的时间
        D{k}(1,1)=t(M(k));
        t(M(k))=t(M(k))+T(k);%t1表示机床1加工本道工序结束时间
        D{k}(1,2)=t(M(k));
        t_bz{x}(y)=t(M(k));%第x工件的第y道工序结束时的时间。下道工序开始时间
        %t_bz即为3*3的零矩阵，用于存储各个工序在机床上对应的机床时间，行数代表工件号，列数代表工序
    else %如果该工序不是第一个工序：temp1为一个中间变量，元素为该机床当前的时间t1、以及该工件上一工序所在机床的对应机床时间
        temp1=[t(M(k)) t_bz{x}(y-1)];%本道工序的前一道工序和本机床的前一道工序时间的最大值
        D{k}(1,1)=max(temp1);
        t(M(k))=D{k}(1,1)+T(k);%选择两者之中的较大值，即为该工件在1机床上（2 3机床同理）上对应的机床时间
        D{k}(1,2)=t(M(k));
        t_bz{x}(y)=t(M(k));%将该时间赋值到时间矩阵
    end
end
T_MAX=max(t);
figure(2);clf
w=0.8; % 横条宽度
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
