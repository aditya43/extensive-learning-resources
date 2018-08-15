#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aditya Hajare
# @Date:   2014-11-07 09:57:14
# @Last Modified time: 2018-06-05 17:04:12

import re
import sys
import os

from requests import get
from requests.exceptions import MissingSchema, ConnectionError

url_re = re.compile('.*\[.*\]\((.*)\)')
current_dir = os.path.dirname(os.path.realpath(__file__))

file = '{current_dir}/../README.md'.format(current_dir=current_dir)
with open(file) as f:
    for line, content in enumerate(f):
        m = re.match(url_re, content)
        if m is None:
            continue
        try:
            result = get(m.group(1))
            if result.status_code >= 400:
                print('{file} line #{line} {url} return {code}'.format(file=file, line=line,
                    url=m.group(1), code=result.status_code))
                sys.exit(1)
            print('{file} line #{line} {url} pass'.format(file=file, line=line, url=m.group(1)))
        except ConnectionError:
            print('{file} line #{line} {url} cannot connect'.format(file=file, line=line,
                    url=m.group(1)))
        except MissingSchema:
            print('{file} line #{line} {url} missing schema'.format(file=file, line=line,
                    url=m.group(1)))


