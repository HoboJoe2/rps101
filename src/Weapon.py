import json


class Weapon():
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)