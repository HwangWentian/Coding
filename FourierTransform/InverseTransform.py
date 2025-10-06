import numpy as np
import cv2
import os

def inverse_fourier_transform(fourier_path):
    # 检查文件是否存在
    if not os.path.exists(fourier_path):
        print(f"傅里叶变换结果文件不存在: {fourier_path}")
        return
    
    # 读取傅里叶变换结果
    fshift = np.load(fourier_path)
    
    # 执行逆傅里叶变换
    f_ishift = np.fft.ifftshift(fshift)  # 将零频率分量移回左上角
    img_back = np.fft.ifft2(f_ishift)    # 逆傅里叶变换
    img_back = np.abs(img_back)          # 取绝对值得到实部
    
    # 将像素值归一化到0-255范围
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    # 获取文件名和路径
    file_name = os.path.splitext(os.path.basename(fourier_path))[0].replace("_fourier", "")
    directory = os.path.dirname(fourier_path)
    if not directory:
        directory = os.getcwd()
    
    # 保存恢复的图像
    output_path = os.path.join(directory, f"{file_name}_recovered.png")
    cv2.imwrite(output_path, img_back)
    
    print(f"逆傅里叶变换完成，恢复的图像已保存至: {output_path}")

if __name__ == "__main__":
    # 获取用户输入的傅里叶变换结果路径
    fourier_path = input("请输入傅里叶变换结果(.npy)的路径: ").strip()
    inverse_fourier_transform(fourier_path)
    