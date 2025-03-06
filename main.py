import argparse
import os
import sys

import docker
from docker.errors import APIError, NotFound


class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
        self.network_name = "my_network"
        self.network = self.start_network()
        self.mongo_container = self.startup_mongodb()


    def start_network(self):
        try:
            self.client.networks.create(self.network_name, driver="bridge")
        except APIError as e:
            # Assume already exists
            print(e)
        return self.client.networks.get("my_network")

    def stop_network(self):
        self.client.networks.get("my_network").remove()

    def startup_mongodb(self):
        try:
            print("Starting MongoDB container...")
            return self.client.containers.run(
                "mongo:latest",  # Image name
                detach=True,  # Run in detached mode
                name="mongodb",  # Container name
                ports={"27017/tcp": 27017},  # Port mapping (container:host)
                network=self.network_name
            )
            print("MongoDB container started.")
        except APIError as e:
            # Assume already exists
            print(e)
            print("MongoDB container already exists. Reusing...")
            return self.client.containers.get("mongodb")

    def stop_mongodb(self):
        print("Stopping MongoDB container...")
        self.client.containers.get("mongodb").stop()
        self.client.containers.get("mongodb").remove()

    def run_dockerfile(self, command: str):
        dockerfile_path = os.path.dirname(os.path.abspath(__file__))
        tag = "court_scraper"
        image = self.client.images.build(
            path=dockerfile_path,
            tag=tag
        )

        # Create data directory if doesn't exist
        data_directory = dockerfile_path + "/data"
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)

        volumes = {
            data_directory: {
                "bind": "/app/data",
                "mode": "rw"
            }
        }
        # Stop if
        self.stop_dockerfile()

        container = self.client.containers.run(
            tag,
            volumes=volumes,
            command=command,
            detach=True,
            name="court_scraper",
            ports={"5000/tcp": 5000},
            network=self.network_name,
            environment={
                "MONGO_URI": "mongodb://mongo:27017/"
            },
            stdout=True,
            stderr=True
        )
        for log in container.logs(stream=True, follow=True):  # 'follow=True' ensures logs stop when the container stops
            print(log.decode().strip())

        return container

    def stop_dockerfile(self):
        try:
            self.client.containers.get("court_scraper")
        except NotFound:
            return
        self.client.containers.get("court_scraper").stop()
        self.client.containers.get("court_scraper").remove()


def run_command(command):
    dm = DockerManager()
    dm.run_dockerfile(command)
    dm.stop_dockerfile()
    dm.stop_network()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command-line tool for docket operations and MongoDB management.")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for 'get_docket_info'
    parser_info = subparsers.add_parser(
        "get-docket-info",
        help="Retrieve information for dockets listed in `data/docket_numbers_from_yesterday.txt`."
    )

    # Subparser for 'get_docket_numbers'
    subparsers.add_parser(
        "get-docket-numbers",
        help="Retrieve all docket numbers from yesterday and writes to `data/docket_numbers_from_yesterday.txt`."
    )

    # Subparser for 'stop_mongodb'
    subparsers.add_parser(
        "stop-mongodb",
        help="Stop the MongoDB service."
    )

    args = parser.parse_args()



    if args.command == "get-docket-info":
        run_command(
            "python get_docket_info.py"
        )
    elif args.command == "get-docket-numbers":
        run_command(
            "python get_docket_numbers_from_yesterday.py"
        )
    elif args.command == "stop-mongodb":
        dm = DockerManager()
        dm.stop_mongodb()
    else:
        parser.print_help()
        sys.exit(1)
