from PIL import Image
import sys

def get_image_data(image):
    data = [[0] * image.size[1] for _ in range(image.size[0])]

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            data[x][y] = image.getpixel((x, y))

    return image.size[0], image.size[1], data

def save_data(width, height, data, filename):
    img = Image.new('RGB', (width, height))
    img.putdata([data[x][y] for y in range(height) for x in
                 range(width)])
    img.save(filename)
    img.close()

def avg_color(color):
    return (color[0] + color[1] + color[2]) / 3.

def pixel_sort_vert(width, height, data, value):
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

if __name__ == '__main__':
    input_name = sys.argv[1]
    threshold = int(sys.argv[2])
    img = Image.open(input_name)
    input_name_split = input_name.split('.')
    output_name = ''.join(input_name_split[:-1]) + '_ps.' + input_name_split[-1]
    print('Getting data.')
    width, height, data = get_image_data(img)
    print('Data loaded.')
    print('Starting sorting.')
    pixel_sort_data = pixel_sort_vert(width, height, data, threshold)
    print('Sorting done.')
    print('Saving data.')
    save_data(width, height, pixel_sort_data, output_name)
    print('Data saved.')
