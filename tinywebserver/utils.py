from time import strftime, localtime
from os import getcwd, listdir, path, execl, lstat, walk
from sys import argv
from time import sleep
from threading import Thread

class Utils:
    def __init__(self):
        pass

    def log(self, text):
        todaystr = strftime("%Y-%m-%d %H:%M:%S", localtime())
        print(todaystr + "\t" + text)

    def get_running_script(self):
        return path.abspath(path.dirname(argv[0])) + "/" + argv[0].split("/")[-1]

    def restart_server(self):
        self.log("Restarting server...")
        execl(self.get_running_script(), "")

    def get_watched_files(self, directory):
        watched_files = {}

        for root, dirnames, filenames in walk(directory):
            for filename in filenames + dirnames:
                watched_files[path.join(root, filename)] = lstat(path.join(root, filename)).st_mtime

        return watched_files

    def watch_start(self, directory):
        watchThread = Thread(target=self.watch, args=([directory]))
        watchThread.daemon = True
        watchThread.start()

    def watch(self, directory):
        watched = self.get_watched_files(directory)

        while True:
            watched_fresh = self.get_watched_files(directory)

            # check if files have been added or removed
            if len(watched) != len(watched_fresh):
                watched = watched_fresh
                self.restart_server()

            for watched_file in watched:
                # fixes bug after file is being moved to other dir
                if watched_file in watched and watched_file in watched_fresh:
                    # check if files have been updated
                    if watched_fresh[watched_file] != watched[watched_file]:
                        watched = watched_fresh
                        self.restart_server()
                else:
                    watched = watched_fresh
                    self.restart_server()

            sleep(1)
