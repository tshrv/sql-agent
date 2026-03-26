from app.agents.user_finder_agent import Dependencies, DatabaseClient, agent as user_finder_agent

db_client = DatabaseClient()
deps = Dependencies(db_client=db_client)

agent = user_finder_agent

result = agent.run_sync(
    "Find me details on username 'tushar'",
    deps=deps
)

print(result.output)