#!/usr/bin/python -i
"""
Change the input/output_file_path to select other files
"""

from mumath.treebuilder import treebuilder
import xml.etree.ElementTree as et

input_file_path = "mumath/sample.mu"
output_file_path= "mumath/sample.html"

def mumath(**options):

	### LOAD EXTENSIONS
	extensions = options.get("extension")

	### PRE-PROCESSING
	NotImplemented

	### BUILD TREE
	ifile = options.get("ifile")
	with open(ifile, mode="r", encoding="utf-8") as ifile:
		text = ifile.read()

	root = treebuilder(text)

	### POST-PROCESSING
	NotImplemented

	### PRINT COMPILED TEXT TO FILE
	ofile = options.get("ofile")
	with open(ofile, mode="w", encoding="utf-8") as ofile:
		ofile.write("""<!DOCTYPE html>""")
		ofile.write("""
<html>
<head>
	<title></title>
	<meta charset="utf-8">
<body>""")
		writer(ofile, root, 0)



INLINE = {}
OPTIONAL = {}
SELFCLOSE = {"mprescripts", "none"}

# sample writer
def writer(file, tree, level):
	if tree.tag not in INLINE: file.write("\n"+level*"\t")

	if tree.tag is et.Comment:
		file.write(f"<!--")
	else:
		file.write(f"<{tree.tag}")
		for attribute, value in tree.attrib.items():
			file.write(f' {attribute}="{value}"')
		if tree.tag in SELFCLOSE:
			file.write("/>") #xml
		else:
			file.write(">")

	#content
	if tree.text:
		lines = tree.text.splitlines()
		file.write(lines[0])
		if tree.tag != "pre":
			for line in lines[1:]:
				file.write("\n" + level*"\t" + line)
		else:
			for line in lines[1:]:
				print(line)
				file.write("\n" + line)

	#subtree
	if tree:
		for subtree in tree:
			if tree.tag != "pre": writer(file, subtree, level+1)
			else: writer(file, subtree, -100)

	#closing tag
	if tree.tag not in INLINE: file.write("\n" + level*"\t")
	if tree.tag not in SELFCLOSE:
		if tree.tag is et.Comment:
			file.write("-->")
		else:
			file.write(f"</{tree.tag}>")

	#tail
	if tree.tail:
		lines = tree.tail.splitlines()
		file.write(lines[0])
		for line in lines[1:]:
			file.write("\n" + level*"\t" + line)

if __name__ == "__main__":
	mumath(
		ifile    = input_file_path,
		ofile   = output_file_path,
		extension = [],
	)
