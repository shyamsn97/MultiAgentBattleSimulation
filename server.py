import webbrowser, os
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line
import ast

from game import Game

static_root = os.path.join(os.path.dirname(__file__), 'static')
#port = 8000
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    def initialize(self,game):
        self.game = game
    connections = set()
    frames = []
    agents = []
    agent_counts = []
    team_counts = []
    num_teams = 0
    def open(self):
        self.connections.add(self)
        print("Preparing UI...")
        if len(self.frames) == 0:
            frames, framestr, agent_counts,team_counts, agents = self.game.playEpisodes()
            self.num_teams = self.game.getNumTeams()
            self.frames = frames
            self.agents = agents
            self.agent_counts = agent_counts
            self.team_counts = team_counts
        messageDict = {"user":"MultiAgentArmy",
                        "job":"setup",
                        "frames":self.frames,
                        "num_teams":self.num_teams, 
                        "agents":self.agents,
                        "agent_counts":self.agent_counts,
                        "team_counts":self.team_counts}
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

def make_app(game):
    return tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_root}),
        (r"/", MainHandler),
        (r"/websocket", SimpleWebSocket, {'game':game})
    ])


def start_server(args):
    print("TRAIN",args.train_model)
    game = Game(size = args.grid_size, 
                num_agents = args.num_agents, num_teams = args.num_teams,
                num_episodes = args.num_episodes, episode_length = args.episode_length, saved_model_path=args.saved_model_path,train=args.train_model)
    port = args.port
    try:
        app = make_app(game)
        app.listen(port)
        print("Starting Server... go to localhost:{}".format(port))
        METER_CHECK_INTERVAL = 1000  #ms
        # periodic sending
        tornado.ioloop.PeriodicCallback(SimpleWebSocket.send_message,METER_CHECK_INTERVAL).start()
        tornado.ioloop.IOLoop.instance().start()
    except (SystemExit, KeyboardInterrupt):
        print("Client closed")

if __name__ == "__main__":
  print("Starting Server... go to localhost:{}".format(8888))
  params = {"grid_size":100, "num_agents":200,"num_teams":2,"num_episodes":20}
  try:
    app = make_app(params)
    app.listen(8888)
    METER_CHECK_INTERVAL = 1000  #ms
    # periodic sending
    tornado.ioloop.PeriodicCallback(SimpleWebSocket.send_message,METER_CHECK_INTERVAL).start()
    tornado.ioloop.IOLoop.instance().start()
  except (SystemExit, KeyboardInterrupt):
    print("Client closed")

