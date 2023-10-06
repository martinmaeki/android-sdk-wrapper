import os
import re
from enum import Enum
from properties import git_path, sdk_path as sdk_folder

class PackagePattern(Enum):
    BUILD_TOOLS = re.compile("^\s*build-tools;")

    def matches(self, line):
        return self.value.match(line)
    

class Command():
    def validate(self, args, arg_count) -> bool:
        return (False, '')


    def execute(self, args, arg_count) -> bool:
        return True


class ShellCommand(Command):
    def execute_shell(self, command):
        #print('[+] Running shell command:')
        #print('[+] {}'.format(command))
        #print('')
        output = os.popen(command).read()
        return output


class SdkManagerCommand(ShellCommand):
    sdk_path = sdk_folder

    def execute_sdkmanager(self, arg_line: str):
        return self.execute_shell('{}sdkmanager.bat {}'.format(self.sdk_path, arg_line))


    def execute_list(self, package_pattern: PackagePattern):
        output = self.execute_sdkmanager('--list')
        output_lines = output.split('\n')
        available_packages_started = False
        available_packages_tag = 'Available Packages'
        available_packages = []
        installed_packages_started = False
        installed_packages_tag = 'Installed packages'
        installed_packages = []
        for line in output_lines:
            if not installed_packages_started and line.find(installed_packages_tag) != -1:
                available_packages_started = False
                installed_packages_started = True
                continue
            if not available_packages_started and line.find(available_packages_tag) != -1:
                installed_packages_started = False
                available_packages_started = True
                continue
            if package_pattern.matches(line):
                line = line.strip()
                if installed_packages_started:
                    installed_packages.append(line)
                elif available_packages_started:
                    available_packages.append(line)
        
        print('[+] Available Packages')
        for (index, package) in enumerate(available_packages):
            print('[{}]\t{}'.format(index + 1, package))
        print('[?] You can install with buildtools -i <index>')
        print('')
        print('')
        print('')

        print('[+] Installed Packages')
        for (index, package) in enumerate(installed_packages):
            print('[{}]\t{}'.format(index + 1, package))
        print('[?] You can uninstall with buildtools -u <index>')
        print('')
        print('')
        print('')
        return (available_packages, installed_packages)


    def execute_sdkmanager_install(self, package):
        # TODO: platform check
        # Win -> echo y | sdkmanager.bat --install package
        print('[+] Installing package: {}'.format(package))
        output = self.execute_shell('echo y | {}sdkmanager.bat --install {}'.format(self.sdk_path, package))
        if output.find('license is not accepted') != -1:
            print('[-] Accept licenses with command licenses')
        elif output.find('100% Computing updates') != -1: # If package was updated?
            print('[+] Package updated: {}'.format(package))
        else:
            print('[+] Package installed: {}'.format(package))


    def execute_sdkmanager_uninstall(self, package):
        print('[+] Uninstalling package: {}'.format(package))
        output = self.execute_sdkmanager('--uninstall {}'.format(package))
        if output.find('Unable to find package') != -1:
            print('[-] Could not find package')
        else:
            print('[+] Package uninstalled: {}'.format(package))


class Licenses(SdkManagerCommand):
    def validate(self, args, arg_count) -> bool:
        return (True, '')
    

    def execute(self, args, arg_count) -> bool:
        accept = input('[+] Do you want to accept licenses? y/n: ')
        if accept.lower() == 'y':
            # TODO: platform check
            # Win -> give path to Git's root folder
            yes_command = '{}\\usr\\bin\\yes.exe'.format(git_path)
            output = self.execute_shell('{} | {}sdkmanager.bat --licenses'.format(yes_command, self.sdk_path))
            print(output)
        else:
            print('[+] Licenses are not accepted')
        return True


class BuildTools(SdkManagerCommand):
    available_packages = []
    installed_packages = []
    usage = 'Usage: buildtools or buildtools -i|-u <package index>'

    def validate(self, args, arg_count):
        # Args count
        if arg_count == 1 or arg_count >= 3:
            return (False, self.usage)
        # Flags and package index
        if arg_count == 2:
            flag = args[0]                      # -i (Install) | -u (Uninstall)
            package_index = int(args[1]) - 1    # integer which is a index for packages array
            if flag != '-i' and flag != '-u':
                return (False, 'Unkown flag')
            if flag == '-i' and (package_index < 0 or len(self.available_packages) <= package_index):
                return (False, 'Package index out of bounds')
            if flag == '-u' and (package_index < 0 or len(self.installed_packages) <= package_index):
                return (False, 'Package index out of bounds')
        return (True, '')


    def execute(self, args, arg_count) -> bool:
        if arg_count == 0:
            available_packages, installed_packages = self.execute_list(PackagePattern.BUILD_TOOLS)
            self.available_packages = available_packages
            self.installed_packages = installed_packages
        elif arg_count == 2:
            flag = args[0]                      # -i (Install) | -u (Uninstall)
            package_index = int(args[1]) - 1    # integer which is a index for build_tools array
            if flag == '-i':
                package: str = self.available_packages[package_index]
                package = package.strip().split(' ', 1)[0]
                
                self.execute_sdkmanager_install(package)
            else: # flag == '-u'
                package: str = self.installed_packages[package_index]
                package = package.strip().split(' ', 1)[0]
                self.execute_sdkmanager_uninstall(package)
        return True
