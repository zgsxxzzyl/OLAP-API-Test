# -*- coding:utf-8 -*-
import argparse
import os

import api
import init
import mdx
import validate


def _single_test(session, script_path, data_path=None, is_init=False, is_mdx=False, is_validate=False):
    print script_path, data_path, is_init, is_mdx, is_validate
    if is_init:
        if data_path is not None:
            init.data(session, data_path)
        else:
            if os.path.exists(os.path.join(script_path, 'data')):
                init.data(session, os.path.join(script_path, 'data'))
    if is_mdx:
        mdx.run(session, script_path)
    if is_validate:
        validate.data()


if __name__ == '__main__':
    _parser = argparse.ArgumentParser(description='')
    _parser.add_argument('-host', metavar=None, type=str, help='Database address')
    _parser.add_argument('-d', metavar='directory', type=str, help='Script execution path')
    _parser.add_argument('-p', metavar='path', type=str, help='Initialize the file path')
    _parser.add_argument('-i', action='store_true', help='Whether it is initialized')
    _parser.add_argument('-m', action='store_true', help='Whether to execute the mdx script')
    _parser.add_argument('-v', action='store_true', help='Whether to verify data')
    # args = parser.parse_args()
    _args = _parser.parse_args(
        ['-host', 'http://localhost:7777', '-d', r'C:\Users\艺龙\Desktop\target', '-p',
         r'C:\Users\艺龙\Desktop\target\data', '-i'])

    _host = None if _args.host is None else _args.host
    _directory = None if _args.d is None else unicode(_args.d, 'utf-8')
    _data = None if _args.p is None else unicode(_args.p, 'utf-8')
    _is_init = False if _args.i is None else True
    _is_run_mdx = False if _args.m is None else True
    _is_validate = False if _args.v is None else True

    _session = api.Session(_args.host)
    for f in os.listdir(_directory):
        if f.lower().startswith('script-'):
            try:
                _single_test(_session, os.path.join(_directory, f), _data, _is_init, _is_run_mdx, _is_validate)
            except:
                pass
            else:
                print 'ok'