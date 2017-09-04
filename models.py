# -*- coding:utf-8 -*-


class Database(object):
    def __init__(self, new_name=None, type=None):
        self.flag = 'DATABASE'
        self.new_name = new_name
        self.type = type


class Dimension(object):
    def __init__(self, name_database=None, new_name=None, type=None):
        self.flag = 'DIMENSION'
        self.name_database = name_database
        self.new_name = new_name
        self.type = type


class Element(object):
    def __init__(self, name_database, name_dimension, new_name, type, name_children, weights):
        self.flag = 'ELEMENT'
        self.name_database = name_database
        self.name_dimension = name_dimension
        self.new_name = new_name
        self.type = type
        self.name_children = name_children
        self.weights = weights


class Cube(object):
    def __init__(self, name_database, new_name, name_dimensions, type):
        self.flag = 'CUBE'
        self.name_database = name_database
        self.new_name = new_name
        self.name_dimensions = name_dimensions
        self.type = type


class Cell(object):
    def __init__(self, name_database, name_cube, name_path, value):
        self.flag = 'CELL'
        self.name_database = name_database
        self.name_cube = name_cube
        self.name_path = name_path
        self.value = value
