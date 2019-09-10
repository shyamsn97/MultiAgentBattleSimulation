# MultiAgentArmySim

## Multi agent reinforcement learning environment where teams of agents, each with a neural network, work together to defeat the other teams in an all out battle.

#### Installation:
	python setup.py install

#### How to use:
	usage: run_server.py [-h] [--grid_size GRID_SIZE] [--num_agents NUM_AGENTS]
                     [--num_teams NUM_TEAMS] [--num_episodes NUM_EPISODES]
                     [--episode_length EPISODE_LENGTH]
                     [--saved_model_path SAVED_MODEL_PATH] [--train_model]
                     port

	Multi agent battle simulation

	positional arguments:
		port                  enter a valid port for the server to listen to

	optional arguments:
  		-h, --help            show this help message and exit
  		--grid_size GRID_SIZE 
				grid size (must be an integer)
  		--num_agents NUM_AGENTS
                        	number of agents in each team
  		--num_teams NUM_TEAMS
                        	number of teams
  		--num_episodes NUM_EPISODES
                	        number of episodes
  		--episode_length EPISODE_LENGTH
                	        length of each episode
  		--saved_model_path SAVED_MODEL_PATH
                	        path to pretrained neural network
  		--train_model         boolean
				train model
	
	# Example with grid size 100, 200 agents on each team, 1 episode with length 100, and a pretrained neural network model. Agents use REINFORCE to train the model
	python run_server.py 8888 --grid_size 100 --num_agents 200 --num_teams 2 --num_episodes 1 --episode_length 100 --saved_model_path src/saved_models/test_model.pth
	# then go to localhost:8888 to see the agents duke it out!

![](images/demo.png)
