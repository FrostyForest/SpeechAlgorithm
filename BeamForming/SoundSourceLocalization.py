

import numpy as np
import librosa
from tqdm import tqdm
import matplotlib.pyplot as plt
from collections import Counter


def gcc_phat(ref, sig, sr):
    n_point = 2 * ref.shape[0] - 1
    X = np.fft.fft(ref, n_point)
    Y = np.fft.fft(sig, n_point)
    XY = X * np.conj(Y)

    c = XY / (abs(X) * abs(Y) + 10e-6)
    c = np.real(np.fft.ifft(c))
    end = len(c)
    center_point = end // 2
	
	#fft shift
    c = np.hstack((c[center_point + 1:], c[:center_point + 1]))
    lag = np.argmax(abs(c)) - len(ref) + 1
    tau = lag / sr
    return tau


SOUND_SPEED = 342.0
MIC_DISTANCE = 0.15
sample_rate = 48000
MAX_TDOA = MIC_DISTANCE / float(SOUND_SPEED)
time_list=[]
for j in range(0,16,1) :
    exec('org_sig, sr = librosa.load("./data/{0}.wav", sr=sample_rate)'.format(j))
    org_ref, sr = librosa.load("./data/0.wav", sr=sample_rate)


    ref = librosa.util.frame(org_ref, 1024, 256).T
    sig = librosa.util.frame(org_sig, 1024, 256).T
    fai = []
    time_delay=[]
    for i in tqdm(range(len(ref))):
        tau = gcc_phat(ref[i], sig[i], sample_rate)
        theta = np.arcsin(tau / MAX_TDOA) * 180 / np.pi
        #fai.append(theta)
        if (abs(tau)<0.001):
            time_delay.append(tau)

    plt.subplot(211)
    plt.ylabel('DOA ')
    plt.xlabel('Frame index')
    plt.title('DOA')
    plt.plot(time_delay)
    #plt.plot(fai)
    plt.subplot(212)
    plt.ylabel('Amplitude')
    plt.xlabel('Frame index')
    plt.title('Waveform')
    plt.plot(org_ref)
    plt.tight_layout()
    plt.show()


    time=Counter(time_delay)
    time_list.append(time.most_common()[0][0])
print(time_list)