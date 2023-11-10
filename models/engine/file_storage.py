#!/usr/bin/python3
"""FileStorage class that serializes instances to a JSON file
and deserializes JSON file to instances"""

import json


class FileStorage:
    """FileStorage class that serializes instances to a JSON file
       and deserializes JSON file to instances"""

    __file_path = "data.json"
    __objects = {}

    def all(self):
        """Return all the objects"""
        return (FileStorage.__objects)

    def new(self, obj):
        """Add a new object"""
        FileStorage.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """Save all objects to a json file"""
        ob = self.__objects.copy()
        for k in self.__objects:
            ob[k] = self.__objects[k].to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(ob, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                j = json.load(f)
            for key in j:
                self.__objects[key] = classes[j[key]["__class__"]](**jo[key])
        except Exception:
            pass
