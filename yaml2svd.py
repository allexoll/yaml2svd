#!/usr/bin/env python3

import yaml
import sys
import os
from collections import OrderedDict
import xmltodict
import re


#open file 
top_file = open(sys.argv[1], 'r')
#load file
top_content = yaml.safe_load(top_file)

# output buffer
output = OrderedDict({"device": {}})

# copy top elements exept for peripherals
for top in top_content["device"].items():
    if top[0] != "peripherals":
        output["device"][top[0]] = top[1]

# copy peripherals
output_peripherals = []
for peripheral in top_content["device"]["peripherals"]:
    # get source file path
    source_path = peripheral["source"]
    # construct path name
    parentDirectory = os.path.dirname(sys.argv[1])
    # open source file
    source = open(os.path.join(parentDirectory, source_path))
    # load source file
    source_content = OrderedDict(yaml.safe_load(source)[0]["peripheral"])
    # copy peripheral name to output
    source_content["name"] = peripheral["name"]
    # copy base address to output
    source_content["baseAddress"] = peripheral["baseAddress"]
    # copy peripheral content to output
    export = {"peripheral": source_content}
    # add peripheral to existing list
    output_peripherals.append(export)


# copy new peripherals into top level
output["device"]["peripherals"] = output_peripherals

# open output file
f = open(sys.argv[2], "w+")

# produce XML
output_xml = xmltodict.unparse(output, pretty=True)

# remove separeted fields in the svd.
exclude_list = [
    "\s*</registers>\n\s+<registers>", "\s*</peripherals>\n\s+<peripherals>",
    "\s*</fields>\n\s+<fields>",
    "\s*</enumeratedValues>\n\s+<enumeratedValues>"
]
for regex in exclude_list:
    output_xml = re.sub(regex, '', output_xml)

replace_list = {
    "<device>" : '<device  schemaVersion="1.1" xmlns:xs="http://www.w3.org/2001/XMLSchema-instance" xs:noNamespaceSchemaLocation="CMSIS-SVD.xsd" >'
}

for element in replace_list.items():
    output_xml = output_xml.replace(element[0], element[1])
    
# write output file
f.write(output_xml)

# done!
print(".svd file created {}".format(sys.argv[2]))
