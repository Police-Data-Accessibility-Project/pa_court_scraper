# pa_court_scraper
Court Scraper for Pennsylvania

# Installation

## Set Up Docker
Ensure that [Docker](https://docs.docker.com/get-started/get-docker/) is installed on your system. 

Docker ensures that the majority of the application operates inside a "container" that is isolated from the rest of the system.

## Set Up Python
Ensure that [Python 3.13](https://www.python.org/downloads/release/python-3132/) is installed on your system. 

While there is a requirements.txt file, that is used within the Python Dockerfile, not by the user directly.
Instead, the user only needs to install the `docker` package
```shell
pip install docker
```

# Commands
Get Docket Numbers
- This script parses the webpage and writes the docket numbers to a text file.
- The text file is located at `data/docket_numbers_from_yesterday.txt`.
```shell
python main.py get-docket-numbers
```

Get Docket Information
- This script retrieves all docket information from the above text file and stores it in a MongoDB database.
- The MongoDB database is located at `mongodb://mongo:27017/`.
  - Currently, the database is "mydatabase", and the collection is "mycollection". 
- Note that this script takes an extended period of time to run, as requests are staggered to avoid rate-limiting.
  - To reduce the number of docket numbers retrieved, delete docket numbers from the text file
```shell
python main.py get-docket-info
```

Stop MongoDB instance
- The MongoDB instance does not stop automatically after the above two commands are run
- The below command will stop and remove the MongoDB container (deleting all data within it)
```shell
python main.py stop-mongodb
```


# Review Results 

Results can be reviewed using [MongoDB Compass](https://www.mongodb.com/try/download/compass). 
Note that the MongoDB container must be up and running to review results.