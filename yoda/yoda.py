from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time
import os


def single_thresholding(image, threshold):
    image_gray = image.convert('L')
    image_bw = image_gray.point(lambda x: 255 if x > threshold else 0, mode='1')
    return image_bw


def double_thresholding(image, lower_threshold, upper_threshold):
    image_gray = image.convert('L')
    image_array = np.array(image_gray)
    image_bw = np.zeros_like(image_array)
    image_bw[(image_array > lower_threshold) & (image_array < upper_threshold)] = 255
    return Image.fromarray(image_bw)


def histogram_equalization(image):
    image_array = np.array(image)
    histogram, bin_edges = np.histogram(image_array, bins=256, range=(0, 255))
    cdf = histogram.cumsum()
    cdf_normalized = cdf * 255 / cdf[-1]
    image_equalized = np.interp(image_array.flatten(), bin_edges[:-1], cdf_normalized)
    return Image.fromarray(image_equalized.reshape(image_array.shape).astype(np.uint8))


def mean_filter_naive(image, filter_size):
    image_array = np.array(image)
    padded_image = np.pad(image_array, filter_size // 2, mode='constant')
    filtered_image = np.zeros_like(image_array)
    
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            filtered_image[i, j] = np.mean(padded_image[i:i+filter_size, j:j+filter_size])
    
    return Image.fromarray(filtered_image.astype(np.uint8))

def mean_filter_summed_area(image, filter_size):
    image_array = np.array(image)
    summed_area_table = np.cumsum(np.cumsum(image_array, axis=0, dtype=np.int64), axis=1, dtype=np.int64)
    padded_table = np.pad(summed_area_table, ((1, 0), (1, 0)), mode='constant')

    def get_sum(x1, y1, x2, y2):
        return (padded_table[x2, y2] 
                - padded_table[x1-1, y2] 
                - padded_table[x2, y1-1] 
                + padded_table[x1-1, y1-1])
    
    filtered_image = np.zeros_like(image_array)
    half_size = filter_size // 2

    for i in range(half_size, image_array.shape[0] - half_size):
        for j in range(half_size, image_array.shape[1] - half_size):
            x1, y1 = i - half_size + 1, j - half_size + 1
            x2, y2 = i + half_size, j + half_size
            total = get_sum(x1, y1, x2, y2)
            filtered_image[i, j] = total / (filter_size ** 2)

    return Image.fromarray(filtered_image.astype(np.uint8))


def save_and_display(image, title):
    temp_path = f"{title}.png"
    image.save(temp_path)
    img = Image.open(temp_path)
    img.show()
    os.remove(temp_path)



yoda_image_path = 'yoda.jpeg'
road_image_path = 'road.jpg'

yoda_image = Image.open(yoda_image_path)
yoda_bw_single = single_thresholding(yoda_image, 128)
yoda_bw_double = double_thresholding(yoda_image, 100, 200)

yoda_gray = yoda_image.convert('L')
yoda_hist_eq = histogram_equalization(yoda_gray)

road_image = Image.open(road_image_path).convert('L')
filter_size = 71


start_time = time.time()
road_filtered_summed_area = mean_filter_summed_area(road_image, filter_size)
summed_area_time = time.time() - start_time

save_and_display(yoda_image, "Original Yoda Image")
save_and_display(yoda_bw_single, "Single Thresholding")
save_and_display(yoda_bw_double, "Double Thresholding")
save_and_display(yoda_hist_eq, "Histogram Equalization")
save_and_display(road_filtered_summed_area, "Summed-Area Table Mean Filter")

print(f"Summed-area table approach time: {summed_area_time} seconds")
