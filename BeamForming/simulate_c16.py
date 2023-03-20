import numpy as np
import matplotlib.pyplot as plt
import heapq
import csv
from scipy.spatial import distance
import math


class point:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
def distance(point1,point2):
    return (abs(point1.x-point2.x)**2+abs(point1.y-point2.y)**2+abs(point1.z-point2.z)**2)**0.5

def cal_point_to_mics_delay(point,mic_list):
    point_to_each_mic_time = []
    for j in range(mic_number):
        d=distance(point,mic_list[j])
        time=d/sound_speed
        point_to_each_mic_time.append(time)#到各麦时间
    point_to_mics_delay=[] #存储单个点到麦的延迟
    for x in range(mic_number):
        for y in range(x+1,mic_number):
            timedelay=(point_to_each_mic_time[y]-point_to_each_mic_time[x]) #点到各麦的时间差
            point_to_mics_delay.append(timedelay)
    return point_to_mics_delay

def Mahalanobis(vec1, vec2):
    npvec1, npvec2 = np.array(vec1), np.array(vec2)
    npvec = np.array([npvec1, npvec2])
    sub = npvec.T[0]-npvec.T[1]
    inv_sub = np.linalg.inv(np.cov(npvec1, npvec2))
    return math.sqrt(np.dot(inv_sub, sub).dot(sub.T))

def Cosine(vec1, vec2):
    npvec1, npvec2 = np.array(vec1), np.array(vec2)
    return npvec1.dot(npvec2)/(math.sqrt((npvec1**2).sum()) * math.sqrt((npvec2**2).sum()))


def PearsonCorrelation(x, y):
    x = np.array(x)
    y = np.array(y)
    x_ = x-np.mean(x)
    y_ = y-np.mean(y)
    return np.dot(x_,y_)/(np.linalg.norm(x_)*np.linalg.norm(y_))



height=0
sound_speed=340
mic_list=[]
mic_number=16#阵列圆形麦克风数量
r=0.08

#批量建立麦克风的坐标

for i in range(0,mic_number):
    exec('mic{num} = point(r*np.sin({degree}*2*3.14159/mic_number),r*np.cos({degree}*2*3.14159/mic_number),0)'.format(num=i,degree=i))
    exec('mic_list.append(mic{0})'.format(i))
x=[]
y=[]
for i in range(len(mic_list)):
    x.append(mic_list[i].x)
    y.append(mic_list[i].y)
print(x)
print(y)
plt.scatter(x,y,)
plt.show()


#虚拟点列表
point_list=[]
i=0
width=2

#批量建立虚拟平面上的点
for x in np.arange(-1*width,width+0.1,0.05):
    for y in np.arange(-1*width,width+0.1,0.05):
        exec('point{}=point({},{},height)'.format(i,x,y))
        exec('point_list.append(point{})'.format(i))
        i=i+1
print(len(point_list))

#各个虚拟点建立到各个麦克风的时延，以mic0为基准
each_point_timedelay_matrix=[]#每个点到各个mic与mic0的预期时延
i=0;j=0;
points_pos=[]#点的坐标
for i in range(len(point_list)):
    each_point_timedelay_matrix.append(cal_point_to_mics_delay(point_list[i],mic_list))
    # points_pos.append([point_list[i].x,point_list[i].y,0])

# #输出csv
# with open('delay.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(each_point_timedelay_matrix)
# with open('points_pos.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(points_pos)


#real_delay=[-6.71170240596264e-05,-0.000131599407346525,-7.31717778470949e-05,1.83420966767812e-05,6.54086552629220e-05,7.89331793860047e-05,5.08554959379241e-05,-0.000164814239430305,0.000195117434290600,0.000131637479746941,5.66973431481824e-05,5.66949322919489e-05,8.82084336443367e-05,0.000131302553338419,9.64736431286305e-06,-9.07544838382318e-05,1.56256875561048e-05,0.000104282518885844,0.000138566201571919,0.000157658916130262,0.000134249477977098,-5.94167011729205e-05,-0.000177739936100697,0.000202001478693110,0.000191384151291365,0.000190228529313031,0.000173645688762455,-0.000185233884316536,5.18573293368135e-05,7.40444491367119e-05,0.000127085988927750,0.000169757058085010,-2.39959275870134e-06,0.000165208694470703,-1.79701703946634e-06,-0.000104084810047910,-0.000179649880119515,-1.75167993255668e-05,4.23154404885942e-05,-0.000127682848650270,-0.000107410775394390,8.57073293336745e-05,5.43063388149070e-05,0.000117853903599958,0.000151622260467378,0.000135030707048168,-9.63384295205045e-05,-0.000205822139590542,0.000193105314792872,0.000165680902349564,0.000163194986320626,0.000176377699610396,0.000209293671116935,-5.15166178291237e-05,3.36302246410200e-05,6.04668381515024e-05,5.02312448916635e-05,-0.000205305300692050,0.000179917561854027,0.000118819468815135,5.41368959597065e-05,3.78357605246234e-05,9.50233256413823e-05,0.000172281965048924,-4.84947794161502e-05,1.03918359289421e-05,-7.22901330351141e-06,-0.000171510015733367,0.000140773914978678,6.41506394719176e-05,1.07717532816505e-05,-8.23306270097249e-06,2.92715311199323e-05,0.000113842752673734,-4.09231872636784e-05,-1.82778707108095e-05,-5.98693154303044e-05,0.000122128356381911,4.63612521146883e-05,-8.78610084987925e-07,-2.85192827744763e-05,2.58961509425437e-05,6.14708033422923e-05,-3.13974568588839e-06,-0.000199464653125439,0.000157026654340778,7.13841513811539e-05,1.38888844930671e-05,-1.17743848763653e-05,4.75626369288847e-05,0.000100328833060808,-7.99105169393313e-05,-5.04406523562418e-05,-0.000167243473248119,-0.000171384732580453,-0.000183363629048928,-0.000201386983172296,-0.000181682360664385,4.95445431066454e-05,-4.39376577670156e-05,-0.000112556511253280,-0.000132114119982486,-0.000112705649649475,-7.14328328544794e-05,-1.51097037051455e-05,-2.55353430274051e-05,-4.92319461976200e-05,-3.38292739242756e-05,3.18129252290260e-06,-7.74426872141927e-05,-1.09870162969429e-05,-6.09048809418731e-07,4.96200707920348e-05,-6.53894375641218e-05,1.60832115643269e-05,5.45638893394532e-05,-6.66036222273590e-05,2.89857494687790e-05,-8.58841827400334e-05,-7.54123078639784e-05]
real_delay=[4.984921050849023e-05, 6.728505072571729e-05, 4.9849326928355295e-05, 2.1637940918195486e-10, -7.515618132565571e-05, -0.0001646817027509146, -0.00025518088786459156, -0.0003326891240346911, -0.00038489184000228653, -0.0004033031845670186, -0.0003848924533361355, -0.0003326902500728028, -0.000255182345251799, -0.00016468326306214726, -7.515760752406508e-05, 1.7435840217227064e-05, 1.164198650677184e-10, -4.9848994129081045e-05, -0.00012500539183414594, -0.00021453091325940483, -0.0003050300983730818, -0.0003825383345431813, -0.00043474105051077676, -0.00045315239507550883, -0.00043474166384462574, -0.00038253946058129304, -0.00030503155576028923, -0.00021453247357063748, -0.0001250068180325553, -1.7435723797361996e-05, -6.728483434630811e-05, -0.000142441232051373, -0.0002319667534766319, -0.00032246593859030885, -0.0003999741747604084, -0.0004521768907280038, -0.0004705882352927359, -0.0004521775040618528, -0.0003999753007985201, -0.0003224673959775163, -0.00023196831378786455, -0.00014244265824978238, -4.984911054894611e-05, -0.000125005508254011, -0.0002145310296792699, -0.00030503021479294685, -0.0003825384509630464, -0.0004347411669306418, -0.0004531525114953739, -0.0004347417802644908, -0.0003825395770011581, -0.0003050316721801543, -0.00021453258999050255, -0.00012500693445242038, -7.51563977050649e-05, -0.0001646819191303238, -0.00025518110424400074, -0.0003326893404141003, -0.0003848920563816957, -0.0004033034009464278, -0.0003848926697155447, -0.000332690466452212, -0.0002551825616312082, -0.00016468347944155644, -7.515782390347427e-05, -8.95255214252589e-05, -0.00018002470653893585, -0.0002575329427090354, -0.0003097356586766308, -0.0003281470032413629, -0.0003097362720104798, -0.0002575340687471471, -0.0001800261639261433, -8.952708173649154e-05, -1.4261984093710822e-09, -9.049918511367695e-05, -0.0001680074212837765, -0.00022021013725137192, -0.000238621481816104, -0.0002202107505852209, -0.0001680085473218882, -9.05006425008844e-05, -1.560311232648437e-09, 8.952409522684952e-05, -7.750823617009954e-05, -0.00012971095213769497, -0.00014812229670242705, -0.00012971156547154396, -7.750936220821125e-05, -1.4573872074430394e-09, 9.04976248024443e-05, 0.00018002328034052648, -5.220271596759543e-05, -7.061406053232751e-05, -5.220332930144442e-05, -1.126038111712302e-09, 7.75067787828921e-05, 0.00016800586097254384, 0.000257531516510626, -1.8411344564732077e-05, -6.133338489866524e-10, 5.220158992948372e-05, 0.00012970949475048753, 0.00022020857694013928, 0.00030973423247822145, 1.841073123088309e-05, 7.06129344942158e-05, 0.0001481208393152196, 0.00023861992150487135, 0.0003281455770429535, 5.2202203263332705e-05, 0.00012971010808433651, 0.00022020919027398826, 0.00030973484581207043, 7.750790482100381e-05, 0.00016800698701065556, 0.00025753264254873773, 9.049908218965175e-05, 0.00018002473772773392, 8.952565553808217e-05]
p1=point(-0.6,-0.6,0)
for i in range(len(real_delay)):
    real_delay[i]=real_delay[i]*-1
print(cal_point_to_mics_delay(p1,mic_list))

each_point_delay_difference=[]#各个点的到麦的时延差与实际时延差之和
for i in range(len(point_list)):
    differ_sum=0
    # for j in range(len(real_delay)):#计算欧氏距离
    #     differ=(each_point_timedelay_matrix[i][j]+real_delay[j])**2#假设时延与实际时延相减
    #     differ_sum=differ_sum+differ
    # each_point_delay_difference.append(differ_sum**0.5)

    # #马氏距离
    # each_point_delay_difference.append(Mahalanobis(each_point_timedelay_matrix[i],real_delay))

    # #余弦距离
    # each_point_delay_difference.append(Cosine(each_point_timedelay_matrix[i],real_delay))

    #皮尔森相关系数
    each_point_delay_difference.append(PearsonCorrelation(each_point_timedelay_matrix[i],real_delay))

x=heapq.nsmallest(10,each_point_delay_difference)
for i in range(10):
    print(point_list[each_point_delay_difference.index(x[i])].x,point_list[each_point_delay_difference.index(x[i])].y)


# x=[]
# y=[]
# for i in range(len(mic_list)):
#     x.append(mic_list[i].x)
#     y.append(mic_list[i].y)
#
# #画各个麦克风的时延分布
# plt.scatter(x,y,)
# plt.colorbar()
# plt.show()

n_x=int(len(point_list)**0.5)
data = np.random.random((n_x, n_x))

max_range=heapq.nlargest(1,each_point_delay_difference)[0]-heapq.nsmallest(1,each_point_delay_difference)[0]
for x in range(n_x):
    for y in range(n_x):
        if((heapq.nlargest(1,each_point_delay_difference)[0]-each_point_delay_difference[x*n_x+n_x-y-1])/max_range>0.99):
            data[y][x]=(heapq.nlargest(1,each_point_delay_difference)[0]-each_point_delay_difference[x*n_x+n_x-y-1])/max_range
            # data[y][x] =each_point_delay_difference[x*n_x+n_x-1-y]
        else:
            data[y][x]=(heapq.nlargest(1,each_point_delay_difference)[0]-each_point_delay_difference[x*n_x+n_x-y-1])/max_range



plt.imshow(data, cmap='jet', interpolation='nearest',extent=(-width,width,-width,width))
plt.colorbar()
x_point = -0.6 # 目标点
y_point = -0.6 #
plt.scatter(x_point, y_point, marker='o', color='aquamarine')
plt.show()
print(each_point_timedelay_matrix[0])