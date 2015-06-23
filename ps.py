from PIL import Image
import sys
import os
import random

def get_image_data(image):
    """This function load the image into a 2 dimensional array of pixels.

    """
    data = [[0] * image.size[1] for _ in range(image.size[0])]

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            data[x][y] = image.getpixel((x, y))

    return image.size[0], image.size[1], data

def save_data(width, height, data, filename):
    """This function save a 2 dimensional array of pixels into a file.

    """
    img = Image.new('RGB', (width, height))
    img.putdata([data[x][y] for y in range(height) for x in
                 range(width)])
    img.save(filename)
    img.close()

def avg_color(color):
    return (color[0] + color[1] + color[2]) / 3.

def pixel_sort_vert(width, height, data, value):
    """Pixel sort vertically from top to bottom. The column is sorted
    from the first pixel above the threshold.

    """
    pixel_sort_data = [[0] * height for _ in range(width)]

    for x in range(width):
        y = 0
        while y < height and avg_color(data[x][y]) < value:
            pixel_sort_data[x][y] = data[x][y]
            y += 1
        pixels = [data[x][i] for i in range(y, height)]
        pixels.sort(key = lambda x: avg_color(x), reverse=True)
        for i in range(len(pixels)):
            pixel_sort_data[x][y + i] = pixels[i]

    return pixel_sort_data

def pixel_sort_vert_contiguous(width, height, data, value):
    """Pixel sort vertically from top to bottom. Only contiguous regions
    which pixels are above the threshold are sorted.

    """
    pixel_sort_data = [[0] * height for _ in range(width)]

    for x in range(width):
        y = 0
        while y < height:
            if avg_color(data[x][y]) < value:
                pixel_sort_data[x][y] = data[x][y]
                y += 1
            else:
                y_max = y
                while y_max < height and avg_color(data[x][y_max]) >= value:
                    y_max += 1
                pixels = [data[x][i] for i in range(y, y_max)]
                pixels.sort(key = lambda x: avg_color(x), reverse=True)
                for i in range(len(pixels)):
                    pixel_sort_data[x][y + i] = pixels[i]
                y = y_max

    return pixel_sort_data

def pixel_shuffle_vert_contiguous(width, height, data, value):
    """Pixel sort vertically from top to bottom. Only contiguous regions
    which pixels are above the threshold are sorted.

    """
    pixel_sort_data = [[0] * height for _ in range(width)]

    for x in range(width):
        y = 0
        while y < height:
            if avg_color(data[x][y]) < value:
                pixel_sort_data[x][y] = data[x][y]
                y += 1
            else:
                y_max = y
                while y_max < height and avg_color(data[x][y_max]) >= value:
                    y_max += 1
                pixels = [data[x][i] for i in range(y, y_max)]
                pixels = random.sample(pixels, len(pixels))
#                pixels.sort(key = lambda x: avg_color(x), reverse=True)
                for i in range(len(pixels)):
                    pixel_sort_data[x][y + i] = pixels[i]
                y = y_max

    return pixel_sort_data


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("USAGE: python ps.py input_file threshold")
        sys.exit(0)
    input_name = sys.argv[1]
    threshold = int(sys.argv[2])
    img = Image.open(input_name)
    input_name_split = input_name.split('.')
    output_name = ''.join(input_name_split[:-1]) + '_ps.' + input_name_split[-1]
    print('Getting data.')
    width, height, data = get_image_data(img)
    print('Data loaded.')
    print('Starting sorting.')
#    pixel_sort_data = pixel_sort_vert_contiguous(width, height, data, threshold)
    pixel_sort_data = pixel_shuffle_vert_contiguous(width, height, data, threshold)
    print('Sorting done.')
    print('Saving data.')
    save_data(width, height, pixel_sort_data, output_name)
    print('Data saved.')
