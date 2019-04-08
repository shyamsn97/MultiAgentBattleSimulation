import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line

from game import Game

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    connections = set()
    a = [0,1,1,2,3,4]
    def open(self):
        self.connections.add(self)
        game = Game(200,num_agents=5)
        frames = game.playEpisodes(200)
       #  map = [
       #   [ 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
       #   [ 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
       #   [ 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
       #   [ 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
       #   [ 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
       #   [ 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
       #   [ 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0 ],
       #   [ 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0 ],
       #   [ 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0 ],
       #   [ 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0 ],
       #   [ 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0 ],
       #   [ 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0 ],
       #   [ 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0 ],
       #   [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
       #   [ 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
       #   [ 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
       # ]
        [client.write_message({"user":"SS","message":frames}) for client in self.connections]

    def on_message(self, message):
    	print("Received {}".format(message))
    	[client.write_message({"user":"SS","message":"POOP"}) for client in self.connections]

    @classmethod
    def send_message(cls):
    	[client.write_message({"user":"NO","message":cls.a}) for client in cls.connections]
    	# cls.a += 1

    def on_close(self):
        self.connections.remove(self)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", SimpleWebSocket)
    ])

if __name__ == "__main__":
	print("Starting Server...")
	try:
		app = make_app()
		app.listen(8000)
		METER_CHECK_INTERVAL = 1000  # ms
		# tornado.ioloop.PeriodicCallback(SimpleWebSocket.send_message,METER_CHECK_INTERVAL).start()
		tornado.ioloop.IOLoop.instance().start()

	except (SystemExit, KeyboardInterrupt):
		print("Client closed")
