# NPC像素图像生成工具

这个工具包含两个Python脚本，用于根据NPC描述生成像素风格的游戏角色图像。

## 文件说明

1. `generate_npc_pixels.py` - 使用AI图像生成API创建高质量的像素风格NPC图像
2. `generate_local_pixels.py` - 使用本地Python库生成简单的像素风格NPC图像（不需要API密钥）

## 使用方法

### 使用AI API生成图像（高质量）

1. 打开 `generate_npc_pixels.py` 文件
2. 将 `API_KEY` 变量替换为您的Stability AI API密钥
3. 运行脚本：
   ```
   python generate_npc_pixels.py
   ```
4. 生成的图像将保存在 `npc_pixels` 文件夹中

### 使用本地生成图像（简单版本）

如果您没有API密钥或想快速生成简单的像素图像，可以使用本地生成脚本：

1. 运行脚本：
   ```
   python generate_local_pixels.py
   ```
2. 生成的图像将保存在 `npc_pixels` 文件夹中

## 自定义描述

您可以编辑项目根目录中的 `npc_pixel_descriptions.txt` 文件来添加或修改NPC描述。每个描述应包含以下信息：

- 职业
- 性别
- 年龄
- 外貌特征（发色、体型等）
- 服装描述
- 表情或姿态
- 手持物品

描述之间用空行分隔。

## 注意事项

1. 使用AI API生成图像需要有效的API密钥和网络连接
2. 本地生成的图像质量较简单，仅提供基本的像素风格表现
3. 生成的图像默认为32x32像素大小，符合描述中的要求