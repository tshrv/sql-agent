import os
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIChatModel(
    model_name='qwen3.5:2b',
    provider=OpenAIProvider(
        base_url="http://172.29.192.1:11434/v1",
        api_key="ollama-dummy-key"
    )
)

# Create a basic agent using Llama3:8b via Ollama
agent = Agent(
    model=model,
    instructions="use tools as and when needed",
    system_prompt='You are a concise, helpful AI assistant built with pydantic-ai and FastAPI.',
)


@agent.tool_plain
def get_current_time():
    """Get the current time."""
    from datetime import datetime
    time = datetime.now().isoformat()
    print(time)
    return time
