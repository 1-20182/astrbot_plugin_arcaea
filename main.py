import os
import random

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Image, Plain

from .utils.generator import ArcaeaStickerGenerator

@register("astrbot_plugin_arcaea_sticker", "YourName", "Arcaea 表情包生成器（优化版）", "4.2.0")
class ArcaeaStickerPlugin(Star):
    # 中文别名映射表（完整）
    CHARACTER_ALIASES = {
        "AI酱": "aichan",
        "彩梦": "ayu",
        "爱托": "eto",
        "光": "hikari",
        "伊莉丝": "ilith",
        "洞烛": "insight",
        "拉可弥拉": "insight",
        "群愿": "kanae",
        "红": "kou",
        "拉格兰": "lagrange",
        "忘却": "lethe",
        "露娜": "luna",
        "摩耶": "maya",
        "奈美": "nami",
        "野乃香": "nonoka",
        "咲弥": "saya",
        "调": "shirabe",
        "白姬": "shirahime",
        "对立": "tairitsu",
        "维塔": "vita",
    }

    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        self.resource_dir = os.path.join(os.path.dirname(__file__), "resources")
        os.makedirs(self.resource_dir, exist_ok=True)

        config = config or {}

        # 安全读取配置，处理可能的类型错误
        def safe_int(key, default):
            try:
                return int(config.get(key, default))
            except (ValueError, TypeError):
                return default

        def safe_float(key, default):
            try:
                return float(config.get(key, default))
            except (ValueError, TypeError):
                return default

        custom_font = config.get("custom_font_path", "")
        self.simple_font_size = safe_int("simple_font_size", 35)
        self.simple_left_rotation = safe_float("simple_left_rotation", -45)
        self.simple_right_rotation = safe_float("simple_right_rotation", 45)
        self.simple_left_margin = safe_int("simple_left_margin", 20)
        self.simple_top_margin = safe_int("simple_top_margin", 20)
        self.simple_right_margin = safe_int("simple_right_margin", self.simple_left_margin)

        # 触发关键词（用于随机表情包）
        keywords_str = config.get("trigger_keywords", "arc表情包")
        self.trigger_keywords = [kw.strip() for kw in keywords_str.split(",") if kw.strip()]

        self.generator = ArcaeaStickerGenerator(self.resource_dir)
        self.available_characters = self._scan_characters()
        for eng in self.available_characters:
            self.CHARACTER_ALIASES[eng] = eng

        # 字体文件夹
        self.fonts_dir = os.path.join(os.path.dirname(__file__), "fonts")
        self.simple_font_path = None
        if os.path.exists(self.fonts_dir):
            ttf_files = [f for f in os.listdir(self.fonts_dir) if f.lower().endswith('.ttf')]
            if ttf_files:
                self.simple_font_path = os.path.join(self.fonts_dir, ttf_files[0])
                logger.info(f"简化模式字体：{self.simple_font_path}")
            else:
                logger.warning("fonts 文件夹中未找到 TTF 字体文件，简化模式将不可用")
        else:
            logger.warning("fonts 文件夹不存在，简化模式将不可用")

        # emoji 文件夹
        self.emoji_dir = os.path.join(os.path.dirname(__file__), "emoji")
        os.makedirs(self.emoji_dir, exist_ok=True)

        # 角色预览图文件夹
        self.list_dir = os.path.join(os.path.dirname(__file__), "list")
        os.makedirs(self.list_dir, exist_ok=True)

        logger.info(f"Arcaea Sticker 插件 v4.2.0 加载，可用角色：{', '.join(self.available_characters)}")
        logger.info(f"触发关键词：{self.trigger_keywords}")

    def _scan_characters(self) -> list:
        if not os.path.exists(self.resource_dir):
            return []
        return [f[:-4] for f in os.listdir(self.resource_dir) if f.lower().endswith(".png")]

    def _resolve_character(self, name: str) -> str | None:
        key = name.lower()
        if key in self.available_characters:
            return key
        if key in self.CHARACTER_ALIASES:
            mapped = self.CHARACTER_ALIASES[key]
            if mapped in self.available_characters:
                return mapped
        return None

    def _list_characters(self) -> str:
        cn_map = {}
        for alias, eng in self.CHARACTER_ALIASES.items():
            if not alias.isascii() and eng in self.available_characters:
                cn_map.setdefault(eng, []).append(alias)
        lines = ["📋 可用角色列表（文字版）："]
        for eng in sorted(self.available_characters):
            cns = cn_map.get(eng, [])
            cn_str = "、".join(cns) if cns else "无中文别名"
            lines.append(f"{eng} ({cn_str})")
        return "\n".join(lines)

    def _send_random_image(self, folder: str) -> str | None:
        """从指定文件夹随机选择一张图片的路径"""
        if not os.path.exists(folder):
            return None
        images = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if not images:
            return None
        chosen = random.choice(images)
        return os.path.join(folder, chosen)

    @filter.regex(r'.*')
    async def on_any_message(self, event: AstrMessageEvent):
        message_str = event.message_str.strip()
        for kw in self.trigger_keywords:
            if kw and kw in message_str:
                img_path = self._send_random_image(self.emoji_dir)
                if img_path:
                    yield event.chain_result([Image.fromFileSystem(img_path)])
                else:
                    yield event.plain_result("❌ emoji 文件夹为空或不存在，请先放入图片。")
                return

    @filter.command("arc表情包")
    async def arc_emoji_command(self, event: AstrMessageEvent):
        """从 emoji 文件夹随机发送一张表情包图片"""
        img_path = self._send_random_image(self.emoji_dir)
        if img_path:
            yield event.chain_result([Image.fromFileSystem(img_path)])
        else:
            yield event.plain_result("❌ emoji 文件夹为空或不存在，请先放入图片。")

    @filter.command("arc角色列表")
    async def arc_role_list_command(self, event: AstrMessageEvent):
        """从 list 文件夹随机发送一张角色预览图"""
        img_path = self._send_random_image(self.list_dir)
        if img_path:
            yield event.chain_result([Image.fromFileSystem(img_path)])
        else:
            yield event.plain_result("❌ list 文件夹为空或不存在，请先放入图片。")

    @filter.command("arc")
    async def arc_command(self, event: AstrMessageEvent):
        """Arcaea 表情包生成器（简化版）
        用法：/arc <角色> <文字>
        当文字长度 ≤3 时，左右两边都渲染；>3 时，只渲染左侧。
        所有参数（字体大小、旋转、边距）可在 WebUI 配置中调整。
        """
        message_str = event.message_str.strip()
        parts = message_str.split(maxsplit=2)

        if len(parts) == 1:
            yield event.plain_result(
                "🎮 Arcaea 表情包生成器（简化版）\n"
                "▶ 用法：/arc <角色> <文字>\n"
                "   - 当文字长度 ≤3 时，左右两边都渲染\n"
                "   - 当文字长度 >3 时，只渲染左侧\n"
                "▶ 查看文字角色列表：/arc list\n"
                "▶ 查看图片角色列表：/arc角色列表\n"
                "▶ 查看帮助：/arc_help\n"
                "💡 字体大小、旋转、边距可在 WebUI 插件配置中调整。"
            )
            return

        if len(parts) >= 2 and parts[1].lower() == "list":
            yield event.plain_result(self._list_characters())
            return

        if len(parts) < 2:
            yield event.plain_result("参数不足。使用 /arc_help 查看帮助")
            return

        raw_character = parts[1]
        character = self._resolve_character(raw_character)
        if character is None:
            yield event.plain_result(
                f"未知角色：{raw_character}。可用角色：{', '.join(self.available_characters)}\n"
                f"使用 /arc list 查看完整角色列表（含中文别名）"
            )
            return

        if len(parts) < 3:
            yield event.plain_result("请提供文字内容")
            return

        text = parts[2].strip()
        if not text:
            yield event.plain_result("文字不能为空")
            return

        # 判断文字长度（字符数）
        render_right = len(text) <= 3

        if not self.simple_font_path:
            yield event.plain_result("❌ 简化模式不可用：fonts 文件夹中未找到 TTF 字体文件")
            return

        img_path = None
        try:
            img_path = self.generator.generate_simple(
                character=character,
                text=text,
                font_path=self.simple_font_path,
                size=self.simple_font_size,
                left_rotation=self.simple_left_rotation,
                right_rotation=self.simple_right_rotation,
                left_margin=self.simple_left_margin,
                top_margin=self.simple_top_margin,
                right_margin=self.simple_right_margin,
                render_right=render_right
            )
            yield event.chain_result([Image.fromFileSystem(img_path)])
        except Exception as e:
            logger.error(f"生成失败: {e}")
            yield event.plain_result(f"生成失败：{str(e)}")
        finally:
            # 确保临时文件被删除，避免磁盘泄漏
            if img_path and os.path.exists(img_path):
                try:
                    os.unlink(img_path)
                except Exception as e:
                    logger.error(f"删除临时文件失败: {e}")

    @filter.command("arc_help")
    async def arc_help(self, event: AstrMessageEvent):
        help_img_path = os.path.join(self.resource_dir, "arc_help.png")
        if os.path.exists(help_img_path):
            yield event.chain_result([Image.fromFileSystem(help_img_path)])
        else:
            help_text = (
                "🎮 Arcaea 表情包生成器帮助\n"
                "▶ 用法：/arc <角色> <文字>\n"
                "   - 当文字长度 ≤3 时，左右两边都渲染\n"
                "   - 当文字长度 >3 时，只渲染左侧\n"
                "▶ 字体大小、旋转角度、边距可在 WebUI 插件配置中调整。\n"
                "▶ 文字角色列表：/arc list\n"
                "▶ 图片角色列表：/arc角色列表\n"
                "▶ 随机表情包：/arc表情包 或包含关键词（可配置）的消息\n"
                "示例：/arc 光 你好（短文字，双文字）\n"
                "示例：/arc 光 欢迎光临（长文字，单文字）"
            )
            yield event.plain_result(help_text)

    async def terminate(self):
        logger.info("Arcaea Sticker 插件已卸载")
