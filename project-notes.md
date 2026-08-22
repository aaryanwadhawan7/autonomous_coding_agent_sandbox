- Started with project structure. Sandbox dir will require the seperate dockerfile!

- dockerfile (blueprint), container(spun up fresh everytime), volume mount (done at runtime, not in dockerfile)
 
- sandbox/executor.py
  - exectur.py: it has a function which takes code: str as a parameter, creates a new dir temp, add this code in ./temp/code.py, it tells docker to run the container but make this temp dir as part of ./app (mounting), run: python /app/code.py, runs container and executes code.py, executer.py captures output and container dies.

  - There are three ways we can do this:
    1) Terminal
    docker exec -it <container_name> sh -c "echo 'print("wrinting code directly inside the container!)' > /path/to/script.py"

    2)  Inside a python script (BEST FOR AUTOMATION)

    3) Mounting local file via docker or compose 

- For environment setup: NEW ENV => python -m env sandboxEnv, source sandboxEnv/bin/activate (Linux / MacOS), sandboxEnv/Scripts/activate.ps1 (Powershell : Windows)

- Write the simple POST request /execute => this run the code_execute() function
- you need platform check at the code_execute() function cause it shows conflict with docker
- you need to import asyncio library to handle async requests

- github : To check the commit in ASCII graph run => git log --graph --all 

- Checklist
  - Sandbox (executor.py + Dockerfile + FastAPI endpoint) [DONE]
  - Planner Agent     => breaks user request into steps
  - Coder Agent       => writes the code
  - Debugger Agent    => reads error, decides fix or done
  - Orchestrator      => runs the loop: code -> execute -> debug ->  retry
  - Final endpoint    - POST /run-agent that ties it all together

  