#!/usr/bin/env python

import os
import ast
from PIL import Image



img_html = """
<div align="center">
<img style="width:%dpx; height:%dpx;" src="%s" alt="%s">
</div>
"""


def add_toc(doc):
	headers = [(i,x) for i,x in enumerate(doc) if x.startswith('#')]
	n = min([len(x[1].split()[0]) for x in headers])
	
	toc = []
	new_doc = doc[:]

	for i,hdr in headers:
		toks = hdr.strip().split()
		hashes = toks[0]
		title = str(' ').join(toks[1:])
		anchor = str('').join([x for x in title \
			if (x.isalnum() or x==' ' or x=='-' or x=='_')])
		anchor = anchor.lower().replace(' ','-')
		
		depth = len(hashes) - n
		entry = "%s- [%s](#%s)" % (depth*4*' ', title, anchor)
		toc.append(entry)

		new_doc[i] = "%s <a name='%s' class='anchor' href='#%s'></a> %s" \
			% (hashes, anchor, anchor, title)

	toc.append("")
	return toc + new_doc


def inject_image(d):
	im = Image.open("../%s" % d["src"])
	scale = d.get("scale", 1.0)
	w = int(im.size[0] * scale)
	h = int(im.size[1] * scale)
	html = img_html % (w, h, d["src"], d.get("alt",""))
	return html


def add_expansions(doc):
	lines = [(i,x) for i,x in enumerate(doc) if x.startswith('!!!')]
	new_doc = doc[:]

	for i,line in lines:
		d = ast.literal_eval("{%s}" % line[3:])
		if d.get("type") == "img":
			new_doc[i] = inject_image(d)
		else:
			raise ValueError("Malformed expansion")

	return new_doc


with open("../user_manual.md") as f:
	usrman = f.read().strip().split('\n')

usrman = add_toc(usrman)
usrman = add_expansions(usrman)
print str('\n').join(usrman)
