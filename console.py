#!/usr/bin/python3
"""Defines the HBNB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    """takes a string arg as input
    and parses it based on the presence of curly braces {}
    and square brackets []."""

    # Search for curly braces content
    curly_braces = re.search(r"\{(.*?)\}", arg)

    # Search for square brackets content
    square_brackets = re.search(r"\[(.*?)\]", arg)

    if curly_braces is None:
        if square_brackets is None:
            # No Curly braces or square brackets found, split on commas
            return [i.strip(",") for i in split(arg)]

        else:
            # Curly braces not found, but square brackets found
            before_square_brackets = split(arg[:square_brackets.span()[0]])
            resulted_list = [element.strip(",")
                             for element in before_square_brackets]
            resulted_list.append(square_brackets.group())

            return (resulted_list)

    else:
        # Curly braces found
        before_curly_braces = split(arg[:curly_braces.span()[0]])
        resulted_list = [element.strip(",") for element in before_curly_braces]
        resulted_list.append(curly_braces.group())
        return (resulted_list)


class HBNBCommand(cmd.Cmd):
    """Defines the AirBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    Classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon entering an empty line"""

        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""

        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""

        print("")
        return True

    def default(self, arg):
        """Default behavior for cmd module"""

        arguments_dictionay = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        matched_string = re.search(r"\.", arg)
        if matched_string is not None:
            new_argument = [arg[:matched_string.span()[0]],
                            arg[matched_string.span()[1]:]]
            matched_string = re.search(r"\((.*?)\)", new_argument[1])
            if matched_string is not None:
                command = [new_argument[1][:matched_string.span()[0]],
                           matched_string.group()[
                    1:-1]]
                if command[0] in arguments_dictionay.keys():
                    call = "{} {}".format(new_argument[0], command[1])
                    return arguments_dictionay[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """

        new_arg = parse(arg)
        if len(new_arg) == 0:
            print("** class name missing **")
        elif new_arg[0] not in HBNBCommand.Classes:
            print("** class doesn't exist **")
        else:
            print(eval(new_arg[0])().id)
            storage.save

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """

        new_arg = parse(arg)
        objects_dictonary = storage.all()
        if len(new_arg) == 0:
            print("** class name missing **")
        elif new_arg[0] not in HBNBCommand.Classes:
            print("** class doesn't exist **")
        elif len(new_arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(new_arg[0], new_arg[1]) not in objects_dictonary:
            print("** no instance found **")
        else:
            print(objects_dictonary["{}.{}".format(new_arg[0], new_arg[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id.
        """

        new_arg = parse(arg)
        objects_dictonary = storage.all()
        if len(new_arg) == 0:
            print("** class name missing **")
        elif new_arg[0] not in HBNBCommand.Classes:
            print("** class doesn't exist **")
        elif len(new_arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format([0], new_arg[1]) not in objects_dictonary:
            print("** no instance found **")
        else:
            del objects_dictonary["{}.{}".format(new_arg[0], new_arg[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""

        new_argument = parse(arg)
        if len(new_argument) > 0 and new_argument[0] not in HBNBCommand.Classes:
            print("** class doesn't exist **")
        else:
            objects_list = []
            for object in storage.all().values():
                if len(new_argument) > 0 and new_argument[0] == object.__class__.__name__:
                    objects_list.append(object.__str__())
                elif len(new_argument) == 0:
                    objects_list.append(object.__str__())
            print(objects_list)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""

        new_argument = parse(arg)
        count = 0
        for obj in storage.all().values():
            if new_argument[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""

        new_argument = parse(arg)
        objects_dictonary = storage.all()

        if len(new_argument) == 0:
            print("** class name missing **")
            return False
        if new_argument[0] not in HBNBCommand.Classes:
            print("** class doesn't exist **")
            return False
        if len(new_argument) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(new_argument[0], new_argument[1]) not in objects_dictonary.keys():
            print("** no instance found **")
            return False
        if len(new_argument) == 2:
            print("** attribute name missing **")
            return False
        if len(new_argument) == 3:
            try:
                type(eval(new_argument[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(new_argument) == 4:
            obj = objects_dictonary["{}.{}".format(
                new_argument[0], new_argument[1])]
            if new_argument[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[new_argument[2]])
                obj.__dict__[new_argument[2]] = valtype(new_argument[3])
            else:
                obj.__dict__[new_argument[2]] = new_argument[3]
        elif type(eval(new_argument[2])) == dict:
            obj = objects_dictonary["{}.{}".format(
                new_argument[0], new_argument[1])]
            for k, v in eval(new_argument[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
