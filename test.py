from sandbox.executor import execute_code

result = execute_code("print('Hello from sandbox')")
print (result)

result = execute_code("print(1/0)")

print (result)