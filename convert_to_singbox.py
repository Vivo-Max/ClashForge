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

    # 配置 API 请求
    url = "https://clash2sfa.xmdhs.com/api/convert"  # 假设的 API 端点，需替换为实际端点
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "ClashForge/1.0"  # 模拟浏览器请求
    }
    payload = {
        "config": clash_config,  # 模拟 textarea 的 config 输入
        "include": include,      # 节点包含关键字
        "exclude": exclude,      # 节点排除关键字
        "addTag": False,         # 是否添加标签
        "disableUrlTest": False  # 是否禁用 URL 测试
    }

    # 配置重试机制
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    # 发送 POST 请求
    try:
        response = session.post(url, headers=headers, json=payload)
        response.raise_for_status()  # 检查请求是否成功
        singbox_config = response.json()  # 假设返回 JSON 格式的 sing-box 配置
    except requests.RequestException as e:
        print(f"API 转换请求失败: {e}")
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
