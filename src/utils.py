import subprocess
import time
from pathlib import Path


class Cmd:

    @staticmethod
    def run(command) -> (bool, str):
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, ''


class Docker:

    CHECK_COUNT = 120
    EXE_FILE = '/Applications/Docker.app'
    # EXE_FILE = 'C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe'

    @staticmethod
    def start():
        is_success, _ = Cmd.run(['open', Docker.EXE_FILE])
        # is_success, _ = Cmd.run([Docker.EXE_FILE])
        if not is_success:
            return False

        for i in range(Docker.CHECK_COUNT):
            time.sleep(1)
            if Docker.is_running():
                return True
        else:
            return False

    @staticmethod
    def stop():
        is_success, _ = Cmd.run(['pkill', 'Docker'])
        # is_success, _ = Cmd.run(['taskkill', '/IM', 'Docker Desktop.exe', '/F'])
        if not is_success:
            return False

        for i in range(Docker.CHECK_COUNT):
            time.sleep(1)
            if not Docker.is_running():
                return True
        else:
            return False

    @staticmethod
    def is_running() -> bool:
        is_success, _ = Cmd.run(['docker', 'ps'])
        return is_success

    @staticmethod
    def is_exist_exe() -> bool:
        return Path(Docker.EXE_FILE).exists()

    @staticmethod
    def get_version() -> str:
        _, version = Cmd.run(['docker', 'version', '--format', '{{.Client.Version}}'])
        return version

    @staticmethod
    def get_docker_compose_version() -> str:
        _, version = Cmd.run(["docker", "compose", "version", "--short"])
        return version
