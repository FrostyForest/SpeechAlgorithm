import matplotlib.pyplot as plt
from sympy import *
import numpy as np
import math


class point:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
def distance(point1,point2):
    return (abs(point1.x-point2.x)**2+abs(point1.y-point2.y)**2+abs(point1.z-point2.z)**2)**0.5

class hyperbola:
    def __init__(self,p1,p2,t):

        self.x0=(p1.x+p2.x)/2
        self.y0 = (p1.y + p2.y) / 2
        self.d=abs(t)*340#到两点距离之差
        self.c=distance(p1,p2)/2#半焦距
        self.a=self.d/2
        self.b=(self.c**2-self.a**2)**0.5
        print(p2.y-p1.y)
        print(asin(0))
        self.degree=asin((p2.y-p1.y)/(2*self.c))
        print(self.degree)
        x, y = symbols('x y')
        self.eq=Eq(((x-self.x0)*math.cos(self.degree)+(y-self.y0)*math.sin(self.degree))**2/(self.a**2) - ((x-self.x0)*math.sin(self.degree)-(y-self.y0)*math.cos(self.degree))**2/(self.b**2), 1)






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
plt.colorbar()
plt.show()

real_delay=[-6.65884E-05,-9.64036E-05,-3.35969E-05,6.66443E-05,0.000104389,1.41833E-05,-2.53482E-05,5.89117E-05,0.000170189,0.000207088,9.07518E-05,6.57092E-05,0.000125084,1.30062E-05,0.000122429,9.51882E-05,0.000140484,7.11976E-05,2.76953E-05,-6.09528E-05,-9.36098E-05]

# 定义变量
x, y = symbols('x y')

f1=hyperbola(mic_list[0],mic_list[1],8.360084988489648e-05)
f2=hyperbola(mic_list[0],mic_list[4],-0.00011358194406223265)


# 定义双曲线方程
eq1 = f1.eq
eq2 = f2.eq
print(eq1)
print(eq2)

# 求解方程组
sol = nsolve((eq1,eq2), (x, y),(-2,-2))
print(sol)

