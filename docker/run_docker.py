
import argparse
import os
import subprocess
import docker

parser = argparse.ArgumentParser()

parser.add_argument('--folder', type=str, help='The location of the PyPSOM folder. If not passed assumes it is on it')
parser.add_argument('--command', type=str, help='The location of the PyPSOM folder. If not passed assumes it is on it')
args = parser.parse_args()

client = docker.from_env()

if __name__ == "__main__":

    folder = args.folder if args.folder != None else os.getcwd()
    volumes = {os.path.join(folder, 'model'): {'bind': '/usr/tmp/pypsom', 'mode': 'rw'}}
    docker_cmd = args.command

    if docker_cmd.split(' ')[0] not in ["compile.sh", "configure.sh", "clean.sh"]:
        command_docker = f'-c "{docker_cmd}"'
    else:
        command_docker = f'tools/{docker_cmd}'
    
    output = client.containers.run('hmalmeida/pypsom:0.63.0', command_docker, volumes = volumes, remove = True)

    print(output.decode('UTF-8').strip())