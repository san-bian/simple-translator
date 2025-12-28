import json
from plyer import notification
import pyperclip
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.tmt.v20180321 import tmt_client, models


def get_clipboard_text():
    try:
        clipboard_content = pyperclip.paste()
        print(f"剪贴板内容: {clipboard_content}")
        return clipboard_content
    except Exception as e:
        print(f"获取剪贴板失败: {e}")
        return None


def tencent_translate(text, source="en", target="zh"):
    try:
        secret_id = ""  # 替换为你的SecretId
        secret_key = ""  # 替换为你的SecretKey

        cred = credential.Credential(secret_id, secret_key)

        http_profile = HttpProfile()
        http_profile.endpoint = "tmt.tencentcloudapi.com"  # 指定接入地域域名

        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile

        client = tmt_client.TmtClient(cred, "ap-guangzhou", client_profile)

        req = models.TextTranslateRequest()

        # 设置参数
        params = {
            "SourceText": text,
            "Source": source,
            "Target": target,
            "ProjectId": 0
        }
        req.from_json_string(json.dumps(params))

        # 发送请求
        resp = client.TextTranslate(req)
        print(resp)
        # 解析响应
        result = json.loads(resp.to_json_string())
        return result.get("TargetText")

    except Exception as e:
        return f"翻译失败: {str(e)}"


def main():
    # 获取剪贴板内容
    text = get_clipboard_text()
    if not text or not text.strip():
        print("剪贴板为空或只有空白字符")
        return

    # 限制文本长度，避免API限制
    if len(text) > 2000:  # 腾讯云API限制
        print("文本过长，截取前2000字符")
        text = text[:2000]

    print(f"原文: {text}")
    print("-" * 50)

    # 翻译
    translated = tencent_translate(text)
    print("-" * 50)
    print(f"翻译: {translated}")

    # 显示通知
    try:
        notification.notify(
            title="翻译结果",
            message=f"{text}\n→ {translated}",
            timeout=5
        )
    except Exception as e:
        print(f"显示通知失败: {e}")


if __name__ == "__main__":
    main()
