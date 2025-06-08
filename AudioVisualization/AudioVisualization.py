import numpy as np
import matplotlib.pyplot as plt
import librosa
import os
from colorsys import hls_to_rgb

def hsl_colormap_vectorized(S_db, vmin, vmax):
    hue = np.clip((S_db - vmin) / (vmax - vmin) * 2 / 3, 0, 2 / 3)  # 避免数值溢出
    
    lightness = np.full_like(hue, 0.5)
    saturation = np.full_like(hue, 0.8)
    
    # 预分配RGB数组
    rgb_data = np.zeros((*hue.shape, 3))
    
    # 向量化计算RGB（逐通道处理）
    for channel in range(3):  # R, G, B 三个通道
        # 使用np.vectorize包装hls_to_rgb的对应通道
        rgb_data[..., channel] = np.vectorize(
            lambda h, l, s: hls_to_rgb(h, l, s)[channel],
            otypes=[float]
        )(hue, lightness, saturation)
    
    return rgb_data

def audio_visualization_hsl(file_path):
    # 加载音频文件
    y, sr = librosa.load(file_path)
    
    # 计算短时傅里叶变换(STFT)
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    
    # 向量化颜色映射
    rgb_data = hsl_colormap_vectorized(S_db, S_db.min(), S_db.max())
    
    # 创建频率和时间轴
    times = librosa.times_like(D)
    freqs = librosa.fft_frequencies(sr=sr)    
    # 创建图形
    dpi = 100
    plt.figure(figsize=(S_db.shape[1] / dpi, S_db.shape[0] / dpi))
    plt.imshow(rgb_data, aspect='auto', origin='lower', 
               extent=[times[0], times[-1], freqs[0], freqs[-1]])
    
    # 设置坐标轴
    ax = plt.gca()
    duration = times[-1]
    
    # 时间轴刻度（主刻度5秒，次刻度1秒）
    major_ticks = np.arange(0, duration, 5)
    minor_ticks = np.arange(0, duration, 1)
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_xticklabels([f"{int(t)}s" for t in major_ticks])
    
    # 频率轴刻度（均匀10段）
    freq_major_ticks = np.linspace(freqs[0], freqs[-1], 10)
    ax.set_yticks(freq_major_ticks)
    ax.set_yticklabels([f"{int(f)} Hz" for f in freq_major_ticks])
    
    # 保存图像
    base_path, ext = os.path.splitext(file_path)
    output_path = f"{base_path}_visualization.png"
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"可视化完成，图像已保存到: {output_path}")
    plt.show()
    plt.close()

if __name__ == "__main__":
    file_path = input("请输入音频文件路径: ")
    if os.path.exists(file_path):
        audio_visualization_hsl(file_path)
    else:
        print("文件不存在，请检查路径是否正确。")