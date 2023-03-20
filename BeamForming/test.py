# 导入必要的库
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

# 定义麦克风阵列坐标和声源方向参数
yi = np.array([0.04, 0.02000003064100781, -0.019999938717937437, -0.03999999999985917, -0.020000122563937347,
               0.019999846794726262])
xi = np.array([0.0, 0.03464099846076537, 0.03464105153252059, 1.0614359175187277e-07, -0.03464094538876623,
               -0.034641104604031865])
M = len(xi) # 阵元个数
c = 340 # 声速
f = 1000 # 信号频率
w = 2 * np.pi * f # 角频率
d = np.sqrt(xi**2 + yi**2) # 阵元到原点的距离
theta_s = np.deg2rad(30) # 声源方向角度（弧度）
k = w / c # 波数
a_s = np.exp(-1j * k * d * np.sin(theta_s)) # 声源方向矢量

# 生成阵列信号矩阵
N = 100 # 采样点数
snr = 10 # 信噪比（dB）
s = np.exp(1j * w * np.arange(N) / N) # 单频信号
n = np.random.randn(M, N) + 1j * np.random.randn(M, N) # 复高斯白噪声
n = n / la.norm(n, axis=1, keepdims=True) * la.norm(s) / (10 ** (snr / 20)) #

# 阵列信号矩阵
X = a_s[:, np.newaxis] * s[np.newaxis, :] + n

# 计算协方差矩阵并进行SVD
R = X @ X.conj().T / N # 协方差矩阵
U, S, V = la.svd(R) # SVD
Us = U[:, :1] # 信号子空间
Un = U[:, 1:] # 噪声子空间

# 定义谱峰函数
def P_music(theta):
    a = np.exp(-1j * k * d * np.sin(theta)) # 方向矢量
    return 1 / la.norm(Un.conj().T @ a)**2 # 谱峰函数

# 在给定的角度范围内进行搜索，找到最大值对应的角度
theta_range = np.linspace(-np.pi/2, np.pi/2, 1000) # 角度范围（弧度）
P_range = np.array([P_music(theta) for theta in theta_range]) # 谱峰函数值
theta_est = theta_range[np.argmax(P_range)] # 估计的角度（弧度）

# 绘制谱峰函数和定位结果
plt.figure()
plt.plot(np.rad2deg(theta_range), P_range)
plt.xlabel('Angle (degree)')
plt.ylabel('Spectrum')
plt.title('MUSIC Spectrum')
plt.grid()
plt.show()

plt.figure()
plt.scatter(xi, yi, c='b', marker='o', label='Microphones')
plt.scatter(d * np.sin(theta_s), 0, c='r', marker='x', label='True Source')
plt.scatter(d * np.sin(theta_est), 0, c='g', marker='+', label='Estimated Source')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Source Localization')
plt.legend()
plt.grid()
plt.show()