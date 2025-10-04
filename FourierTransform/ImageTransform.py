import cv2
import numpy as np
from pathlib import Path

def image_to_fft(image_path):
    """
    Convert an image to grayscale, perform FFT with low frequencies at center,
    and save the result in the same directory.
    
    Args:
        image_path (str): Path to the input image file
    """
    # Read the image in grayscale mode
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"Error: Could not load image from {image_path}")
        return
    
    # Perform 2D Fast Fourier Transform
    fft = np.fft.fft2(img)
    
    # Shift zero frequency component to center
    fft_shifted = np.fft.fftshift(fft)
    
    # Calculate magnitude spectrum (log scale for better visualization)
    magnitude_spectrum = np.log(1 + np.abs(fft_shifted))
    
    # Normalize to 0-255 range for image saving
    magnitude_spectrum_normalized = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX)
    magnitude_spectrum_uint8 = np.uint8(magnitude_spectrum_normalized)
    
    # Generate output file path
    input_path = Path(image_path)
    output_filename = f"{input_path.stem}_fft{input_path.suffix}"
    output_path = input_path.parent / output_filename
    
    # Save the FFT magnitude spectrum
    cv2.imwrite(str(output_path), magnitude_spectrum_uint8)
    print(f"FFT image saved to: {output_path}")

# Example usage
if __name__ == "__main__":
    # Replace with your image path
    image_path = input()
    image_to_fft(image_path)