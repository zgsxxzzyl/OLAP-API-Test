# -*- coding:utf-8 -*-
import datetime
from urlparse import urlparse

import utils as req


class Session(object):
    _database_req = None
    _server_req = None
    _cell_req = None
    _cube_req = None
    _element_req = None
    _dimension_req = None
    _mdx_req = None
    _start = None
    _sid = None

    def __init__(self, address):
        self.address = urlparse(address)

    def database(self):
        if self._database_req is None:
            self._database_req = DatabaseReq(self.address.hostname, self.address.port, self._get_sid())
        return self._database_req

    def server(self):
        if self._server_req is None:
            self._server_req = ServerReq(self.address.hostname, self.address.port, self._get_sid())
        return self._server_req

    def cell(self):
        if self._cell_req is None:
            self._cell_req = CellReq(self.address.hostname, self.address.port, self._get_sid())
        return self._cell_req

    def dimension(self):
        if self._dimension_req is None:
            self._dimension_req = DimensionReq(self.address.hostname, self.address.port, self._get_sid())
        return self._dimension_req

    def cube(self):
        if self._cube_req is None:
            self._cube_req = CubeReq(self.address.hostname, self.address.port, self._get_sid())
        return self._cube_req

    def element(self):
        if self._element_req is None:
            self._element_req = ElementReq(self.address.hostname, self.address.port, self._get_sid())
        return self._element_req

    def mdx(self):
        if self._mdx_req is None:
            self._mdx_req = MdxReq(self.address.hostname, self.address.port, self._get_sid())
        return self._mdx_req

    def _get_sid(self):
        if self._start is None or (datetime.datetime.now() - self._start).microseconds > 30 * 1000 * 1000:
            self._start = datetime.datetime.now()
            self._sid = self.server().login(params={'user': 'admin', 'extern_password': 'planning'}).split(';')[0];
        return self._sid


class ServerReq(object):
    def __init__(self, host, port, sid):
        self.host = host
        self.port = str(port)

    def login(self, params):
        __url = 'http://' + self.host + ':' + self.port + '/server/login'
        return req.get(__url, params)


class DatabaseReq(object):
    def __init__(self, host, port, sid):
        self._host = host
        self._port = str(port)
        self._sid = sid

    def create(self, params):
        __url = 'http://' + self._host + ':' + self._port + '/database/create'
        params['sid'] = self._sid
        return req.get(__url, params)

    def destroy(self, params):
        __url = 'http://' + self._host + ':' + self._port + '/database/destroy'
        params['sid'] = self._sid
        return req.get(__url, params)

    def cubes(self, params):
        __url = 'http://' + self._host + ':' + self._port + '/database/cubes'
        params['sid'] = self._sid
        return req.get(__url, params)


class DimensionReq(object):
    def __init__(self, host, port, sid):
        self._host = host
        self._port = str(port)

    def create(self, params):
        __url = 'http://' + self._host + ':' + self._port + '/dimension/create'
        params['sid'] = self._sid
        return req.get(__url, params)


class ElementReq(object):
    def __init__(self, host, port, sid):
        self._host = host
        self._port = str(port)
        self._sid = sid

    def create(self, params):
        __url = 'http://' + self._host + ':' + self._port + '/element/create'
        params['sid'] = self._sid
        return req.get(__url, params)


class CubeReq(object):
    def __init__(self, host, port, sid):
        self._host = host
        self._port = str(port)
        self._sid = sid

    def clear(self, params):
        __url = 'http://' + self._host + ':' + self._port + '/cube/clear'
        params['sid'] = self._sid
        return req.get(__url, params)

    def create(self, params):
        __url = 'http://' + self._host + ':' + self._port + '/cube/create'
        params['sid'] = self._sid
        return req.get(__url, params)


class CellReq(object):
    def __init__(self, host, port, sid):
        self._host = host
        self._port = str(port)
        self._sid = sid

    def replace(self, params):
        __url = 'http://' + self._host + ':' + self._port + '/cell/replace'
        params['sid'] = self._sid
        return req.get(__url, params)


class MdxReq(object):
    def __init__(self, host, port, sid):
        self._host = host
        self._port = str(port)
        self._sid = sid
