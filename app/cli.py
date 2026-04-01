from app.agents.agent import Dependencies, DatabaseClient, agent as sql_agent
# from app.agents.user_finder_agent import Dependencies, DatabaseClient, agent as user_finder_agent

db_client = DatabaseClient()
deps = Dependencies(db_client=db_client)

# agent = user_finder_agent
agent = sql_agent

result = agent.run_sync(
    # "Find me details on username 'tushar'",
    # "Which tables do we have in the database?",
    # "Who is employee id 10001?",
    # "What is the age difference between employees with id 10001 and 10002?",
    # "Get me employee count in every department",
    "How many employees work in more than one department?",
    deps=deps
)

print(result.output)

