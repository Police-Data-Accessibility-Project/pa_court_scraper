import json


class SimpleCache:
    def __init__(self):
        self.cache = {}

    def load_from_file(self):
        # Load from JSON
        with open("cache.json", "r") as f:
            self.cache = json.loads(f.read())


    def save_to_file(self):
        # Save as JSON
        with open("cache.json", "w") as f:
            f.write(json.dumps(self.cache))

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def is_empty(self):
        return len(self.cache) == 0

    def get_keys(self):
        return list(self.cache.keys())