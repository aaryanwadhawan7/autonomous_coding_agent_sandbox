import os
from groq import Groq

client = Groq(api_key = os.environ.get('GROQ_API_KEY'))

def code(task_desc: str) -> str:
    try:
        response = client.chat.completions.create(
            messages= [
                {
                    'role' : 'system',
                    'content' : 'You are a coding agent. Given a task description return ONLY  the python code, no markdown, no backticks, no explaination. Just raw python code. '
                },
                {
                    'role' : 'user',
                    'content' : task_desc
                }
            ],
            model='llama-3.3-70b-versatile'
        )
        return response.choices[0].message.content
    except Exception as err:
        return {
            'stdout': "",
            'stderr': str(err),
            'exit_code': -1
        }