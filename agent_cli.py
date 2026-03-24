from agent import Dependencies, agent, DatabaseClient

db_client = DatabaseClient()
deps = Dependencies(db_client=db_client)

result = agent.run_sync(
    "Find me details on username 'tushar'",
    deps=deps
)

print(result.output)