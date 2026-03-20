# 🎨 Arcaea 表情包生成器 (AstrBot 版)

[![AstrBot](https://img.shields.io/badge/AstrBot-插件-green.svg)](https://github.com/Soulter/AstrBot) [![Version](https://img.shields.io/badge/Version-4.2.0-blue)]()

本插件是 [nonebot-plugin-arcaea-sticker](https://github.com/JQ-28/nonebot-plugin-arcaea-sticker) 的 **AstrBot 重构版**，专为 Arcaea 玩家设计，可快速生成带有自定义文字的游戏风格表情包。

---

## ✨ 功能亮点

- **双模式支持**  
  - **简化模式**：文字自动放置在图片左上角（逆时针45°）和右上角（顺时针45°），强制使用 `./fonts` 下的 TTF 字体，仅输出图片，干净利落。  
  - **复杂模式**：支持自定义文字位置、大小、旋转角度、颜色、描边宽度，自由度极高。

- **全角色中文别名**  
  内置 20+ 角色的中文映射（如“光”→“hikari”，“对立”→“tairitsu”，“伊莉丝”→“ilith”），使用中文名即可快速调用，无需记忆英文文件名。

- **WebUI 可视化配置**  
  字体大小、旋转角度、边距等参数均可通过 AstrBot 管理界面即时调整，无需修改代码。

- **纯图片输出**  
  简化模式成功生成后只返回图片，无任何文字提示，完美嵌入群聊表情包需求。

---

## 📥 安装与配置

### 1. 放置文件
将本插件文件夹 `astrbot_plugin_arcaea_sticker` 放入 AstrBot 的 `data/plugins` 目录，确保目录结构如下：

```

astrbot_plugin_arcaea_sticker/
├── metadata.yaml
├── _conf_schema.json
├── main.py
├── utils/
│   └── generator.py
├── fonts/          (需手动创建，放入 .ttf 字体)
└── resources/      (需手动创建，放入角色图片)

```

### 2. 安装依赖
在插件目录执行：
```bash
pip install Pillow
```

3. 准备资源

· 字体：在 fonts 文件夹中放入至少一个 TTF 字体文件（简化模式强制使用该字体）。
· 角色图片：在 resources 文件夹中放入角色 PNG 图片，文件名必须与英文名一致（例如 hikari.png、tairitsu.png、ilith.png 等）。支持的角色及对应英文名见下文。

4. 重启 AstrBot

重启后，在 WebUI 的“插件管理”页面找到本插件，点击“配置”按钮即可调整简化模式的各项参数。

---

📋 角色列表

发送 /arc list 可查看当前支持的角色及其中文别名。以下为内置别名（用户可自行在 main.py 的 CHARACTER_ALIASES 中扩充）：

英文文件名 中文别名
aichan AI酱
ayu 彩梦
eto 爱托
hikari 光
hikari2 无中文别名
ilith 伊莉丝
insight 洞烛, 拉可弥拉
kanae 群愿
kou 红
lagrange 拉格兰
lethe 忘却
luna 露娜
maya 摩耶
nami 奈美
nonoka 野乃香
saya 咲弥
shirabe 调
shirahime 白姬
tairitsu 对立
tairitsu2 无中文别名
tairitsu3 无中文别名
vita 维塔

💡 如果角色图片文件名与上表不同，请自行修改 CHARACTER_ALIASES 映射。

---

🎮 指令用法

1. 简化模式

```
/arc <角色> <文字>
```

· 示例：/arc 光 你好
· 功能：文字同时出现在左上角（逆时针45°）和右上角（顺时针45°），使用 fonts 下的字体，仅输出图片。
· 参数可在 WebUI 配置中调整（字体大小、旋转角度、边距）。

2. 复杂模式

```
/arc <角色> <文字> [选项]
```

选项说明：

· -s 字体大小 (20~45，默认35)
· -x X坐标 (0~296，默认148)
· -y Y坐标 (0~256，默认128)
· -r 旋转角度 (-180~180，默认-12)
· -c 颜色 (如 red, #FF0000)
· -w 描边宽度 (如 2，默认0)

示例：/arc 光 欢迎光临 -s 40 -x 200 -y 150 -r 0 -c gold -w 2

3. 其他命令

· /arc list —— 查看所有可用角色及中文别名
· /arc_help —— 显示详细帮助（若 resources 中存在 arc_help.png 则返回图片，否则返回文字版）

---

⚙️ WebUI 可配置项

配置项 说明 默认值
custom_font_path 复杂模式自定义字体路径 空
simple_font_size 简化模式字体大小 35
simple_left_rotation 左上角文字旋转角度 -45
simple_right_rotation 右上角文字旋转角度 45
simple_left_margin 左上角边距（距左/上） 20
simple_top_margin 上边距 20
simple_right_margin 右上角右边距 20

---

🙏 致谢与友情链接

· 本插件基于 nonebot-plugin-arcaea-sticker 重构，感谢原作者的创意与开源精神！
· 特别感谢 yangze321 为本项目贡献了自定义的 Arcaea 表情包资源，极大地丰富了角色的可玩性。
· 如果你使用 NoneBot2，可直接前往原仓库体验。

NoneBot 原版仓库：https://github.com/JQ-28/nonebot-plugin-arcaea-sticker

---

📄 许可证

本项目采用 MIT 许可证。欢迎二次开发，请保留原作者信息。

---

如有问题或建议，欢迎提交 Issue 或 Pull Request。

```
