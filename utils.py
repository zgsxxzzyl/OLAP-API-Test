# -*- coding:utf-8 -*-
import requests as req


def get(url, params):
    _resp = req.get(url, params)
    if _resp.status_code == 200:
        print _resp.url
        return _resp.text
    if _resp.status_code > 200:
        raise Exception(_resp.text)
