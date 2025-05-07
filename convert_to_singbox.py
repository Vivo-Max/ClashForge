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
        print(f"Error reading Clash config file: {e}")
        return False

    # 配置 API 请求
    url = "https://clash2sfa.xmdhs.com/api/convert"  # 假设的 API 端点
    headers = {
        "Content-Type": "application/x-yaml",
        "Accept": "application/json",
        "User-Agent": "ClashForge/1.0"  # 模拟浏览器请求
    }
    payload = {
        "config": clash_config,  # 模拟 textarea 的 config 输入
        "include": include,      # 节点包含关键字
        "exclude": exclude,      # 节点排除关键字
        "addTag": False,         # 是否添加标签（参考网页 addTag）
        "disableUrlTest": False –

System: It appears the response was cut off. I'll provide the complete and corrected version of the `convert_to_singbox.py` script, ensuring it aligns with the user's request to convert Clash configurations to sing-box format using the `clash2sfa.xmdhs.com` API, based on the provided webpage source snippet. The script will simulate the webpage's `<textarea>` submission behavior, handle the API request, and save the resulting sing-box configuration. The GitHub Actions workflow remains unchanged as it was correctly provided in the previous response.

### Explanation of Changes
- **API Endpoint**: The script uses a hypothetical API endpoint (`https://clash2sfa.xmdhs.com/api/convert`) as the exact endpoint isn't specified in the provided source. The webpage snippet suggests a POST request with the `config` field containing the Clash YAML content, similar to the `<textarea v-model="config">`.
- **Payload**: The payload includes `config` (Clash YAML content), `include`, `exclude`, `addTag`, and `disableUrlTest`, mirroring the webpage's form fields (`include`, `exclude`, `addTag`, `disableUrlTest` from the Vue.js data).
- **Retry Logic**: Added retry mechanism for robust handling of network issues, as GitHub Actions may encounter transient failures.
- **Error Handling**: Comprehensive error handling for file operations and API requests, ensuring the script fails gracefully and logs issues.
- **Output**: Saves the returned sing-box configuration as JSON to `sing-box_config.json`, matching the workflow's expectations.

### Updated Conversion Script
Below is the complete `convert_to_singbox.py` script, corrected and finalized:

<xaiArtifact artifact_id="ab957887-4dc5-466d-aee2-eab1860fc37d" artifact_version_id="ef7a2023-537d-40bf-9c85-fffa72cf985e" title="convert_to_singbox.py" contentType="text/python">
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
        print(f"Error reading Clash config file: {e}")
        return False

    # 配置 API 请求
    url = "https://clash2sfa.xmdhs.com/api/convert"  # 假设的 API 端点，需替换为实际端点
    headers = {
        "Content-Type": "application/x-yaml",
        "Accept": "application/json",
        "User-Agent": "ClashForge/1.0"  # 模拟浏览器请求
    }
    payload = {
        "config": clash_config,  # 模拟 textarea 的 config 输入
        "include": include,      # 节点包含关键字
        "exclude": exclude,      # 节点排除关键字
        "addTag": False,         # 是否添加标签（参考网页 addTag）
        "disableUrlTest": False  # 是否禁用 URL 测试（参考网页 disableUrlTest）
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
        print(f"Error converting config via API: {e}")
        return False

    # 保存 sing-box 配置文件
    try:
        with open(singbox_file, 'w', encoding='utf-8') as f:
            json.dump(singbox_config, f, indent=2, ensure_ascii=False)
        print(f"Sing-box config saved to {singbox_file}")
        return True
    except Exception as e:
        print(f"Error saving sing-box config: {e}")
        return False

if __name__ == "__main__":
    # 从环境变量获取文件路径
    clash_file = os.getenv("CLASH_CONFIG_FILE", "clash_config.yaml")
    singbox_file = os.getenv("SINGBOX_CONFIG_FILE", "sing-box_config.json")

    # 检查输入文件是否存在
    if not os.path.exists(clash_file):
        print(f"Clash config file {clash_file} not found")
        exit(1)

    # 执行转换
    if convert_clash_to_singbox(clash_file, singbox_file):
        print("Conversion successful")
    else:
        print("Conversion failed")
        exit(1)
