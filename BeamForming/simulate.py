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
    for j in range(mic_number+1):
        d=distance(point,mic_list[j])
        time=d/sound_speed
        point_to_each_mic_time.append(time)#到各麦时间
    point_to_mics_delay=[] #存储单个点到麦的延迟
    for x in range(mic_number+1):
        for y in range(x+1,mic_number+1):
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
mic_number=6#阵列圆形麦克风数量
r=0.04

#批量建立麦克风的坐标
mic0=point(0,0,0)
mic_list.append(mic0)
for i in range(0,mic_number):
    exec('mic{num} = point(r*np.sin({degree}*2*3.14159/mic_number),r*np.cos({degree}*2*3.14159/mic_number),0)'.format(num=i+1,degree=i))
    exec('mic_list.append(mic{0})'.format(i+1))
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

#各个通道之间的时延
real_delay=[-6.65884E-05,-9.64036E-05,-3.35969E-05,6.66443E-05,0.000104389,1.41833E-05,-2.53482E-05,5.89117E-05,0.000170189,0.000207088,9.07518E-05,6.57092E-05,0.000125084,1.30062E-05,0.000122429,9.51882E-05,0.000140484,7.11976E-05,2.76953E-05,-6.09528E-05,-9.36098E-05]
# real_delay=[8.453044280763364e-05, 0.00011381601605638374, 3.300423443374249e-05, -8.17549372929354e-05, -0.00011344383805183883, -2.783202731844285e-05, 2.9285573248750106e-05, -5.152620837389115e-05, -0.00016628538010056903, -0.00019797428085947246, -0.00011236247012607649, -8.081178162264125e-05, -0.00019557095334931914, -0.00022725985410822257, -0.0001416480433748266, -0.00011475917172667788, -0.00014644807248558132, -6.083626175218534e-05, -3.168890075890343e-05, 5.3922909974492544e-05, 8.561181073339598e-05]
# for i in range(len(real_delay)):
#     real_delay[i]=real_delay[i]*-1
p1=point(-0.6,-0.6,0)
print(cal_point_to_mics_delay(p1,mic_list))#虚拟时延

each_point_delay_difference=[]#各个点的到麦的时延差与实际时延差之和
for i in range(len(point_list)):
    differ_sum=0
    # for j in range(len(real_delay)):#计算欧氏距离
    #     differ=(each_point_timedelay_matrix[i][j]+real_delay[j])**2#假设时延与实际时延相减
    #     differ_sum=differ_sum+differ
    # each_point_delay_difference.append(differ_sum**0.5)

    # #马氏距离
    # each_point_delay_difference.append(Mahalanobis(each_point_timedelay_matrix[i],real_delay))

    #余弦距离
    each_point_delay_difference.append(Cosine(each_point_timedelay_matrix[i],real_delay))

    # #皮尔森相关系数
    # each_point_delay_difference.append(PearsonCorrelation(each_point_timedelay_matrix[i],real_delay))

x=heapq.nsmallest(3,each_point_delay_difference)
pos_x=[]
pos_y=[]
for i in range(3):
    print(point_list[each_point_delay_difference.index(x[i])].x,point_list[each_point_delay_difference.index(x[i])].y)
    pos_x.append(point_list[each_point_delay_difference.index(x[i])].x)
    pos_y.append(point_list[each_point_delay_difference.index(x[i])].y)

print(sum(pos_x)/len(pos_x))
print(sum(pos_y)/len(pos_y))
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

#print(each_point_timedelay_matrix[0])