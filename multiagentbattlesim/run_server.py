import argparse

from multiagentbattlesim.ui import server


def main():
    parser = argparse.ArgumentParser(
        description=""" 
                        Multi agent battle simulation
                    """
    )

    parser.add_argument(
        "port", type=int, help="enter a valid port for the server to listen to"
    )
    parser.add_argument(
        "--grid_size", type=int, default=100, help="grid size (must be an integer)"
    )
    parser.add_argument(
        "--num_agents", type=int, default=200, help="number of agents in each team"
    )
    parser.add_argument("--num_teams", type=int, default=2, help="number of teams")
    parser.add_argument(
        "--num_episodes", type=int, default=20, help="number of episodes"
    )
    parser.add_argument(
        "--episode_length", type=int, default=100, help="length of each episode"
    )
    parser.add_argument(
        "--saved_model_path",
        type=str,
        default=None,
        help="path to pretrained neural network",
    )
    parser.add_argument(
        "--train_model", default=False, action="store_true", help="train"
    )

    args = parser.parse_args()

    server.start_server(args)


if __name__ == "__main__":
    main()
