from subprocess import check_output, CalledProcessError
from shlex import split
import os
import sys
import re


def run(command, allow_fail=False):
    print(command)
    try:
        output = check_output(split(command))
        print(output.decode())
    except CalledProcessError as e:
        if not allow_fail:
            raise e


def get_packages_path():
    try:
        _clear_local_directory_from_path()
        import createserial
        p = os.path.dirname(os.path.dirname(createserial.__file__))
        print("Found existing installation...", p)
        return p
    except ImportError:
        for p in sys.path:
            if re.match(r'(/\w*)*python3\.\d+/\w+-packages', p):
                print("Found packages directory...", p)
                return p
    raise FileNotFoundError("Could not find system python packages directory")


def _clear_local_directory_from_path():
    cwd = os.getcwd()
    sys.path = [p for p in sys.path if p != cwd]


def check_if_root():
    try:
        run("sudo echo Testing for root access...")
    except CalledProcessError:
        raise PermissionError("Please run as root")


def verify_install():
    _clear_local_directory_from_path()
    try:
        import createserial
        print("Successfully found createserial!")
    except ImportError:
        raise ImportError("Failed to find the createserial library installed on the system")


def main():
    check_if_root()
    packages_path = get_packages_path()
    run(f"sudo rm -r {os.path.join(packages_path, 'createserial')}", allow_fail=True)
    run(f"sudo cp -r {os.path.join(os.getcwd(), 'createserial')} {packages_path}")
    verify_install()


if __name__ == '__main__':
    main()
