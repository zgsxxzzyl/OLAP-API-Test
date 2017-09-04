# -*- coding:utf-8 -*-
import csv
import os
import re

import api
from models import Cell, Element, Dimension, Cube, Database


def csv_convert_obj(path):
    _list = list()
    with open(path) as f:
        _csv = csv.reader(f, delimiter=';')
        if os.path.basename(path).lower().startswith('cell-'):
            for row in _csv:
                if list(row).__len__() == 5:
                    _list.append(Cell(row[1], row[2], row[3], row[4]))
        elif os.path.basename(path).lower().startswith('element-'):
            for row in _csv:
                if list(row).__len__() == 7:
                    _list.append(Element(row[1], row[2], row[3], row[4], row[5], row[6]))
        elif os.path.basename(path).lower().startswith('dimension-'):
            for row in _csv:
                if list(row).__len__() == 4:
                    _list.append(Dimension(row[1], row[2], row[3]))
        elif os.path.basename(path).lower().startswith('cube-'):
            for row in _csv:
                if list(row).__len__() == 5:
                    _list.append(Cube(row[1], row[2], row[3], row[4]))
        elif os.path.basename(path).lower().startswith('database-'):
            for row in _csv:
                if list(row).__len__() == 3:
                    _list.append(Database(row[1], row[2]))
    return _list


# li = csv_convert_obj(unicode(r'C:\Users\艺龙\Desktop\target\data\cell-input.csv','utf-8'))
# print li.__len__()

def _database(session, path):
    for d in csv_convert_obj(path):
        if isinstance(d, Database):
            _resp = session.database().create(params={'new_name': d.new_name})
        print _resp


def _dimension(session, path):
    for d in csv_convert_obj(path):
        if isinstance(d, Dimension):
            _resp = session.dimension().create(params={'name_database': d.name_database, 'new_name': d.new_name})
        print _resp


def _element(session, path):
    for d in csv_convert_obj(path):
        if isinstance(d, Element):
            _resp = session.element().create(
                params={'name_database': d.name_database, 'name_dimension': d.name_dimension, 'new_name': d.new_name,
                        'name_dimension': d.name_dimension})
        print _resp


def _cube(session, path):
    for d in csv_convert_obj(path):
        if isinstance(d, Cube):
            _resp = session.cube().create(
                params={'name_database': d.name_database, 'new_name': d.new_name, 'name_dimensions': d.name_dimensions})
        print _resp


def _cell(session, path):
    for d in csv_convert_obj(path):
        if isinstance(d, Cell):
            _resp = session.cell().replace(
                params={'name_database': d.name_database, 'name_path': d.name_path, 'name_cube': d.name_cube,
                        'value': d.value})
        print _resp


def data(session, path):
    if _verify_file(path):
        try:
            _database(session, os.path.join(path, 'database-input.csv'))
        except Exception as e:
            if str(e.message).startswith('2005'):  # code return database name in use
                _pattern = re.compile(r"value\s{1}\'(?P<name>\S*)\'")
                _match = _pattern.search(e.message)
                _db_name = _match.group('name')
                _resp = session.database().cubes(params={'name_database': _db_name})
                for line in _resp.splitlines(False):
                    session.cube().clear(
                        params={'name_database': _db_name, 'cube': str(line).split(';', 1)[0], 'complete': 1})
        else:
            _dimension(session, os.path.join(path, 'dimension-input.csv'))
            _element(session, os.path.join(path, 'element-input.csv'))
            _cube(session, os.path.join(path, 'cube-input.csv'))
        finally:
            _cell(session, os.path.join(path, 'cell-input.csv'))


def _verify_file(path):
    if os.path.exists(path):
        if 'cell-input.csv' in os.listdir(path) and 'cube-input.csv' in os.listdir(
                path) and 'database-input.csv' in os.listdir(path) and 'dimension-input.csv' in os.listdir(path) \
                and 'element-input.csv' in os.listdir(path):
            return True
    return False


_session = api.Session('http://localhost:7777')
# _session.database().cubes(params={'name_database': 'test'})
data(_session, unicode(r'C:\Users\艺龙\Desktop\target\data', 'utf-8'))
# _session.server().login(params={'user':'admin',''})
