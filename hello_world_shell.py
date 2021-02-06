import cmd
class hello_world(cmd.Cmd):
    """Simple command processor example."""
    
    def do_greet(self, person):
        """greet [person]
        Greet the named person"""
        if person:
            print(f"hi, {person}")
        else:
            print('hi')
    
    def do_bye(self, line):
        return self.do_EOF(line)

    def do_EOF(self, line):
        return True
    
    def postloop(self):
        print("goodbye world")

if __name__ == '__main__':
    hello_world().cmdloop()