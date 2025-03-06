# pa_court_scraper
Court Scraper for Pennsylvania


```shell
docker run -d --name mongodb -p 27017:27017 mongo:latest
```

Install requirements

```shell
pip install -r requirements.txt
```

Run `get_docket_numbers_from_yesterday.py` to retrieve all docket numbers filed on the previous day.

Run `get_docket_info.py` to retrieve information about each docket number.
- Note that this script takes an extended period of time to run, as requests are staggered to avoid rate-limiting.

While `get_docket_info` is running, the MongoDB database can be inspected using an application such as [MongoDBCompass](https://www.mongodb.com/products/tools/compass).
- Currently, the database is "mydatabase", and the collection is "mycollection".