import os
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageColor

class ArcaeaStickerGenerator:
    def __init__(self, resource_dir: str):
        self.resource_dir = resource_dir
        self.default_colors = {
            "hikari": "#FFD700",
            "tairitsu": "#4A4AFF",
            "luna": "#C0C0C0",
            "eto": "#FF69B4",
            "nami": "#00CED1",
            "aichan": "#FFB6C1",
            "ayu": "#98FB98",
            "ilith": "#8A2BE2",
            "insight": "#DAA520",
            "kanae": "#FFA07A",
            "kou": "#DC143C",
            "lagrange": "#4682B4",
            "lethe": "#708090",
            "maya": "#FFD700",
            "nonoka": "#F0E68C",
            "saya": "#DB7093",
            "shirabe": "#9ACD32",
            "shirahime": "#F8F8FF",
            "vita": "#7B68EE",
        }

    def _parse_color(self, color_spec):
        try:
            return ImageColor.getrgb(color_spec)
        except ValueError:
            return (0, 0, 0)

    def _draw_text_on_image(self, image: Image.Image, text: str, center_x: int, center_y: int,
                            rotate: float, font_path: str, size: int, color):
        txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        try:
            font = ImageFont.truetype(font_path, size)
        except Exception as e:
            raise RuntimeError(f"加载字体失败: {font_path}") from e

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_img = Image.new("RGBA", (text_width, text_height), (255, 255, 255, 0))
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((-bbox[0], -bbox[1]), text, fill=color, font=font)

        rotated = text_img.rotate(rotate, expand=1, resample=Image.BICUBIC)

        paste_x = center_x - rotated.width // 2
        paste_y = center_y - rotated.height // 2

        txt_layer.paste(rotated, (paste_x, paste_y), rotated)
        image.paste(txt_layer, (0, 0), txt_layer)

    def generate_simple(self, character: str, text: str, font_path: str,
                        size=35, left_rotation=-45, right_rotation=45,
                        left_margin=20, top_margin=20, right_margin=20,
                        render_right=True):
        """
        简化模式：文字出现在左上角（和右上角，根据 render_right 决定）
        - 左上角坐标 (left_margin, top_margin)
        - 右上角坐标 (image.width - right_margin, top_margin)
        - render_right: 是否渲染右侧文字
        """
        char_img_path = os.path.join(self.resource_dir, f"{character}.png")
        if not os.path.exists(char_img_path):
            raise FileNotFoundError(f"角色图片不存在：{char_img_path}")
        img = Image.open(char_img_path).convert("RGBA")

        color = self.default_colors.get(character, "#000000")
        text_color = self._parse_color(color)

        # 左上角始终渲染
        self._draw_text_on_image(
            img, text,
            center_x=left_margin,
            center_y=top_margin,
            rotate=left_rotation,
            font_path=font_path,
            size=size,
            color=text_color
        )
        # 右上角根据参数决定
        if render_right:
            self._draw_text_on_image(
                img, text,
                center_x=img.width - right_margin,
                center_y=top_margin,
                rotate=right_rotation,
                font_path=font_path,
                size=size,
                color=text_color
            )

        tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img.save(tmp_file.name, "PNG")
        return tmp_file.name
