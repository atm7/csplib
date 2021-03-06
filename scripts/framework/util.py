# -*- coding: utf-8 -*-
# Bilal Syed Hussain

import cgi  # for cgi.escape
import markdown
import os, os.path as path
import zipfile


markdown_exts = ['extra', 'meta', 'sane_lists', 'tables', 'smartypants(entities=named)', 'cite_bibtex']

source_types = set(['cc', 'c', 'java', 'cpp', 'cs', 'eprime', 'erl', 'essence',
				'groovy', 'h', 'hh', 'hpp', 'hrl', 'javascript', 'js',
				'param', 'php', 'pl', 'py', 'rb', 'scala', 'solution', 'xml'])

text_formats = set(['txt', 'minizinc', 'hs', 'lhs', 'lisp', 'cnf', 'ecl', 'egenet',
					'chip', 'mzn', 'pi', 'pl', 'co'])
text_formats |= source_types


def convert_markdown(page_path):
	md = markdown.Markdown(extensions=markdown_exts)
	md_input = read_file(page_path)
	page = md.convert(md_input)
	if hasattr(md, 'Meta'):
		return (page, md.Meta)
	else:
		return (page, dict())


def read_file(filepath):
	with open(filepath, "r") as f:
		return "".join(f.readlines() + ["\n"])


def get_content_and_metadata(filepath, store_dir):
	(_, ext) = path.splitext(filepath)
	if (ext == ".md"):
		(a, b) = convert_markdown(filepath)
		if not('type' in b):
			b['type'] = [ext[1:]]
		return (a, b, None)
	elif (ext == '.html'):
		return (read_file(filepath), None, None)

	meta = dict()

	meta_path = filepath + ".metadata"
	try:
		(_, meta) = convert_markdown(meta_path)
	except Exception:
		pass

	# Add the language
	if not('type' in meta):
		meta['type'] = [ext[1:]]

	print
	if ext[1:] in text_formats:
		css_class = ""
		txt = read_file(filepath)
		if ext[1:] in source_types:
			css_class = "class ='brush: {0}'".format(ext[1:])
			txt = cgi.escape(txt)

		return ("<pre {0}>{1}</pre>".format(css_class, txt), meta, None)
	else:
		bname = path.basename(filepath)
		url = path.join(store_dir, bname)
		return ("<a href='{0}'> {1} </a>".format(url, bname), meta, url)


def create_zip_file(create_path, files):
	""" creates a zip file with the specified (src,dst) """
	zf = zipfile.ZipFile(create_path, "w")
	for (src, dst) in files:
		zf.write(src, dst)
	zf.close()


# since exist_ok is not in python2
def makedirs_exist_ok(path):
	try:
		os.makedirs(path)
	except OSError:
		if not os.path.isdir(path):
			raise
