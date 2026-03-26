from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel
from app.settings import settings


@dataclass
class UserInfo:
    name: str
    age: int
    location: str


class DatabaseClient:
    USER_DATA = {
        "tushar": {
            "name": "Tushar",
            "age": 30,
            "location": "New York"
        },
        "alice": {
            "name": "Alice",
            "age": 25,
            "location": "San Francisco"
        }
    }
    def get_user_info(self, username: str) -> UserInfo | None:
        user_data = self.USER_DATA.get(username)
        if user_data:
            return UserInfo(**user_data)
        return None


class Dependencies(BaseModel):
    db_client: 'DatabaseClient'

    model_config = {
        "arbitrary_types_allowed": True
    }


model = OpenAIChatModel(
    model_name=settings.llm_model,
    provider=OpenAIProvider(
        base_url=settings.llm_api_base_url,
        api_key=settings.llm_api_key
    )
)


agent = Agent[Dependencies](
    model=model,
    instructions="use tools as and when needed",
    system_prompt='You are a concise, helpful AI assistant built with pydantic-ai and FastAPI.',
    deps_type=Dependencies
)


@agent.tool
def get_user_info(ctx: RunContext[Dependencies], username: str) -> UserInfo | None:
    """Get user information by username."""
    user_info = ctx.deps.db_client.get_user_info(username)
    if user_info:
        print(f"User info for {username}: {user_info}")
        return user_info
    else:
        print(f"No user found with username: {username}")
        return None

@agent.tool_plain
def get_current_time():
    """Get the current time."""
    from datetime import datetime
    time = datetime.now().isoformat()
    print(time)
    return time
