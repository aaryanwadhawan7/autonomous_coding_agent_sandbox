import asyncio
from dotenv import load_dotenv
load_dotenv()  # add this
import os
print("API KEY:", os.environ.get('GROQ_API_KEY')[:10])  # verify key loads
from agents.orchestrator import auto_agent

async def test():
    result = await auto_agent("write a hello world function")
    print(result)

asyncio.run(test())