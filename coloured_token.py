import json

USER_IDENTIFICATION = 'user_id'


class ColouredToken:
    json_dict = None
    user_id = None

    def __init__(self, value):
        self.json_dict = json.dumps(value, separators=(',\n', ':'))
        self.user_id = value.get(USER_IDENTIFICATION)

    def __str__(self):
        return self.json_dict

    def __repr__(self):
        return self.__str__() if len(self.__str__()) < 60 else self.__str__()[0:60:1] + '...'

    def __eq__(self, other):
        if self.__str__() == other.__str__():
            return True
        return False

    def __hash__(self):
        return hash(self.json_dict)

    def get_dict(self):
        return json.loads(self.json_dict)
