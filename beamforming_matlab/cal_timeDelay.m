clc
clear all
close all

data_path='C:\Users\林海\Desktop\audio\mica_channel_array_0_2等7个文件\outwav\';
type='*.wav';
filelist = dir([data_path type]); % 获取当前文件夹下所有wav文件的名字

% filelist = dir('*.wav'); % 获取当前文件夹下所有wav文件的名字
n = length(filelist); % 获取文件个数
audio = []; % 初始化音频数据矩阵
Fs = []; % 初始化采样频率矩阵
for i = 1:n % 用for循环逐个读取文件
    [audioi,Fsi] = audioread(filelist(i).name); % 读取第i个文件的音频数据和采样频率
    audio = [audio;audioi']; % 将音频数据拼接到矩阵y中
    Fs = [Fs;Fsi]; % 将采样频率拼接到矩阵Fs中
end
l=length(audio(1,:));
xl=1:1:l;
% figure;
% plot(xl,movmean(audio(5,:),64));


% 
% % 生成两个信号x (t)和y (t)，都是50Hz的正弦信号，但y (t)有一个相位延迟 
% t = 0:0.001:0.2; 
% % 时间向量 
% x = cos (2*pi*50*t);%+randn (size (t)); % x (t)信号 
% y = cos (2*pi*50*(t-0.005));%+randn (size (t)); % y (t)信号，相位延迟0.01秒
% figure;
% plot(t,x,t,y);
fs=48000
x=audio(2,:);
y=fft(x);
Fs=48000;
n=length(x);
t=1:1:n;
L=length(t);
f=Fs*(0:n/2)/n;
p=abs(y/n);
plot(f,p(1:n/2+1));

xlabel('频率 (Hz)');

title('声音信号的频谱图');

time_Delay_matrix=[];
for i=1:length(audio(:,1))
    for j=i+1:length(audio(:,1))
        % 计算x和y的交叉功率谱密度（CPSD） 
        [Pxy,f] = cpsd(audio(i,:),audio(j,:),hann(2048),1024,2048,48000); % 使用汉宁窗分割信号，并指定采样频率为48000Hz
        Pxy2=Pxy;
%         [Cxy,F] = mscohere(audio(i,:),audio(j,:),hann(2048),1024,2048,48000);
%         [maxR,index]=max(Cxy)

%         figure;subplot(1,1,1)
%         plot(F,Cxy)
%         title('Magnitude-Squared Coherence')

%         % 绘制CPSD的幅值和相位曲线 
        figure; subplot(2,1,1); % 上图为幅值曲线 
        plot(f,abs(Pxy)); % 绘制频率与幅值的关系 
        xlabel('Frequency (Hz)'); % x轴标签为频率 
        ylabel('Magnitude'); % y轴标签为幅值 
        title('Cross Power Spectral Density of x and y'); % 标题为CPSD

        % 假设已经有了一个包含所有[Pxy,f]元组的矩阵 tuples_matrix
        tuples_matrix=[abs(Pxy),f];
        x = 1600; % 设定最低频率x的值
        logical_index = tuples_matrix(:,2)>x; % 找出第一列大于x的行对应的逻辑向量
        result = tuples_matrix(logical_index,:); % 使用逻辑向量进行索引，得到符合条件的行
        result = result(1:sum(logical_index),:);
        x = 10; % 需要找到最大的10个Pxy及其对应的f
        sorted_matrix = sortrows(result, -1); % 按照第一列（Pxy）从大到小排序
        top_x_tuples = sorted_matrix(1:x, :); % 取前x行即为所需结果
        logical_index = ismember(f,top_x_tuples(:,2)); % 找到需要提取的索引的行
        Pxy=Pxy(logical_index,:);


       
        delay=[top_x_tuples(:,2),-angle(Pxy)./top_x_tuples(:,2)/2/pi];
        subplot(2,1,2); % 下图为相位曲线 
        plot(f,-angle(Pxy2)./f/2/pi); % 绘制频率与相位差的关系，转换为角度单位 
        xlabel('Frequency (Hz)'); % x轴标签为频率 
        ylabel('Phase difference (degrees)'); % y轴标签为相位差 
        title('Phase difference between x and y'); % 标题为相位差


        
        tda=median(delay(:,2));
        time_Delay_matrix=[time_Delay_matrix;[tda;i;j]'];
    end
end