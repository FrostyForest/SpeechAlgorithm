data_path='C:\Users\�ֺ�\Desktop\audio\mica_channel_array_0_2��7���ļ�\outwav\';
type='*.wav';
filelist = dir([data_path type]); % ��ȡ��ǰ�ļ���������wav�ļ�������

% filelist = dir('*.wav'); % ��ȡ��ǰ�ļ���������wav�ļ�������
n = length(filelist); % ��ȡ�ļ�����
audio = []; % ��ʼ����Ƶ���ݾ���
Fs = []; % ��ʼ������Ƶ�ʾ���
for i = 1:n % ��forѭ�������ȡ�ļ�
    [audioi,Fsi] = audioread(filelist(i).name); % ��ȡ��i���ļ�����Ƶ���ݺͲ���Ƶ��
    audio = [audio;audioi']; % ����Ƶ����ƴ�ӵ�����y��
    Fs = [Fs;Fsi]; % ������Ƶ��ƴ�ӵ�����Fs��
end

tau = gccphat(audio(2,:)',audio(7,:)',48000);
disp("ʹ��gcc-phatʱ��Ϊ");
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
% disp("ʹ������ص�ʱ��Ϊ");
% disp(timeDiff);

