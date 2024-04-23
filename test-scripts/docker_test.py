import docker
client = docker.from_env()
r = client.containers.run("alpine", ["echo", "hello", "world"])
print(str(r, encoding='utf-8'))