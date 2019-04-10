import webbrowser, os
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line
import ast

from game import Game

static_root = os.path.join(os.path.dirname(__file__), 'static')
port = 8000
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    connections = set()
    frames = []
    agents = []
    counts = []
    num_teams = 0
    def open(self):
        self.connections.add(self)
        print("Preparing UI...")
        if len(self.frames) == 0:
            game = Game(150,num_agents=400,num_teams=2)
            frames, framestr, counts, agents = game.playEpisodes(200)
            self.num_teams = game.getNumTeams()
            self.frames = frames
            self.agents = agents
            self.counts = counts
        messageDict = {"user":"MultiAgentArmy",
                        "job":"setup",
                        "frames":self.frames,
                        "num_teams":self.num_teams, 
                        "agents":self.agents,
                        "counts":self.counts}
        [client.write_message(messageDict) for client in self.connections]

    def on_message(self, message):
        message = ast.literal_eval(message)
        job = message["job"]
        if job == "tick":
            print("{}".format(message["message"]))
        elif message["job"] == "send_data":
            [client.write_message({"user":"S","message":"None"}) for client in self.connections]

    @classmethod
    def send_message(cls):
    	[client.write_message({"job":"tick"}) for client in cls.connections]

    def on_close(self):
        self.connections.remove(self)

def make_app():
    return tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_root}),
        (r"/", MainHandler),
        (r"/websocket", SimpleWebSocket)
    ])

if __name__ == "__main__":
  print("Starting Server... go to localhost:{}".format(port))
  try:
    app = make_app()
    app.listen(port)
    METER_CHECK_INTERVAL = 1000  #ms
    # periodic sending
    tornado.ioloop.PeriodicCallback(SimpleWebSocket.send_message,METER_CHECK_INTERVAL).start()
    tornado.ioloop.IOLoop.instance().start()
  except (SystemExit, KeyboardInterrupt):
    print("Client closed")

