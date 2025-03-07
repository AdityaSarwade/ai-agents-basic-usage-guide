from autogen import UserProxyAgent, AssistantAgent

llm_config = {
    "model": "REDACTED",
    "api_key": "REDACTED",
    "base_url": "REDACTED",
    "api_type": "REDACTED",
    "api_version": "REDACTED",
}

assistant = AssistantAgent("Assistant", llm_config=llm_config)
user_proxy = UserProxyAgent("user_proxy", code_execution_config=False)

user_proxy.initiate_chat(assistant, message="Hey!")
