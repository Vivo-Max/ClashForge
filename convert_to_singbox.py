import os
import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def convert_clash_to_singbox(clash_file, singbox_file, include="", exclude=""):
    # 读取 Clash 配置文件
    try:
        with open(clash_file, 'r', encoding='utf-8') as f:
            clash_config = f.read()
    except Exception as e:
        print(f"读取 Clash 配置文件失败: {e}")
        return False

    # 可能的 API 端点列表
    possible_endpoints = [
        "https://clash2sfa.xmdhs.com/api/convert",
        "https://clash2sfa.xmdhs.com/convert",
        "https://clash2sfa.xmdhs.com/api/subscribe",
        "https://clash2sfa.xmdhs.com/api/v1/convert"
    ]
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "ClashForge/1.0"
    }
    payload = {
        "config": clash_config,
        "include": include,
        "exclude": exclude,
        "addTag": False,
        "disableUrlTest": False
    }

    # 配置重试机制
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    # 尝试每个端点
    for url in possible_endpoints:
        print(f"尝试 API 端点: {url}")
        try:
            response = session.post(url, headers=headers, json=payload)
            response.raise_for_status()
            singbox_config = response.json()
            print(f"API 请求成功，端点: {url}")
            break
        except requests.RequestException as e:
            print(f"API 请求失败，端点 {url}: {e}")
            continue
    else:
        print("所有 API 端点均失败，请检查端点或使用替代方案")
        return False

    # 保存 sing-box 配置文件
    try:
        with open(singbox_file, 'w', encoding='utf-8') as f:
            json.dump(singbox_config, f, indent=2, ensure_ascii=False)
        print(f"sing-box 配置文件已保存至 {singbox_file}")
        return True
    except Exception as e:
        print(f"保存 sing-box 配置文件失败: {e}")
        return False

if __name__ == "__main__":
    # 从环境变量获取文件路径
    clash_file = os.getenv("CLASH_CONFIG_FILE", "clash_config.yaml")
    singbox_file = os.getenv("SINGBOX_CONFIG_FILE", "sing-box_config.json")

    # 检查输入文件是否存在
    if not os.path.exists(clash_file):
        print(f"Clash 配置文件 {clash_file} 未找到")
        exit(1)

    # 执行转换
    if convert_clash_to_singbox(clash_file, singbox_file):
        print("转换成功")
    else:
        print("转换失败")
        exit(1)
