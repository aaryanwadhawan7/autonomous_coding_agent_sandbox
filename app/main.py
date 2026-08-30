from fastapi import FastAPI
from pydantic import BaseModel
from sandbox.executor import execute_code
import asyncio
from agents.orchestrator import auto_agent
import sys 

if sys.platform == 'win32':
    loop = asyncio.SelectorEventLoop()
    asyncio.set_event_loop(loop)

app = FastAPI()

@app.get('/')
def healthCheck():
    return {'message': "FastAPI Backend is running successfully!"}

class CodeRequest(BaseModel):
    code: str

@app.post('/execute')
async def execute(coderequest: CodeRequest):
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, execute_code, coderequest.code)
        return result
    except Exception as err:
        return {
            'stdout': "",
            'stderr': str(err),
            'exit_code': -1
        }
        
@app.post('/run-agent')
async def run_agent (request: CodeRequest):
    result = await auto_agent(request.code)
    return result