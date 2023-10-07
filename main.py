import cmd # https://pymotw.com/2/cmd/#shelling-out
from commands import All, BuildTools, Command, Licenses


class AndroidSdkWrapper(cmd.Cmd):
    all = All()
    build_tools = BuildTools()
    licenses = Licenses()

    # Helpers
    def parse_args(self, args_line: str):
        args = args_line.split(' ')
        args = [] if len(args[0]) == 0 else args
        arg_count = len(args)
        return (args, arg_count)


    def run_command(self, command: Command, args_line: str):
        args, arg_count = self.parse_args(args_line)
        valid, error_msg = command.validate(args, arg_count)
        if valid:
            command.execute(args, arg_count)
        else:
            print('[-] {}'.format(error_msg))


    # Commands
    def do_init(self, args_line: str):
        'Download Android SDK command line tools'
        print('Not implemented yet')


    def do_all(self, args_line: str):
        'List all installed and available packages'
        self.run_command(self.all, args_line)


    def do_buildtools(self, args_line: str):
        'List all installed and available build-tools'
        self.run_command(self.build_tools, args_line)


    def do_licenses(self, args_line: str):
        'Accept licenses'
        self.run_command(self.licenses, args_line)


    def do_destroy(self, line):
        'Remove SDK'
        print('Not implemented yet')


    def do_exit(self, line):
        return True


if __name__ == '__main__':
    # TODO: check JAVA_HOME or java --version
    AndroidSdkWrapper().cmdloop()