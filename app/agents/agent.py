from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel

import logfire

from app.settings import settings
from app.db import DatabaseClient


logfire.configure()
logfire.instrument_pydantic_ai()

class Dependencies(BaseModel):
    db_client: DatabaseClient

    model_config = {
        "arbitrary_types_allowed": True
    }


model = OpenAIResponsesModel(
    model_name=settings.llm_model,
    provider=OpenAIProvider(
        base_url=settings.llm_api_base_url,
        api_key=settings.llm_api_key
    )
)


agent = Agent[Dependencies](
    model=model,
    instructions="You are a data assistant who has access to a PostgreSQL database. Use the tools as needed. When you are building SELECT queries, if the table_schema is not `public`, make sure to include the table_schema name as prefix for table_name in the query.",
    deps_type=Dependencies
)


@agent.tool
async def run_sql(ctx: RunContext[Dependencies], query: str) -> list[dict]:
    """Run a SQL query on the database."""
    result = await ctx.deps.db_client.execute_query(query)
    print(f"Query result: {result}")
    return result

@agent.tool
async def list_tables(ctx: RunContext[Dependencies]) -> list[dict]:
    """List all tables in the database"""
    query = (
        "SELECT table_schema, table_name FROM information_schema.tables "
        "WHERE table_type = 'BASE TABLE' and table_schema not in ('information_schema', 'pg_catalog')"
        "ORDER BY table_schema, table_name;"
    )
    result = await ctx.deps.db_client.execute_query(query)
    print(f"Query result: {result}")
    return result

@agent.tool
async def get_table_schema(ctx: RunContext[Dependencies], table_name: str) -> list[dict]:
    """Get the schema for a specific table"""
    query = (
        "SELECT table_schema, table_name, column_name, data_type, is_nullable, column_default "
        "FROM information_schema.columns "
        f"WHERE table_schema = 'employees' and table_name = '{table_name}' "
        "ORDER BY table_schema, table_name, ordinal_position;"
    )
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
