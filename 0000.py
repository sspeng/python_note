#! /usr/bin/python3

# PIL的文档说明 (http://pillow.readthedocs.io/en/latest/index.html)
from PIL import Image, ImageDraw, ImageFont
import sys

def add_num(img, str):

    # 获取头像作为底板
    base = Image.open(img).convert('RGBA')

    # 创建一个新的透明图像，大小和底板大小相同，RGBA模式描述颜色的是一个四元组，最后一个参数是不透明度
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

    # 获取一个字体，字体文件可以从当前工作目录或者从系统文件夹获取，第二个参数是大小
    fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', base.size[0] // 4)

    # 获取一个绘制环境，
    d = ImageDraw.Draw(txt)

    # text()方法在当前的绘制上下文中绘制文字
    d.text((base.size[1] - base.size[0] // 2, 0), str, font=fnt, fill=(255, 0, 0, 255))

    # d调用 Image.alpha_composite方法将第二个图像覆盖到第一个图像上
    out = Image.alpha_composite(base, txt)

    return out


if __name__ == '__main__':
    out = add_num(sys.argv[1], sys.argv[2])
    out.show()
