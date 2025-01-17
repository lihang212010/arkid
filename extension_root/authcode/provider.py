from PIL import Image, ImageDraw, ImageFont, ImageFilter
from common.provider import AuthCodeBaseProvider
from .constants import KEY
from io import BytesIO

import random
import string
import base64


class AuthCodeProvider(AuthCodeBaseProvider):
    def __init__(self, data) -> None:
        self.auth_code_length = data.get('auth_code_length', 4)

    def get_random_char(self):
        '''
        获取随机字符组合
        '''
        chr_all = string.ascii_letters + string.digits
        str_random = ''.join(random.sample(chr_all, self.auth_code_length))
        return str_random

    def get_random_color(self, low, high):
        '''
        获取随机颜色
        '''
        return (
            random.randint(low, high),
            random.randint(low, high),
            random.randint(low, high),
        )

    def get_authcode_picture(self):
        '''
        制作验证码图片
        '''
        width, height = 180, 60
        # 创建空白画布
        image = Image.new('RGB', (width, height), self.get_random_color(20, 100))
        # 验证码的字体
        font = ImageFont.truetype('./extension_root/authcode/assess/stxinwei.ttf', 40)
        # 创建画笔
        draw = ImageDraw.Draw(image)
        # 获取验证码
        char_4 = self.get_random_char()
        # 向画布上填写验证码
        for i in range(self.auth_code_length):
            draw.text(
                (40 * i + 10, 0),
                char_4[i],
                font=font,
                fill=self.get_random_color(100, 200),
            )
        # 绘制干扰点
        for x in range(random.randint(200, 600)):
            x = random.randint(1, width - 1)
            y = random.randint(1, height - 1)
            draw.point((x, y), fill=self.get_random_color(50, 150))
        # 模糊处理
        image = image.filter(ImageFilter.BLUR)
        key = self.generate_key()
        buf = BytesIO()
        # 将图片保存在内存中，文件类型为png
        image.save(buf, 'png')
        byte_data = buf.getvalue()
        base64_str = base64.b64encode(byte_data)
        return key, char_4, base64_str
