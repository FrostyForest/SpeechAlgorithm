import numpy as np
import matplotlib.pyplot as plt

# 定义麦克风数量
N = 8

# 定义目标信号的角度
target_angle = 30

# 定义每个麦克风的位置
microphone_angles = np.linspace(0, 360, N, endpoint=False)

# 定义频率
frequency = 1000

# 计算阵列增益
array_gain = np.zeros(N)
for i in range(N):
    array_gain[i] = np.exp(-1j * 2 * np.pi * frequency * np.cos(np.deg2rad(target_angle - microphone_angles[i])))

# 定义阵列信号
array_signal = np.zeros(N, dtype=np.complex128)

# 增益每个通道
for i in range(N):
    array_signal[i] = np.exp(1j * 2 * np.pi * frequency * np.cos(np.deg2rad(microphone_angles[i])))

# 应用波束成像算法
beamformed_signal = np.sum(array_signal * array_gain)

# 计算相位
phase = np.angle(beamformed_signal)

# 可视化阵列增益
plt.stem(microphone_angles, np.abs(array_gain))
plt.xlabel("Microphone Angle (degrees)")
plt.ylabel("Array Gain")
plt.show()

# 可视化相位
plt.stem(microphone_angles, phase)
plt.xlabel("Microphone Angle (degrees)")
plt.ylabel("Phase (radians)")
plt.show()
