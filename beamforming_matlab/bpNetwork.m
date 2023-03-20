net=feedforwardnet([10 10 10]);%隐藏层数量和神经元个数
net.trainFcn = 'trainscg'%选择训练方式
net.performFcn= 'mse'; 
%性能评价指标，我觉得无伤大雅，按照默认的mse就行。除此之外，还有mae（平均绝对误差）、sae（绝对值和误差）、sse（平方和误差）、crossentropy（交叉熵）。
 net.trainParam.show=1;
%这个是负责图像刷新频率的，每多少个数据刷新一次。
 net.trainParam.lr=0.2;
%学习率，改不改无所谓，有些下降方法是自适应学习率的，改了也没用。
 net.trainParam.max_fail=100;
%当出现多少次下降失败时停止训练，这里是100次。
 net.trainParam.epochs=1e3;
%最大迭代次数
 net.trainParam.goal=0;
%当训练性能评价指标达到多少时停止训练
 net.trainParam.min_grad=0;
%当下降梯度达到多少时停止训练
 net.layers{1}.transferFcn='tansig';
 net.layers{2}.transferFcn='tansig';
 net.layers{3}.transferFcn='tansig';
 net.layers{4}.transferFcn='tansig';%最后一层
%这里我们初始化的时候网络结构选择了[12 12 12]，加上输入输出层为5层。也就是说有4个传递过程，即做多初始化到4.
net.divideParam.trainRatio=0.8;
net.divideParam.valRatio=0.1;
net.divideParam.testRatio=0.1;
%训练50%，验证20%，测试30%
%三选一，没有GPU的开GPU会报错
%[net,tr]=train(net,inputn,outputn);
%朴素模式
 %[net,tr]=train(net,inputn,outputn,'UseParallel','yes');
%开并行
 [net,tr]=train(net,delay',pointspos','UseParallel','yes','UseGPU','no');
%开并行+开GPU


view(net)
y = net(delay');
perf = perform(net,y,pointspos')