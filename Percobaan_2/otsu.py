import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def total_pix(image):
    return image.size

def histogramify(image):
    grayscale_array = np.array(image)
    plt.hist(grayscale_array.ravel(), bins=256, color='blue', alpha=0.7)
    plt.title("Grayscale Histogram")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")
    plt.show()

def get_best_threshold(img_array):
    histogram, _ = np.histogram(img_array, bins=256, range=(0, 256))
    total_pixels = img_array.size

    sum_all = np.dot(np.arange(256), histogram)
    sum_b = 0
    weight_b = 0
    max_variance = 0
    best_threshold = 0
    
    for t in range(256):
        weight_b += histogram[t]
        if weight_b == 0:
            continue
        
        weight_f = total_pixels - weight_b
        if weight_f == 0:
            break
        
        sum_b += t * histogram[t]
        mean_b = sum_b / weight_b
        mean_f = (sum_all - sum_b) / weight_f
        
        between_variance = weight_b * weight_f * (mean_b - mean_f) ** 2
        
        if between_variance > max_variance:
            max_variance = between_variance
            best_threshold = t
    
    return best_threshold

def my_otsu(image, threshold):
    image = np.asarray(image)
    bin_image = image < threshold
    total = image.size
    
    w0 = np.sum(bin_image)
    w1 = total - w0
    
    if w0 == 0 or w1 == 0:
        return 0
    
    mean0 = np.sum(image * bin_image) / w0
    mean1 = (np.sum(image) - np.sum(image * bin_image)) / w1
    
    var_between = w0 / total * w1 / total * (mean0 - mean1) ** 2
    
    return var_between


#print(my_otsu(img_array, 116))


