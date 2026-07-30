import requests


def process_single_text(
    system_prompt: str,
    user_text: str,
    chat_id: str = "1",
    endpoint: str = "http://localhost:8081/ai/chat"
) -> str:
    """
    处理单个文本内容，调用本地 LLM 进行优化。
    
    参数:
        system_prompt: 系统提示词
        user_text: 用户输入的文本内容
        chat_id: 对话ID，默认为 "1"
        endpoint: LLM 接口地址，默认为 "http://localhost:8081/ai/chat"
    
    返回:
        处理后的文本内容（字符串）
    
    异常:
        如果请求失败，会抛出 requests.HTTPError
    """
    # 组合系统提示词和用户文本内容
    prompt = system_prompt + f"\n{user_text}"
    
    # 准备请求参数
    params = {
        "prompt": prompt,
        "chatId": chat_id
    }
    
    # 发送 POST 请求
    resp = requests.post(endpoint, data=params, timeout=60)
    resp.raise_for_status()
    
    # 返回处理后的结果
    return resp.text.strip()


if __name__ == "__main__":
    # 测试示例
    from prompt import 自动记笔记提示词
    
    system_prompt = 自动记笔记提示词
    user_text = "这是一段测试文本内容，用于验证函数是否正常工作。"
    result = process_single_text(system_prompt, user_text)
    print("处理结果：")
    print(result)




