# 更新日志 (CHANGELOG)

所有对本项目的显著变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，  
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [4.2.0] - 2026-03-20
### 优化
- **配置解析健壮性**：在 `__init__` 中增加了异常处理，确保用户通过 WebUI 输入无效值时不会导致插件崩溃，安全回退到默认值。
- **临时文件泄漏修复**：在 `arc_command` 中使用 `try...finally` 确保生成的临时图片在发送后被立即删除，避免磁盘空间耗尽。
- **移除死代码**：删除了 `utils/generator.py` 中未调用的 `_wrap_text`、`_find_chinese_font` 及描边相关逻辑，代码大幅精简。
- **现代类型提示**：移除了 `typing.List` 和 `typing.Dict` 的导入，改用 Python 内置的 `list` 和 `dict`（兼容 Python 3.9+）。

## [4.1.0] - 2026-03-18
### 新增
- 添加 `/arc角色列表` 命令，可从 `./list` 文件夹随机发送一张角色预览图。

## [4.0.0] - 2026-03-18
### 移除
- **删除复杂模式**：不再支持自定义位置、角度、颜色、描边等参数，仅保留简化模式。
### 变更
- **智能单双文字**：当文字长度 ≤3 字符时，左右两边都渲染；>3 字符时，只渲染左侧。所有渲染参数（字体大小、旋转角度、边距）仍可通过 WebUI 配置。

## [3.2.0] - 2026-03-18
### 新增
- **随机表情包功能**：新增 `/arc表情包` 命令，从 `./emoji` 文件夹随机发送图片；支持关键词触发（可配置，默认“arc表情包”），用户消息包含关键词时自动发送随机表情包。

## [3.1.0] - 2026-03-18
### 新增
- **完整角色别名**：根据用户提供的列表，更新了所有 Arcaea 角色的中文别名映射。

## [3.0.0] - 2026-03-17
### 变更
- **WebUI 配置标准化**：采用 `_conf_schema.json` 定义可配置项，通过 `main.py` 的 `config` 参数读取，实现在管理界面快速调整简化模式的字体大小、旋转角度、边距等参数。

## [2.5.0] - 2026-03-17
### 变更
- **配置方式调整**：移除 `metadata.yaml` 中的 `config` 字段，改为通过 `__init__` 的 `config` 参数接收配置（与示例插件一致）。

## [2.4.0] - 2026-03-17
### 新增
- **WebUI 可配置参数**：为简化模式添加字体大小、旋转角度、边距等 6 个配置项，用户可通过管理界面调整。

## [2.3.0] - 2026-03-17
### 变更
- **指令整合**：不再新增 `/arcs` 指令，简化模式集成到原有 `/arc` 指令中：无任何选项参数时自动进入简化模式（固定左上/右上双文字，仅输出图片）；带选项时进入复杂模式。

## [2.2.0] - 2026-03-17
### 新增
- **描边效果**：支持 `-w` 参数设置描边宽度。
- **多行文字**：自动换行，支持 `\n` 手动换行。
- **角色默认颜色**：根据角色自动匹配默认文字颜色。
- **智能字体大小**：文字过长时自动缩小以适配图片宽度。
- **参数范围校验**：对 `-s`、`-x`、`-y`、`-r` 进行范围检查。
- **帮助指令**：`/arc_help` 返回图文并茂的使用说明（可放置 `arc_help.png`）。

## [2.1.0] - 2026-03-17
### 新增
- **自定义字体配置**：用户可通过 WebUI 设置自定义字体路径，插件优先使用该字体生成图片。

## [2.0.0] - 2026-03-17
### 新增
- **中文角色映射**：支持“光”、“对立”等中文别名自动匹配英文文件名。
- **角色列表指令**：`/arc list` 显示所有可用角色（英文名 + 中文别名）。

## [1.1.0] - 2026-03-17
### 新增
- **角色列表指令**：`/arc list` 显示所有可用角色。

## [1.0.0] - 2026-03-17
### 新增
- **初始发布**：基于 [nonebot-plugin-arcaea-sticker](https://github.com/JQ-28/nonebot-plugin-arcaea-sticker) 重构，适配 AstrBot。
- **核心功能**：支持简化模式（固定双文字）和复杂模式（自定义位置、角度、颜色、描边）。
- **中文别名**：内置“光”、“对立”等常见角色中文名映射。
- **字体管理**：简化模式强制使用 `./fonts` 文件夹下的第一个 TTF 字体文件。
- **纯图片输出**：简化模式成功生成后只返回图片，无文字提示。

---

[4.2.0]: https://github.com/1-20182/astrbot_plugin_arcaea/compare/v4.1.0...v4.2.0
[4.1.0]: https://github.com/1-20182/astrbot_plugin_arcaea/compare/v4.0.0...v4.1.0
[4.0.0]: https://github.com/1-20182/astrbot_plugin_arcaea/compare/v3.2.0...v4.0.0
[3.2.0]: https://github.com/1-20182/astrbot_plugin_arcaea/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/1-20182/astrbot_plugin_arcaea/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/1-20182/astrbot_plugin_arcaea/compare/v2.5.0...v3.0.0
[2.5.0]: https://github.com/1-20182/astrbot_plugin_arcaea/compare/v2.4.0...v2.5.0
[2.4.0]: https://github.com/1-20182/astrbot_plugin_arcaea/compare/v2.3.0...v2.4.0
[2.3.0]: https://github.com/1-20182/astrbot_plugin_arcaea/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/1-20182/astrbot_plugin_arcaea/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/1-20182/astrbot_plugin_arcaea/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/1-20182/astrbot_plugin_arcaea/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/1-20182/astrbot_plugin_arcaea/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/1-20182/astrbot_plugin_arcaea/releases/tag/v1.0.0
