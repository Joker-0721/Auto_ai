import os
import re
import requests
import json
import time
from PIL import Image
import io
import base64

# 配置
API_KEY = "YOUR_API_KEY"  # 请替换为您的API密钥
API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"  # 使用Stability AI的API

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

# 优化提示词
def optimize_prompt(description):
    # 提取关键信息
    prompt = description.strip()
    
    # 添加额外的提示词以确保生成高质量的像素艺术
    enhanced_prompt = f"{prompt}, pixel art style, 16-bit colors, game character, clear details, no text"
    
    return enhanced_prompt

# 生成图像
def generate_image(prompt, api_key, api_url):
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
        return match.group(1).strip()
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
        
        # 优化提示词
        prompt = optimize_prompt(description)
        print(f"优化后的提示词: {prompt[:100]}...")
        
        # 提取NPC名称
        npc_name = extract_npc_name(description)
        
        # 生成图像
        print("生成图像中...")
        image = generate_image(prompt, API_KEY, API_URL)
        
        if image:
            # 保存图像
            output_path = os.path.join(OUTPUT_DIR, f"{npc_name}.png")
            image.save(output_path)
            print(f"图像已保存到: {output_path}")
        else:
            print("图像生成失败")
        
        # 添加延迟以避免API限制
        time.sleep(2)

# 运行程序
if __name__ == "__main__":
    print("开始生成NPC像素图像...")
    main()
    print("\n所有NPC像素图像生成完成！")