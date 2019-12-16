import argparse
import os
import subprocess

parser = argparse.ArgumentParser()

parser.add_argument('--folder', type=str, help='The location of the PyPSOM folder. If not passed assumes it is on it')
parser.add_argument('--command', type=str, help='The location of the PyPSOM folder. If not passed assumes it is on it')
args = parser.parse_args()

if __name__ == "__main__":

    folder = args.folder if args.folder != None else os.getcwd()
    docker_cmd = args.command

    if docker_cmd.split(' ')[0] not in ["compile.sh", "configure.sh", "clean.sh"]:
        command_docker = f'docker run -v {folder}/model:/usr/temp/pypsom hmalmeida/pypsom:0.63.0 -c "{docker_cmd}"'
    else:
        command_docker = f'docker run -v {folder}/model:/usr/temp/pypsom hmalmeida/pypsom:0.63.0 tools/{docker_cmd}'
    print(docker_cmd)
    ## For degub, delete print after finished
    
    print("########################################", command_docker, "########################################", sep = '\n')
    subprocess.call(command_docker, shell = True)