net=feedforwardnet([10 10 10]);%���ز���������Ԫ����
net.trainFcn = 'trainscg'%ѡ��ѵ����ʽ
net.performFcn= 'mse'; 
%��������ָ�꣬�Ҿ������˴��ţ�����Ĭ�ϵ�mse���С�����֮�⣬����mae��ƽ����������sae������ֵ������sse��ƽ��������crossentropy�������أ���
 net.trainParam.show=1;
%����Ǹ���ͼ��ˢ��Ƶ�ʵģ�ÿ���ٸ�����ˢ��һ�Ρ�
 net.trainParam.lr=0.2;
%ѧϰ�ʣ��Ĳ�������ν����Щ�½�����������Ӧѧϰ�ʵģ�����Ҳû�á�
 net.trainParam.max_fail=100;
%�����ֶ��ٴ��½�ʧ��ʱֹͣѵ����������100�Ρ�
 net.trainParam.epochs=1e3;
%����������
 net.trainParam.goal=0;
%��ѵ����������ָ��ﵽ����ʱֹͣѵ��
 net.trainParam.min_grad=0;
%���½��ݶȴﵽ����ʱֹͣѵ��
 net.layers{1}.transferFcn='tansig';
 net.layers{2}.transferFcn='tansig';
 net.layers{3}.transferFcn='tansig';
 net.layers{4}.transferFcn='tansig';%���һ��
%�������ǳ�ʼ����ʱ������ṹѡ����[12 12 12]���������������Ϊ5�㡣Ҳ����˵��4�����ݹ��̣��������ʼ����4.
net.divideParam.trainRatio=0.8;
net.divideParam.valRatio=0.1;
net.divideParam.testRatio=0.1;
%ѵ��50%����֤20%������30%
%��ѡһ��û��GPU�Ŀ�GPU�ᱨ��
%[net,tr]=train(net,inputn,outputn);
%����ģʽ
 %[net,tr]=train(net,inputn,outputn,'UseParallel','yes');
%������
 [net,tr]=train(net,delay',pointspos','UseParallel','yes','UseGPU','no');
%������+��GPU


view(net)
y = net(delay');
perf = perform(net,y,pointspos')