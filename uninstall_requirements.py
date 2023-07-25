import subprocess

def uninstall_packages(filename):
    with open(filename, 'r') as file:
        packages = file.readlines()
        packages = [package.strip() for package in packages]
        for package in packages:
            uninstall_command = f'pip uninstall -y {package}'
            subprocess.run(uninstall_command, shell=True)

if __name__ == '__main__':
    requirements_file = 'requirements.txt'  # Replace with the path to your requirements.txt file
    uninstall_packages(requirements_file)
