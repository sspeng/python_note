# /usr/bin/python3
# coding=utf8

from PIL import Image
import argparse


# 命令行参数处理
parser = argparse.ArgumentParser()

parser.add_argument('file')
parser.add_argument('-o', '--output')
parser.add_argument('--width', type=int, default=80)
parser.add_argument('--height', type=int, default=80)


args = parser.parse_args()

IMG = args.file
OUTPUT = args.output
WIDTH = args.width
HEIGHT = args.height

# 灰度值公式
# gray = 0.2126 * r + 0.7152 * g + 0.0722 * b

# 绘制字符画所用的字符集,可以看出其饱满程度随索引递减
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


# RGB值 映射 到70个qqqq字符集的函数
def get_char(r, g, b, alpha=256):
    """
    :param r: 像素点的R值
    :param g: 像素点的G值
    :param b: 像素点的B值
    :param alpha: 像素点的 alpha 值，默认为 256
    :return: 返回像素点所对应的字符
    """
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1.0) / length
    return ascii_char[int(gray / unit)]

if __name__ == '__main__':
    img = Image.open(IMG)
    img = img.resize((WIDTH, HEIGHT), Image.NEAREST)
    img.show()
    text = ''

    for x in range(HEIGHT):
        for y in range(WIDTH):
            # Image.getpixel()方法提供一个元组，调用时 参数 + *  号表示元组拆包， + ** 号表示字典拆包
            text += get_char(*img.getpixel((y, x)))
        text += '\n'
    print(text)

    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(text)
    else:
        with open('output.txt', 'w') as f:
            f.write(text)

