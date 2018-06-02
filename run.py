#!/usr/bin/env python3
#
import os
import sys
import subprocess as sp
from files import Files
import re

lua_module = ''
intel_license_line = ''
f = Files()
user = os.getenv('USER')

env = f.files['env']

env_cmd = f'{env}'
show_env = sp.getoutput(env_cmd)
clean_env_cmd = f'env -i bash -f -c env'
clean_env = sp.getoutput(clean_env_cmd)

vars = {}
for line in show_env.splitlines():
    if "=" not in line:
        continue
    if line in clean_env:
        continue
    var = line.split("=")[0]
    values = line.split("=")[1]
    
    vars[var] = [ v for v in values.split(":") ]

    for var, values in vars.items():
        temp = ''
        for value in values:
            if value == "":
                continue
            elif re.search("\(\)$", var):
                # match bash functions
                continue
                temp += f"setenv(\"{var}\",\"{value}\")\n"
            else:
                temp += f"prepend_path(\"{var}\",\"{value}\")\n"
    lua_module += temp

lua_module = f"""-- -*- lua module file : Create a mirror image of user {user} environment --

help([[this module will create a mirror image of user {user} environment
and convert it to an lmod lua module file.]])

family("user_environment")
{lua_module}
"""
print(lua_module)
