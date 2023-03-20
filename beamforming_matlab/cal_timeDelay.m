clc
clear all
close all

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
l=length(audio(1,:));
xl=1:1:l;
% figure;
% plot(xl,movmean(audio(5,:),64));


% 
% % ���������ź�x (t)��y (t)������50Hz�������źţ���y (t)��һ����λ�ӳ� 
% t = 0:0.001:0.2; 
% % ʱ������ 
% x = cos (2*pi*50*t);%+randn (size (t)); % x (t)�ź� 
% y = cos (2*pi*50*(t-0.005));%+randn (size (t)); % y (t)�źţ���λ�ӳ�0.01��
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

xlabel('Ƶ�� (Hz)');

title('�����źŵ�Ƶ��ͼ');

time_Delay_matrix=[];
for i=1:length(audio(:,1))
    for j=i+1:length(audio(:,1))
        % ����x��y�Ľ��湦�����ܶȣ�CPSD�� 
        [Pxy,f] = cpsd(audio(i,:),audio(j,:),hann(2048),1024,2048,48000); % ʹ�ú������ָ��źţ���ָ������Ƶ��Ϊ48000Hz
        Pxy2=Pxy;
%         [Cxy,F] = mscohere(audio(i,:),audio(j,:),hann(2048),1024,2048,48000);
%         [maxR,index]=max(Cxy)

%         figure;subplot(1,1,1)
%         plot(F,Cxy)
%         title('Magnitude-Squared Coherence')

%         % ����CPSD�ķ�ֵ����λ���� 
        figure; subplot(2,1,1); % ��ͼΪ��ֵ���� 
        plot(f,abs(Pxy)); % ����Ƶ�����ֵ�Ĺ�ϵ 
        xlabel('Frequency (Hz)'); % x���ǩΪƵ�� 
        ylabel('Magnitude'); % y���ǩΪ��ֵ 
        title('Cross Power Spectral Density of x and y'); % ����ΪCPSD

        % �����Ѿ�����һ����������[Pxy,f]Ԫ��ľ��� tuples_matrix
        tuples_matrix=[abs(Pxy),f];
        x = 1600; % �趨���Ƶ��x��ֵ
        logical_index = tuples_matrix(:,2)>x; % �ҳ���һ�д���x���ж�Ӧ���߼�����
        result = tuples_matrix(logical_index,:); % ʹ���߼����������������õ�������������
        result = result(1:sum(logical_index),:);
        x = 10; % ��Ҫ�ҵ�����10��Pxy�����Ӧ��f
        sorted_matrix = sortrows(result, -1); % ���յ�һ�У�Pxy���Ӵ�С����
        top_x_tuples = sorted_matrix(1:x, :); % ȡǰx�м�Ϊ������
        logical_index = ismember(f,top_x_tuples(:,2)); % �ҵ���Ҫ��ȡ����������
        Pxy=Pxy(logical_index,:);


       
        delay=[top_x_tuples(:,2),-angle(Pxy)./top_x_tuples(:,2)/2/pi];
        subplot(2,1,2); % ��ͼΪ��λ���� 
        plot(f,-angle(Pxy2)./f/2/pi); % ����Ƶ������λ��Ĺ�ϵ��ת��Ϊ�Ƕȵ�λ 
        xlabel('Frequency (Hz)'); % x���ǩΪƵ�� 
        ylabel('Phase difference (degrees)'); % y���ǩΪ��λ�� 
        title('Phase difference between x and y'); % ����Ϊ��λ��


        
        tda=median(delay(:,2));
        time_Delay_matrix=[time_Delay_matrix;[tda;i;j]'];
    end
end