clc
clear all
close all

data_path='C:\Users\林海\Desktop\audio\mica_channel_array_0_2等7个文件\outwav\';
type='*.wav';
filelist = dir([data_path type]); % 获取当前文件夹下所有wav文件的名字
n = length(filelist); % 获取文件个数
audio = []; % 初始化音频数据矩阵
Fs = []; % 初始化采样频率矩阵
for i = 1:n % 用for循环逐个读取文件
    [audioi,Fsi] = audioread(filelist(i).name); % 读取第i个文件的音频数据和采样频率
    audio = [audio;audioi']; % 将音频数据拼接到矩阵y中
    Fs = [Fs;Fsi]; % 将采样频率拼接到矩阵Fs中
end
l=length(audio(1,:));
R = audio*audio'/l; % 接收数据的自协方差矩阵  A.'是一般转置，A'是共轭转置

%% ------------------------------初始化常量-------------------------------%
c = 340;   % 声速c
fs = 1000;   % 抽样频率fs
T = 0.1;   % ??
t = 0:1/fs:T;  % 时间 [0, 0.1]
L = length(t); % 时间长度:101
f = 500;   % 感兴趣的频率
w = 2*pi*f;  % 角频率
k = w/c;   % 波数 k

%% ------------------------------各阵元坐标-------------------------------%
M = 7;   % 阵元个数
% Nmid = 12;      % 参考点
% d = 3;         % 阵元间距
% m = (0:1:M-1) 
yi = zeros(M,1); % 生成一个M*1维的零矩阵
zi = [0; 0.04; 0.02000003064100781; -0.019999938717937437; -0.03999999999985917; -0.020000122563937347; 0.019999846794726262];
xi = [0; 0.0; 0.03464099846076537; 0.03464105153252059; 1.0614359175187277e-07; -0.03464094538876623; -0.034641104604031865];
%xi = xi.'      % 列向量 m*d 阵元数*阵元间距


figure(1)
plot(xi,zi,'r*');
title('圆形麦克风阵列')

%% ----------------------------------扫描范围----------------------------------%
% 我们设置步长为0.1，扫描范围是20x20的平面，双重for循环得到M*1矢量矩阵，最后得到交叉谱矩阵（cross spectrum matrix）
% 由DSP理论，这个就是声音的功率。
x2 = 0;  % array center
y2 = 0;
z2 = 0;


step_x = 0.02;  % 步长设置为0.1
step_z = 0.02;
y = 0;
x = (-3:step_x:3);  % 扫描范围 9-15
z = (-3:step_z:3); 

for k1=1:length(z)
    for k2=1:length(x)
        Ri = sqrt((x(k2)-xi).^2+(y-yi).^2+(z(k1)-zi).^2);  % 该扫描点到各阵元的聚焦距离矢量
        Ri2 = sqrt((x(k2)-x2).^2+(y-y2).^2+(z(k1)-z2).^2);  % 10.8628
        Rn = Ri-Ri2;   % 扫描点到各阵元与参考阵元的程差矢量
        b = exp(-j*w*Rn/c); % 声压聚焦方向矢量
        Pcbf(k1,k2) = abs(b'*R*b); % CSM,最关键,(1,18)*(18,18)*(18,1)
    end
end


for k1 = 1:length(z)
    pp(k1) = max(Pcbf(k1,:)); % Pcbf 的第k1行的最大元素的值
    pp2(k1) = min(Pcbf(k1,:)); % Pcbf 的第k1行的最大元素的值
end

Pcbf = Pcbf/max(pp);  % 所有元素除以其最大值 归一化幅度, (61,61)


%% -------------------------------------作图展示------------------------------------%
figure(2)
surf(x,z,Pcbf);
xlabel('x(m)'),ylabel('z(m)')
title('三维单声源图')
colorbar
 
figure(3)
pcolor(x,z,Pcbf);
shading interp;
xlabel('x(m)');
ylabel('z(m)');
title('单声源图')
colorbar