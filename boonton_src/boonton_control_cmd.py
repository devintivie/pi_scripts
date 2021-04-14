import cmd
from boonton_manager import boonton_manager

class boonton_control_cmd(cmd.Cmd):
    """Simple command processor example."""
    def __init__(self, boonton_manager):
        super(boonton_control_cmd, self).__init__()
        self.reply_str = ''
        self.reply_str_text = ''
        self.reply_str_data = ''
        self.verbose = None
        self.boonton_control = boonton_manager

    def precmd(self, line):
        line = line.lower()
        self.reply_str = f'[{line.strip()}]\n'
        self.reply_str_data = ''
        return line
    
    def postcmd(self, stop, line):
        self.reply_str += '\f'
        return None #self.reply_str

    def emptyline(self):
        pass


    # def reply(self, string='', end='\n'):
    #     self.reply_str_text += string + end
    #     if self.verbose:
    #         print(string, end=end)
    
    # def reply_data(self, string=''):
    #     self.reply_str_data += string

    # def do_test(self, arg):
    #     self.reply('0123456')
    #     self.reply_data('ABCDEF')

    def do_verbose(self, args):
        print(type(args))
        print(args)
        if args == 'true':
            self.verbose = True
        else:
            self.verbose = False


    def do_startup(self, none_arg):
        self.boonton_control.startup()

    
    def do_bye(self, line):
        return self.do_EOF(line)

    def do_EOF(self, line):
        return True
    
    def postloop(self):
        print("goodbye world")

