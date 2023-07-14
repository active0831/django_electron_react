import time, sys, os, subprocess, signal, psutil

class RunServer():
    def __init__(self,parent_pid):
        self.server = None
        self.parent_pid = parent_pid

    def start(self):
        print("Starting servers")
        self.server = subprocess.Popen(
            ["./backend/.venv/Scripts/python.exe",
             "./backend/manage.py",
             "runserver"])

        while True:
            time.sleep(1)
            if self.parent_pid not in psutil.pids():
                print("Parent process has been closed")
                break

    def __del__(self):
        print("Closing servers")        
        self.server.send_signal(signal.CTRL_C_EVENT)
        self.server.kill()
        print("All servers have been closed")

if __name__=="__main__":
    print("Starting server launcher (parent:", sys.argv[1] +")")
    RunServer(parent_pid = int(sys.argv[1])).start()
