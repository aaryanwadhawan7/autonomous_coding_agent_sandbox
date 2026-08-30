import os
from groq import Groq
import asyncio
import json
from sandbox.executor import execute_code
from dotenv import load_dotenv
load_dotenv()
import functools

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

# Start conversation with system prompt + user request
# Call Groq with tools registered
# If LLM's returns text -> it's done, return it
# If LLM returns the tool call -> execute the sandbox, feed result back
# Repeat from step 2 (max 5 iterations)

# Iterable Object 
tools = [
    {
        'type': 'function',
        'function': {
            'name': 'execute_code',
            'description': 'Executes Python code in an isolated Sandbox. Return stdout, stderr and exit code',
            'parameters': {
                'type': 'object',
                'properties': {
                    'code': {
                        'type': 'string',
                        'description': 'Raw Python Code to execute'
                    }
                },
                'required': ['code']
            }
        }
    }
]

SYSTEM_PROMPT = """You are an autonomous coding agent.
You write Python code to solve the user's request.
You MUST test your code using the execute_code tool.
If the code fails, fix it and test again.
Only stop when the code runs successfully (exit_code == 0).
Never return unexecuted code.
IMPORTANT: Only use Python standard library. 
No pip installs. No numpy, pandas, or external packages."""

async def auto_agent (user_request: str) -> dict:
    try:
        messages = [
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': user_request
            },
        ]

        max_iteration = 5
        initial_iteration = 0

        while (initial_iteration < max_iteration):
            initial_iteration += 1

            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                functools.partial(
                    client.chat.completions.create,
                    messages=messages,
                    model='qwen/qwen3.8-27b',
                    tools=tools,
                    tool_choice='auto'
            )
)
            message = response.choices[0].message
            messages.append(message)

            if message.tool_calls:
                for tool_call in message.tool_calls:
                    # tool_call is executing
                    args = json.loads(tool_call.function.arguments)
                    code = args.get('code')

                    # run sandbox in thread (blocking call -> sync safe)
                    result = await asyncio.get_running_loop().run_in_executor(
                        None, execute_code, code
                    )

                    print(f"Sandbox result: {result}") 

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": "execute_code",
                        "content": json.dumps(result)
                    })
            else:
                return {
                    "result": message.content,
                    "iterations": initial_iteration
                }
        return {
            'result': 'Maximum iteration reached without success!',
            'iterations': initial_iteration
        }
    except Exception as err:
        return {
            'stdout': '',
            'stderr': str(err),
            'exit_code': -1
        }
