import os
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def debugger(code: str, error: str) -> str:
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a debugging agent. You will recieve Python code and an error message. Fix this code and return ONLY the corrected Python code. No explanation, no markdown, no backticks. Just raw Python code.'
                },
                {
                    'role': 'user',
                    'content': f"Code:\n{code}\n\nError:\n{error}"
                }
            ],
            model= 'llama-3.3-70b-versatile'
        )
        return response.choices[0].message.content
    except Exception as err:
        return {
            'stdout': "",
            'stderr': str(err),
            'exit_code': -1
        }