
import numpy as np
import librosa
from tqdm import tqdm
import matplotlib.pyplot as plt
from collections import Counter
from scipy import signal
#
# def gcc_phat(sig, refsig, fs=48000, max_tau=0.001, interp=8):
#     """
#     计算两个信号之间的时间延迟
#     :param sig: 源信号
#     :param refsig: 参考信号
#     :param fs: 采样率
#     :param max_tau: 最大延迟时间
#     :param interp: 互相关函数的插值因子
#     :return: 估计的延迟时间
#     """
#
#     # 信号的长度必须是2的幂
#     n = sig.shape[0] + refsig.shape[0]
#     n_fft = 2 ** int(np.ceil(np.log2(n)))
#
#     # 计算双通道FFT
#     SIG = np.fft.rfft(sig, n=n_fft)
#     REFSIG = np.fft.rfft(refsig, n=n_fft)
#     R = SIG * np.conj(REFSIG)
#
#     # 计算互相关函数
#     cc = np.fft.irfft(R / np.abs(R), n=(interp * n_fft))
#     cc = np.concatenate((cc[-(sig.shape[0] - 1):], cc[:sig.shape[0]]))
#
#     # 寻找延迟
#     if max_tau:
#         max_shift = np.minimum(int(max_tau * fs), sig.shape[0])
#         cc = cc[:max_shift]
#     shift = np.argmax(np.abs(cc)) - cc.size // 2
#
#     # 计算时间延迟
#     tau = shift / float(interp * fs)
#     return tau

def gcc_phat(ref, sig, sr=48000):
    n_point = 2 * ref.shape[0] - 1
    X = np.fft.fft(ref, n_point)
    Y = np.fft.fft(sig, n_point)
    XY = X * np.conj(Y)

    c = XY / (abs(X) * abs(Y) + 10e-6)
    c = np.real(np.fft.ifft(c))
    end = len(c)
    center_point = end // 2

    # fft shift
    c = np.hstack((c[center_point + 1:], c[:center_point + 1]))
    lag = np.argmax(abs(c)) - len(ref) + 1
    tau = lag / sr
    return tau


SOUND_SPEED = 342.0
MIC_DISTANCE = 0.15
sample_rate = 48000
MAX_TDOA = MIC_DISTANCE / float(SOUND_SPEED)
time_list =[]
for j in range(0 ,7 ,1) :
    print(j)
    exec('org_sig, sr = librosa.load("./data/{0}.wav", sr=sample_rate)'.format(j))
    org_ref, sr = librosa.load("./data/0.wav", sr=sample_rate)
    ref = librosa.util.frame(org_ref, 1024*2, 256*2).T
    sig = librosa.util.frame(org_sig, 1024*2, 256*2).T
    fai = []
    time_delay =[]
    for i in tqdm(range(len(ref))):
        tau = gcc_phat(ref[i], sig[i])
        theta = np.arcsin(tau / MAX_TDOA) * 180 / np.pi
        # fai.append(theta)
        if (abs(tau)<0.001 ):
            time_delay.append(tau)

    plt.subplot(211)
    plt.ylabel('DOA ')
    plt.xlabel('Frame index')
    plt.title('DOA')
    plt.plot(time_delay)
    # plt.plot(fai)
    plt.subplot(212)
    plt.ylabel('Amplitude')
    plt.xlabel('Frame index')
    plt.title('Waveform')
    plt.plot(org_ref)
    plt.tight_layout()
    plt.show()


    time =Counter(time_delay)
    if len(time)==0 or len(time)==1:
        time_list.append(0)
    else:
        print(time.most_common())
        if time.most_common()[0][0]!=0:
            time_list.append(time.most_common()[0][0])
        else:
            time_list.append(time.most_common()[1][0])
print(time_list)