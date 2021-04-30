import json
import datetime as dt


class GameScore:
    JSON_FILENAME = "./scores.json"
    FIELDNAMES = ["username", "levels"]
    EMPTY_lEVEL = {"level": None, "duration": None, "score": None}

    def __init__(self, username):
        self.username = username
        self.levels = []

    def add_level(self, level, starttime, endtime, score):
        new_level_data = dict()
        new_level_data["level"] = level
        new_level_data["starttime"] = starttime
        new_level_data["endtime"] = endtime
        new_level_data["score"] = score
        self.levels.append(new_level_data)

    def _is_file_clear(self):
        with open(self.JSON_FILENAME, "r") as f:
            data = f.read()
        if data.strip() == "":
            return True
        return False

    def _get_self_dict(self):
        mydict = {field: getattr(self, field) for field in self.FIELDNAMES}
        return mydict

    def save(self):
        if self._is_file_clear():
            with open(self.JSON_FILENAME, "w") as f:
                f.write("[]")

        with open(self.JSON_FILENAME, "r") as f:
            records = json.load(f)

        records.append(self._get_self_dict())

        with open(self.JSON_FILENAME, "w") as f:
            json.dump(records, f, default=str)


def main():
    score = GameScore("Mena")
    score.add_level(2, dt.datetime.now(), dt.datetime.now(), 1400)
    score.save()


if __name__ == "__main__":
    main()
