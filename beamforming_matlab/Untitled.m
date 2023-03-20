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

tau = gccphat(audio(2,:)',audio(7,:)',48000);
disp("使用gcc-phat时延为");
disp(tau);
figure(3);
t=1:length(tau);
plot(lag,real(R(:,1)));

% [rcc,lag] = xcorr(audio(1,:),audio(5,:));
% figure(4);
% plot(lag/Fs,rcc);
% [M,I] = max(abs(rcc));
% lagDiff = lag(I);
% timeDiff = lagDiff/Fs;
% disp("使用自相关的时延为");
% disp(timeDiff);

