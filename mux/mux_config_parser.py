#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2016 Yoann QUERET <yoann@queret.net>
"""


import shlex
from collections import OrderedDict
import json


class BoostInfoTree(object):
	def __init__(self, value = None, parent = None):
		super(BoostInfoTree, self).__init__()
		self.subTrees = OrderedDict()
		self.value = value
		self.parent = parent

		self.lastChild = None

	def createSubtree(self, treeName, value=None ):
		newTree = BoostInfoTree(value, self)
		if treeName in self.subTrees:
			self.subTrees[treeName].append(newTree)
		else:
			self.subTrees[treeName] = [newTree]
		self.lastChild = newTree
		return newTree

	def __getitem__(self, key):
		# since there can be repeated keys, we may have to get creative
		#print self.subTrees
		found = self.subTrees[key]
		return list(found)

	def getValue(self):
		return self.value

	def _prettyprint(self, indentLevel=1):
		prefix = " "*indentLevel
		s = ""
		if self.parent is not None:
			if self.value is not None and len(self.value) > 0:
				s += "\"" + str(self.value) + "\""
			s+= "\n" 
		if len(self.subTrees) > 0:
			if self.parent is not None:
				s += prefix+ "{\n"
			nextLevel = " "*(indentLevel+2)
			for t in self.subTrees:
				for subTree in self.subTrees[t]:
					s += nextLevel + str(t) + " " + subTree._prettyprint(indentLevel+2)
			if self.parent is not None:
				s +=  prefix + "}\n"
		return s

	def _prettygetConfig(self):
		s = ""
		if self.parent is not None:
			if self.value is not None and len(self.value) > 0:
				s += "\"" + str(self.value) + "\","
		if len(self.subTrees) > 0:
			s += "{"
			for t in self.subTrees:
				for subTree in self.subTrees[t]:
					s += "\"" + str(t) + "\": " + subTree._prettygetConfig()
			s = s[:-1]
			s +=  "},"
			
		return s

	def __str__(self):
		return self._prettyprint()

	def getConfig(self):
		j = self._prettygetConfig()[:-1]
		return json.loads(j)


class BoostInfoParser(object):
	def __init__(self):
		self._reset()

	def _reset(self):
		self._root = BoostInfoTree()
		self._root.lastChild = self

	def read(self, filename):
		with open(filename, 'r') as stream:
			ctx = self._root
			for line in stream:
				ctx = self._parseLine(line.strip(), ctx)

	def write(self, filename):
		with open(filename, 'w') as stream:
			stream.write(str(self._root))

	def _parseLine(self, string, context):
		# skip blank lines and comments
		commentStart = string.find(";")
		if commentStart >= 0:
			string = string[:commentStart].strip()
		if len(string) == 0:
			return context

		# ok, who is the joker who put a { on the same line as the key name?!
		sectionStart = string.find('{')
		if sectionStart > 0:
			firstPart = string[:sectionStart]
			secondPart = string[sectionStart:]

			ctx = self._parseLine(firstPart, context)
			return self._parseLine(secondPart, ctx)

		#if we encounter a {, we are beginning a new context
		# TODO: error if there was already a subcontext here
		if string[0] == '{':
			context = context.lastChild 
			return context

		# if we encounter a }, we are ending a list context
		if string[0] == '}':
			context = context.parent
			return context

		# else we are expecting key and optional value
		strings = shlex.split(string)
		key = strings[0]
		if len(strings) > 1:
			val = strings[1]
		else:
			val = None
		newTree = context.createSubtree(key, val)

		return context

	def getRoot(self):
		return self._root

	def __getitem__(self, key=None):
		ctxList = [self._root]
		if key is not None:
			path = key.split('/')
			foundVals = []
			for k in path:
				newList = []
				for ctx in ctxList:
					try:
						newList.extend(ctx[k])
					except KeyError:
						pass
				ctxList = newList
		return ctxList
	def load(self, key=None):
		return self.__getitem__(key).__getitem__(0)

def main():
	import sys
	import argparse
	
	parser = argparse.ArgumentParser(description='ODR - Tools to convert mux configuration file')
	parser.add_argument('-i', '--input', help='Input file', required=True)
	cli_args = parser.parse_args()
    
	try:
		parser = BoostInfoParser()
		parser.read(cli_args.input)
		
		# Print all configuraton file
		print parser.load().getConfig()

		# Print only subchannels section
		print parser.load("subchannels").getConfig()

	except IndexError:
		print 'Error'

if __name__ == '__main__':

	main()
	
