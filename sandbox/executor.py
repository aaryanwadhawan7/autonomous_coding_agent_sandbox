import docker
import tempfile
import os 
import platform


# client = docker.from_env()
# This stops the Docker client from having it's connection reset by Windows
def get_client ():
    return docker.from_env()

def execute_code(code: str) -> dict:
    try:
        client = get_client()
        # created a temp dir 
        with tempfile.TemporaryDirectory() as tmpdir:
            # create the appended code.py in temp dir
            code_file = os.path.join(tmpdir, 'code.py')
            with open(code_file, 'w') as f:
                f.write(code)

            if platform.system() == 'Windows':
                tmpdir_docker = tmpdir.replace('\\','/').replace('C:','//c')
            else:
                tmpdir_docker = tmpdir

            output = client.containers.run(
                image = "sandbox-executor",
                command = 'python code.py',
                #We are telling docker to mount tmpdir on ur computer
                volumes = {tmpdir_docker: {"bind" : "/app", "mode" : "ro"}}, #ro = "read only",
                mem_limit= "128m", #memory cap
                network_disabled = True, #no internet access
                remove = True, #auto-delete after run
                stdout = True,
                stderr = True
            )

            return {
                "stdout": output.decode('utf-8'),
                "stderr": "",
                "exit_code": 0
            }
    
    except docker.errors.ContainerError as e:
        return {
            "stdout" : "",
            "stderr" : str(e.stderr.decode("utf-8")),
            "exit_code" : 1
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1
        }