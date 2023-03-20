import os
import wave
import numpy as np
import struct
import sys

def pcm2wav(pcm_path, out_path, channel, sample_rate):
    # with open(pcm_path, 'rb') as pcm_file:
    #     pcm_data = pcm_file.read()
    #     pcm_file.close()
    # with wave.open(out_path, 'wb') as wav_file:
    #     ## 不解之处， 16 // 8， 第4个参数0为何有效
    #     wav_file.setparams((channel, 2, sample_rate, 0, 'NONE', 'NONE'))
    #     wav_file.writeframes(pcm_data)
    #     wav_file.close()
    if sys.byteorder == 'little':  # 检查系统字节顺序是否是小端
        with open(pcm_path, 'rb') as infile:
            outfile=(infile.read()[::-1])  # 直接反转输入文件的字节顺序并写入输出文件
            with wave.open(out_path, 'wb') as wav_file:
                ## 不解之处， 16 // 8， 第4个参数0为何有效
                wav_file.setparams((channel, 2, sample_rate, 0, 'NONE', 'NONE'))
                wav_file.writeframes(outfile)
                wav_file.close()

                # 打开wav文件
                f = wave.open(out_path, "rb")
                # 读取所有帧数据
                frames = f.readframes(f.getnframes())
                # 关闭文件
                f.close()
                # 将帧数据转换为字节数组
                data = bytearray(frames)
                # 反转字节数组（每两个字节为一个采样点）
                data.reverse()
                for i in range(0, len(data) - 1, 2):
                    data[i], data[i + 1] = data[i + 1], data[i]
                # 将字节数组转换为bytes对象
                frames = bytes(data)
                # 创建新的wav文件
                f = wave.open(out_path, "wb")
                # 设置参数和帧数据
                f.setparams((1, 2, sample_rate, 0, 'NONE', 'not compressed'))
                f.writeframes(frames)
                # 关闭文件
                f.close()
    else:  # 如果系统字节顺序是大端，就不需要转换了
        print('No conversion needed.')

if __name__ == '__main__':
    dir = r"C:\Users\林海\Desktop\audio\mica_channel_array_0_2等7个文件"
    out_dir = dir + r"\outwav"
    sample_rate = 48000
    channel = 1
    for i in range(7):
        exec('out_path = os.path.join(out_dir, "{0}.wav")'.format(i))
        exec('pcm2wav(os.path.join(dir, "mica_channel_array_0_{0}"), out_path, channel, sample_rate)'.format(i))