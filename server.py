import argparse
import queue
import threading
from pythonosc import dispatcher as disp
from pythonosc import osc_server


class ServerThread(threading.Thread):
    def __init__(self, address, port):
        self.server_queue = queue.Queue()
        super(ServerThread, self).__init__(target=self.stream_data, kwargs={'address': address, 'port': port})

    def stream_data(self, address, port):
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip",
                            default="127.0.0.1",
                            help="The ip to listen on")
        parser.add_argument("--port",
                            type=int, default=port,
                            help="The port to listen on")
        args = parser.parse_args()
        dispatcher = disp.Dispatcher()
        dispatcher.map(address, queue_put, self.server_queue)
        self.server = osc_server.ThreadingOSCUDPServer(
            (args.ip, args.port), dispatcher)
        print("Serving on {}".format(self.server.server_address))
        self.server.serve_forever()


def queue_put(unused_addr, args, volume):
    try:
        args[0].put(volume)
    except AttributeError:
        print('{0} is not a Queue'.format(args[0]))
