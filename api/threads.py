from threading import Thread, Lock


class Threads:
    lock = Lock()

    def thread_func(self, *args):
        Threads.lock.acquire()
        self.func(*args)
        Threads.lock.release()

    def __init__(self, target, args):
        self.func = target
        self.thread = Thread(target=self.thread_func, args=args)

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()