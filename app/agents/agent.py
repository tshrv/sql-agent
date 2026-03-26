from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel

from app.settings import settings, Settings
from app.db import DatabaseClient


class Dependencies(BaseModel):
    settings: Settings
    db_client: DatabaseClient

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
async def run_sql(ctx: RunContext[Dependencies], query: str) -> list[dict]:
    """Run a SQL query on the database."""
    result = await ctx.deps.db_client.execute_query(query)
    print(f"Query result: {result}")
    return result

@agent.tool_plain
def get_current_time():
    """Get the current time."""
    from datetime import datetime
    time = datetime.now().isoformat()
    print(time)
    return time
