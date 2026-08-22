import os 
from groq import Groq


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
            model = 'llama-3.3-70b-versatile'
        )
        return response.choices[0].message.content
    except Exception as err:
        return {
            'stdout': "",
            'stderr': str(err),
            'exit_code': -1
        }
