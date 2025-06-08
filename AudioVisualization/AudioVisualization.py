import numpy as np
import matplotlib.pyplot as plt
import librosa
import os
from colorsys import hls_to_rgb

def audio_visualization_hsl(file_path):
    # 加载音频文件
    y, sr = librosa.load(file_path)
    
    # 计算短时傅里叶变换(STFT)
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    
    # 创建频率和时间轴
    times = librosa.times_like(D)
    freqs = librosa.fft_frequencies(sr=sr)
    
    # 创建HSL颜色映射（亮度固定为50%）
    def hsl_colormap(value, vmin, vmax):
        # 将值归一化到0-1范围
        hue = (value - vmin) / (vmax - vmin)
        # 使用HSL色轮（0-240度，避免紫色到红色的过渡）
        lightness = 0.5  # 固定亮度50%
        saturation = 0.8
        return hls_to_rgb(hue * 2 / 3, lightness, saturation)
    
    # 将频谱图数据转换为RGB颜色
    vmin, vmax = S_db.min(), S_db.max()
    rgb_data = np.zeros((S_db.shape[0], S_db.shape[1], 3))
    
    for i in range(S_db.shape[0]):
        for j in range(S_db.shape[1]):
            rgb_data[i, j] = hsl_colormap(S_db[i, j], vmin, vmax)
        print(f"\r已完成{i * 100 // S_db.shape[0]}%", end="")
    
    # 创建图形
    dpi = 100
    plt.figure(figsize=(S_db.shape[1] / dpi, S_db.shape[0] / dpi))
    plt.imshow(rgb_data, aspect='auto', origin='lower', 
               extent=[times[0], times[-1], freqs[0], freqs[-1]])
    
    # 设置更细致的刻度和网格
    ax = plt.gca()
    
    # 设置x轴（时间轴）的刻度和标签
    duration = times[-1]
    major_ticks = np.arange(0, duration, 5)  # 每5秒一个主刻度
    minor_ticks = np.arange(0, duration, 1)  # 每1秒一个次刻度
    
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_xticklabels([f"{int(t)}s" for t in major_ticks])
    
    # 设置y轴（频率轴）的刻度和标签
    freq_major_ticks = np.linspace(freqs[0], freqs[-1], 10)
    ax.set_yticks(freq_major_ticks)
    ax.set_yticklabels([f"{int(f)} Hz" for f in freq_major_ticks])
    
    # 保存图像到相同路径
    base_path, ext = os.path.splitext(file_path)
    output_path = f"{base_path}_visualization.png"
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    
    print(f"\r可视化完成，图像已保存到: {output_path}")
    plt.show()
    plt.close()

# 用户输入文件路径
if __name__ == "__main__":
    file_path = input("请输入音频文件路径: ")
    if os.path.exists(file_path):
        audio_visualization_hsl(file_path)
    else:
        print("文件不存在，请检查路径是否正确。")