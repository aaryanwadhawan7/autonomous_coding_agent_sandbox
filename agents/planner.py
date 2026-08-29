import os 
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))


def plan(user_request: str) -> str:
    try:
        response = client.chat.completions.create(
            messages = [
                {
                    'role': 'system',
                    'content': 'You are a planning agent. Given the user request describe clearly what python code to be written to solve it. Be specific and concise. Return only the task description.'
                },
                {
                    'role': 'user',
                    'content': user_request
                }
            ],
            model = 'qwen/qwen3.8-27b'
        )
        return response.choices[0].message.content
    except Exception as err:
        return {
            'stdout': "",
            'stderr': str(err),
            'exit_code': -1
        }
