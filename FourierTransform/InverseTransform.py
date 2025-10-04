import cv2
import numpy as np
from pathlib import Path

def fft_to_image(fft_image_path):
    """
    Perform inverse FFT on a frequency domain image to reconstruct the spatial image.
    
    Args:
        fft_image_path (str): Path to the FFT magnitude spectrum image
    """
    # Read the FFT magnitude spectrum image
    fft_magnitude = cv2.imread(fft_image_path, cv2.IMREAD_GRAYSCALE)
    
    if fft_magnitude is None:
        print(f"Error: Could not load FFT image from {fft_image_path}")
        return
    
    # Denormalize - reverse the normalization process
    # Since we used log(1 + abs(fft)) and normalized to 0-255, we need to reverse this
    fft_magnitude_float = fft_magnitude.astype(np.float64)
    
    # Reverse normalization (approximate)
    # Note: This is an approximation since we lost phase information and exact scaling
    magnitude_spectrum = np.exp(fft_magnitude_float * np.log(256) / 255) - 1
    
    # Create a random phase (since phase information was lost in the magnitude spectrum)
    # In practice, for perfect reconstruction you would need both magnitude and phase
    random_phase = np.random.uniform(0, 2*np.pi, magnitude_spectrum.shape)
    
    # Reconstruct complex FFT from magnitude and random phase
    fft_complex = magnitude_spectrum * np.exp(1j * random_phase)
    
    # Shift frequencies back to original position
    fft_ishifted = np.fft.ifftshift(fft_complex)
    
    # Perform inverse FFT
    img_reconstructed = np.fft.ifft2(fft_ishifted)
    
    # Take real part (imaginary part should be very close to zero)
    img_reconstructed = np.real(img_reconstructed)
    
    # Normalize to 0-255 range
    img_reconstructed = cv2.normalize(img_reconstructed, None, 0, 255, cv2.NORM_MINMAX)
    img_reconstructed_uint8 = np.uint8(img_reconstructed)
    
    # Generate output file path
    input_path = Path(fft_image_path)
    output_filename = f"{input_path.stem}_reconstructed{input_path.suffix}"
    output_path = input_path.parent / output_filename
    
    # Save the reconstructed image
    cv2.imwrite(str(output_path), img_reconstructed_uint8)
    print(f"Reconstructed image saved to: {output_path}")
    
    return img_reconstructed_uint8

def fft_to_image_with_phase(fft_magnitude_path, fft_phase_path=None):
    """
    Perform inverse FFT with optional phase information for better reconstruction.
    
    Args:
        fft_magnitude_path (str): Path to the FFT magnitude spectrum image
        fft_phase_path (str, optional): Path to the FFT phase image
    """
    # Read magnitude spectrum
    magnitude_img = cv2.imread(fft_magnitude_path, cv2.IMREAD_GRAYSCALE)
    
    if magnitude_img is None:
        print(f"Error: Could not load magnitude image from {fft_magnitude_path}")
        return
    
    # Denormalize magnitude
    magnitude_float = magnitude_img.astype(np.float64)
    magnitude_spectrum = np.exp(magnitude_float * np.log(256) / 255) - 1
    
    if fft_phase_path:
        # If phase image is provided, use it for reconstruction
        phase_img = cv2.imread(fft_phase_path, cv2.IMREAD_GRAYSCALE)
        if phase_img is not None:
            # Denormalize phase from 0-255 to 0-2pi
            phase = phase_img.astype(np.float64) * (2 * np.pi / 255)
        else:
            print("Warning: Could not load phase image, using random phase")
            phase = np.random.uniform(0, 2*np.pi, magnitude_spectrum.shape)
    else:
        # Use random phase if no phase image provided
        phase = np.random.uniform(0, 2*np.pi, magnitude_spectrum.shape)
    
    # Reconstruct complex FFT
    fft_complex = magnitude_spectrum * np.exp(1j * phase)
    
    # Shift back and perform inverse FFT
    fft_ishifted = np.fft.ifftshift(fft_complex)
    img_reconstructed = np.real(np.fft.ifft2(fft_ishifted))
    
    # Normalize and convert to uint8
    img_reconstructed = cv2.normalize(img_reconstructed, None, 0, 255, cv2.NORM_MINMAX)
    img_reconstructed_uint8 = np.uint8(img_reconstructed)
    
    # Save reconstructed image
    input_path = Path(fft_magnitude_path)
    output_filename = f"{input_path.stem}_reconstructed{input_path.suffix}"
    output_path = input_path.parent / output_filename
    
    cv2.imwrite(str(output_path), img_reconstructed_uint8)
    print(f"Reconstructed image saved to: {output_path}")
    
    return img_reconstructed_uint8

def save_fft_components(image_path):
    """
    Save both magnitude and phase components of FFT for perfect reconstruction.
    
    Args:
        image_path (str): Path to the input image file
    """
    # Read image and perform FFT
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"Error: Could not load image from {image_path}")
        return
    
    # FFT processing
    fft = np.fft.fft2(img)
    fft_shifted = np.fft.fftshift(fft)
    
    # Calculate magnitude and phase
    magnitude = np.log(1 + np.abs(fft_shifted))
    phase = np.angle(fft_shifted)
    
    # Normalize magnitude to 0-255
    magnitude_normalized = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    magnitude_uint8 = np.uint8(magnitude_normalized)
    
    # Normalize phase from -pi to pi range to 0-255
    phase_normalized = cv2.normalize(phase, None, 0, 255, cv2.NORM_MINMAX)
    phase_uint8 = np.uint8(phase_normalized)
    
    # Save both components
    input_path = Path(image_path)
    
    magnitude_path = input_path.parent / f"{input_path.stem}_fft_magnitude{input_path.suffix}"
    phase_path = input_path.parent / f"{input_path.stem}_fft_phase{input_path.suffix}"
    
    cv2.imwrite(str(magnitude_path), magnitude_uint8)
    cv2.imwrite(str(phase_path), phase_uint8)
    
    print(f"Magnitude spectrum saved to: {magnitude_path}")
    print(f"Phase spectrum saved to: {phase_path}")
    
    return str(magnitude_path), str(phase_path)

# Example usage
if __name__ == "__main__":
    # For basic reconstruction from magnitude only
    fft_image_path = input()
    fft_to_image(fft_image_path)