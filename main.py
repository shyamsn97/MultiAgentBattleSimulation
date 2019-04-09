import webbrowser, os
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line
import ast

from game import Game

port = 8000
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    connections = set()
    a = [1,2,3]
    def open(self):
        self.connections.add(self)
        game = Game(150,num_agents=100,num_teams=3)
        frames = game.playEpisodes(200)
        print("Preparing UI...")
        messageDict = {"user":"MultiAgentArmy",
                        "job":"setup","frames":frames,
                        "num_teams":game.getNumTeams(), 
                        "agents":game.serializeAgents()}
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
        (r"/", MainHandler),
        (r"/websocket", SimpleWebSocket)
    ])

if __name__ == "__main__":
  print("Starting Server... go to localhost:{}".format(port))
  # webbrowser.open('file://' + os.path.realpath("index.html"))
  try:
    app = make_app()
    app.listen(port)
    METER_CHECK_INTERVAL = 1000  # ms
    # periodic sending
    tornado.ioloop.PeriodicCallback(SimpleWebSocket.send_message,METER_CHECK_INTERVAL).start()
    tornado.ioloop.IOLoop.instance().start()
  except (SystemExit, KeyboardInterrupt):
    print("Client closed")

