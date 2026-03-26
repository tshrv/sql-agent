from fastapi import FastAPI
from pydantic import BaseModel
from app.agents import agent, Dependencies
from app.settings import settings
from app.db import DatabaseClient

app = FastAPI(
    title="FastAPI Template",
    description="A basic FastAPI template with a built-in AI Agent",
    version="1.0.0"
)
dbc = DatabaseClient(settings)

# Request model for our chat endpoint
class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test-db")
async def test_db():
    count = await dbc.execute_query("SELECT count(*) FROM employees.employee")
    return {"message": "Database connection successful", "employee_count": count}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Send a prompt to the AI agent and get a response.
    The agent is configured to use Llama3:8b via Ollama.
    """
    try:
        deps = Dependencies(settings=settings, db_client=DatabaseClient(settings))
        # Run the agent asynchronously
        result = await agent.run(request.prompt, deps=deps)
        return {"response": result.data}
    except Exception as e:
        return {
            "error": str(e), 
            "message": "Make sure Ollama is running with the llama3:8b model!"
        }
