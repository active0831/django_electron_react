import time, sys, subprocess

class Run():
    def __init__(self,parent_pid):
        self.runserver = None
        self.parent_pid = parent_pid

    def start(self):
        self.runserver = subprocess.Popen(
            ["./backend/.venv/Scripts/python.exe",
             "./runserver.py",
             str(self.parent_pid)])

        while True:
            time.sleep(100000)

if __name__=="__main__":
    Run(parent_pid = int(sys.argv[1])).start()