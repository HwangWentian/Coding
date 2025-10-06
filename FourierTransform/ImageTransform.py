import numpy as np
import cv2
import os

def image_fourier_transform(image_path):
    # 读取图像，以灰度模式打开（确保后续处理为单通道）
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"无法读取图像: {image_path}")
        return
    
    # 1. 执行傅里叶变换（核心计算，保留复数结果用于逆变换）
    f = np.fft.fft2(img)  # 二维傅里叶变换（结果为复数数组）
    fshift = np.fft.fftshift(f)  # 将零频率分量（低频）移到频谱中心
    
    # 2. 保存完整傅里叶变换结果（复数数组，确保逆变换完全恢复）
    file_name = os.path.splitext(os.path.basename(image_path))[0]
    directory = os.path.dirname(image_path) or os.getcwd()  # 处理当前目录路径
    fourier_output_path = os.path.join(directory, f"{file_name}_fourier.npy")
    np.save(fourier_output_path, fshift)
    
    # 3. 生成并优化频谱图（解决偏亮问题）
    # 步骤1：计算幅度谱（复数的模，反映频率分量的强度）
    magnitude_spectrum = np.abs(fshift)
    # 步骤2：对数变换（压缩高频分量的亮度范围，突出细节）
    # 加1是为了避免log(0)报错（幅度谱最小值为0）
    magnitude_spectrum_log = 20 * np.log1p(magnitude_spectrum)
    # 步骤3：归一化到0-255（核心修复！解决偏亮问题）
    # 将对数变换后的数值映射到0-255，确保亮度正常
    magnitude_spectrum_norm = cv2.normalize(
        magnitude_spectrum_log, 
        None, 
        alpha=0, 
        beta=255, 
        norm_type=cv2.NORM_MINMAX,  # 按最小值-最大值归一化
        dtype=cv2.CV_8U  # 转换为8位无符号整数（图像标准格式）
    )
    
    # 保存优化后的频谱图
    spectrum_output_path = os.path.join(directory, f"{file_name}_spectrum.png")
    cv2.imwrite(spectrum_output_path, magnitude_spectrum_norm)
    
    print(f"傅里叶变换完成！")
    print(f"- 复数结果（用于逆变换）: {fourier_output_path}")
    print(f"- 频谱图: {spectrum_output_path}")

if __name__ == "__main__":
    image_path = input("请输入图像路径: ").strip()
    image_fourier_transform(image_path)