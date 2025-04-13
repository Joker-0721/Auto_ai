import os
import re
import time
import random
from PIL import Image, ImageDraw
import requests
import json
import io
import base64

# 配置
API_KEY = "YOUR_API_KEY"  # 请替换为您的API密钥
API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"  # 使用Stability AI的API
USE_API = False  # 设置为True使用API生成，False使用本地生成

# 创建输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "npc_pixels")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 读取NPC描述文件
def read_npc_descriptions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 按空行分割每个NPC描述
    descriptions = [desc.strip() for desc in content.split('\n\n') if desc.strip()]
    return descriptions

# 解析描述提取关键信息
def parse_description(description):
    # 提取性别
    gender = "男" if "男" in description else "女" if "女" in description else "未知"
    
    # 提取年龄
    age_match = re.search(r'(\d+)岁', description)
    age = int(age_match.group(1)) if age_match else 30
    
    # 提取发色
    hair_colors = {
        "白": (230, 230, 230),
        "黑": (30, 30, 30),
        "金": (230, 190, 90),
        "红": (200, 80, 60),
        "棕": (150, 90, 50),
        "灰": (160, 160, 160)
    }
    
    hair_color = (100, 100, 100)  # 默认发色
    for color_name, rgb in hair_colors.items():
        if color_name in description:
            hair_color = rgb
            break
    
    # 提取服装颜色
    cloth_colors = {
        "蓝": (60, 100, 200),
        "红": (200, 60, 60),
        "绿": (60, 180, 60),
        "白": (230, 230, 230),
        "黑": (40, 40, 40),
        "棕": (140, 100, 60)
    }
    
    cloth_color = (100, 100, 150)  # 默认服装颜色
    for color_name, rgb in cloth_colors.items():
        if color_name in description and "衣" in description[description.index(color_name)-5:description.index(color_name)+5]:
            cloth_color = rgb
            break
    
    # 提取手持物品
    items = []
    item_match = re.search(r'手持([^，。]+)', description)
    if item_match:
        items.append(item_match.group(1))
    
    # 提取职业/角色
    role_match = re.search(r'像素风格的([^，]+)', description)
    role = role_match.group(1) if role_match else "未知角色"
    
    # 提取体型特征
    body_features = []
    for feature in ["强壮", "结实", "瘦高", "矮小", "健壮"]:
        if feature in description:
            body_features.append(feature)
    
    # 提取面部特征
    face_features = []
    for feature in ["胡须", "眼镜", "雀斑", "伤疤", "皱纹"]:
        if feature in description:
            face_features.append(feature)
    
    return {
        "gender": gender,
        "age": age,
        "hair_color": hair_color,
        "cloth_color": cloth_color,
        "items": items,
        "role": role,
        "body_features": body_features,
        "face_features": face_features
    }

# 生成简单的像素风格图像
def generate_local_pixel_image(npc_info):
    # 创建32x32像素的图像，使用RGBA模式支持透明度
    image = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 根据年龄调整人物大小
    if npc_info["age"] < 15:  # 儿童
        body_height = 12
        head_size = 8
        y_offset = 8
    elif npc_info["age"] > 60:  # 老年
        body_height = 16
        head_size = 10
        y_offset = 4
    else:  # 成年
        body_height = 18
        head_size = 9
        y_offset = 3
    
    # 肤色根据描述调整
    if "黝黑" in str(npc_info):
        skin_color = (150, 110, 80)
    elif "白皙" in str(npc_info):
        skin_color = (240, 220, 200)
    else:
        skin_color = (220, 180, 150)  # 默认肤色
    
    # 绘制头部
    head_x = 16 - head_size // 2
    head_y = y_offset
    draw.rectangle((head_x, head_y, head_x + head_size, head_y + head_size), fill=skin_color)
    
    # 绘制头发
    hair_y = head_y
    hair_height = head_size // 3
    draw.rectangle((head_x, hair_y, head_x + head_size, hair_y + hair_height), fill=npc_info["hair_color"])
    
    # 绘制眼睛
    eye_size = max(1, head_size // 5)
    eye_y = head_y + head_size // 3
    left_eye_x = head_x + head_size // 3 - eye_size // 2
    right_eye_x = head_x + 2 * head_size // 3 - eye_size // 2
    draw.rectangle((left_eye_x, eye_y, left_eye_x + eye_size, eye_y + eye_size), fill=(0, 0, 0))
    draw.rectangle((right_eye_x, eye_y, right_eye_x + eye_size, eye_y + eye_size), fill=(0, 0, 0))
    
    # 绘制面部特征
    if "眼镜" in npc_info["face_features"]:
        # 简单的眼镜框
        glasses_y = eye_y - 1
        draw.rectangle((left_eye_x - 1, glasses_y, right_eye_x + eye_size + 1, glasses_y + eye_size + 1), outline=(50, 50, 50))
    
    if "胡须" in npc_info["face_features"]:
        # 简单的胡须
        beard_y = head_y + head_size - head_size // 4
        beard_width = head_size // 2
        beard_x = head_x + head_size // 2 - beard_width // 2
        draw.rectangle((beard_x, beard_y, beard_x + beard_width, beard_y + 2), fill=(npc_info["hair_color"][0], npc_info["hair_color"][1], npc_info["hair_color"][2]))
    
    # 绘制身体
    body_width = head_size + 2
    body_x = 16 - body_width // 2
    body_y = head_y + head_size
    draw.rectangle((body_x, body_y, body_x + body_width, body_y + body_height), fill=npc_info["cloth_color"])
    
    # 绘制手臂
    arm_width = 3
    arm_height = body_height - 2
    left_arm_x = body_x - arm_width
    right_arm_x = body_x + body_width
    arm_y = body_y + 2
    
    # 根据性别和描述调整手臂
    if npc_info["gender"] == "男" and ("强壮" in npc_info["body_features"] or "结实" in npc_info["body_features"]):
        arm_width += 1
    
    draw.rectangle((left_arm_x, arm_y, left_arm_x + arm_width, arm_y + arm_height), fill=npc_info["cloth_color"])
    draw.rectangle((right_arm_x, arm_y, right_arm_x + arm_width, arm_y + arm_height), fill=npc_info["cloth_color"])
    
    # 绘制腿
    leg_width = 4
    leg_height = 6
    leg_gap = 2
    left_leg_x = 16 - leg_width - leg_gap // 2
    right_leg_x = 16 + leg_gap // 2
    leg_y = body_y + body_height
    
    leg_color = (min(npc_info["cloth_color"][0] - 30, 255), 
                min(npc_info["cloth_color"][1] - 30, 255), 
                min(npc_info["cloth_color"][2] - 30, 255))
    
    draw.rectangle((left_leg_x, leg_y, left_leg_x + leg_width, leg_y + leg_height), fill=leg_color)
    draw.rectangle((right_leg_x, leg_y, right_leg_x + leg_width, leg_y + leg_height), fill=leg_color)
    
    # 如果有手持物品，在右手添加简单图形
    if npc_info["items"]:
        item_x = right_arm_x + arm_width
        item_y = arm_y + arm_height // 2
        item_size = 4
        
        # 根据物品类型选择颜色
        item = npc_info["items"][0].lower()
        if "剑" in item or "刀" in item or "锤" in item or "斧" in item:
            item_color = (200, 200, 200)  # 金属色
        elif "书" in item or "纸" in item or "卷" in item:
            item_color = (240, 230, 200)  # 纸张色
        elif "花" in item or "草" in item or "药" in item:
            item_color = (100, 200, 100)  # 植物色
        elif "杖" in item or "棍" in item or "木" in item:
            item_color = (150, 100, 50)  # 木头色
        else:
            item_color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
        
        draw.rectangle((item_x, item_y, item_x + item_size, item_y + item_size), fill=item_color)
    
    return image

# 优化提示词
def optimize_prompt(description):
    # 提取关键信息
    prompt = description.strip()
    
    # 添加额外的提示词以确保生成高质量的像素艺术
    enhanced_prompt = f"{prompt}, pixel art style, 16-bit colors, game character, clear details, no text"
    
    return enhanced_prompt

# 使用API生成图像
def generate_api_image(prompt, api_key, api_url):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    payload = {
        "text_prompts": [
            {
                "text": prompt,
                "weight": 1.0
            }
        ],
        "cfg_scale": 7,
        "height": 512,
        "width": 512,
        "samples": 1,
        "steps": 30,
        "style_preset": "pixel-art"
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            # 解析返回的图像数据
            image_data = base64.b64decode(data["artifacts"][0]["base64"])
            image = Image.open(io.BytesIO(image_data))
            # 调整大小为32x32像素
            image = image.resize((32, 32), Image.NEAREST)
            return image
        else:
            print(f"错误: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"生成图像时出错: {e}")
        return None

# 提取NPC名称
def extract_npc_name(description):
    # 尝试从描述中提取职业作为文件名
    match = re.search(r'像素风格的([^，]+)', description)
    if match:
        # 替换文件名中的非法字符，包括斜杠
        name = match.group(1).strip()
        # 将斜杠替换为下划线或其他安全字符
        name = name.replace('/', '_').replace('\\', '_')
        return name
    else:
        # 如果无法提取，使用索引作为名称
        return f"npc_{int(time.time())}"

# 主函数
def main():
    # 描述文件路径
    description_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "npc_pixel_descriptions.txt")
    
    # 读取描述
    descriptions = read_npc_descriptions(description_file)
    
    print(f"找到 {len(descriptions)} 个NPC描述")
    
    # 处理每个描述
    for i, description in enumerate(descriptions):
        print(f"\n处理NPC {i+1}/{len(descriptions)}")
        print(f"描述: {description[:100]}...")
        
        # 提取NPC名称
        npc_name = extract_npc_name(description)
        
        if USE_API:
            # 使用API生成
            print("使用API生成图像...")
            # 优化提示词
            prompt = optimize_prompt(description)
            print(f"优化后的提示词: {prompt[:100]}...")
            
            # 生成图像
            image = generate_api_image(prompt, API_KEY, API_URL)
        else:
            # 使用本地生成
            print("使用本地生成图像...")
            # 解析描述
            npc_info = parse_description(description)
            print(f"解析信息: 性别={npc_info['gender']}, 年龄={npc_info['age']}, 角色={npc_info['role']}")
            
            # 生成图像
            image = generate_local_pixel_image(npc_info)
        
        if image:
            # 保存图像
            output_path = os.path.join(OUTPUT_DIR, f"{npc_name}.png")
            image.save(output_path)
            print(f"图像已保存到: {output_path}")
        else:
            print("图像生成失败")
        
        # 添加延迟以避免API限制
        if USE_API:
            time.sleep(2)

# 运行程序
if __name__ == "__main__":
    print("开始生成NPC像素图像...")
    main()
    print("\n所有NPC像素图像生成完成！")