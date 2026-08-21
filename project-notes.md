- Started with project structure. Sandbox dir will require the seperate dockerfile!

- dockerfile (blueprint), container(spun up fresh everytime), volume mount (done at runtime, not in dockerfile)
 
- sandbox/executor.py
  - exectur.py: it has a function which takes code: str as a parameter, creates a new dir temp, add this code in ./temp/code.py, it tells docker to run the container but make this temp dir as part of ./app (mounting), run: python /app/code.py, runs container and executes code.py, executer.py captures output and container dies.

  - There are three ways we can do this:
    1) Terminal
    docker exec -it <container_name> sh -c "echo 'print("wrinting code directly inside the container!)' > /path/to/script.py"

    2)  Inside a python script (BEST FOR AUTOMATION)

    3) Mounting local file via docker or compose 

- Write the simple POST request /execute => this run the code_execute() function

    