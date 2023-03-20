import wave
import os
def pcm2wav(pcm_path, out_path, channel, sample_rate,sample_width):
    with open(pcm_path, 'rb') as f:
        pcm_data = f.read()

    # 打开WAV文件
    with wave.open(out_path, 'wb') as f:
        f.setnchannels(channel)
        f.setsampwidth(sample_width)
        f.setframerate(sample_rate)
        f.writeframes(pcm_data)


# 设置参数
mic_number=16#阵列通道数量
for i in range(16):
    dir = r"C:\Users\林海\Desktop\audio\mica_channel_array_0_2等7个文件"
    out_dir = dir + r"\outwav"
    channel = 1
    num_channels = 1  # 单声道
    sample_width = 2  # 采样位宽，2字节
    sample_rate = 48000  # 采样率，48kHz
    num_frames = None  # 文件长度，None表示全部读入
    exec('out_path = os.path.join(out_dir, "{0}.wav")'.format(i))
    exec('pcm2wav(os.path.join(dir, "mica_channel_array_0_{0}"), out_path, channel, sample_rate,sample_width)'.format(i))


