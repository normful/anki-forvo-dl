#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  forvo.py
#
#  Copyright 2016 Troy <troy@pingviini>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import os
import json
import requests
import urllib2

URL_FORMAT=unicode("http://apifree.forvo.com/action/standard-pronunciation/format/json/word/{word}/language/{lang}/key/{key}/")
LANGUAGE=unicode("fi")

def getAPIKey():
	key = ""
	with open(os.path.expanduser("~/.forvo"), "r") as fd:
		key = fd.read(32)

	return key

# downloads the word and puts it into the given directory
def download(word, directory):
	q = urllib2.quote(word.encode('utf-8'))
	url=URL_FORMAT.format(key=getAPIKey(),lang=LANGUAGE,word=q)
	r = requests.get(url)

	if r.status_code != requests.codes.ok:
		return False

	json = r.json()

	if len(json['items']) == 0:
		return False

	pathmp3 = json['items'][0]['pathmp3']

	mp3 = requests.get(pathmp3)

	if mp3.status_code != requests.codes.ok:
		return False

	filename = directory + "/" + word + ".mp3"

	with open(filename, 'wb') as fd:
		for chunk in mp3.iter_content(512):
			fd.write(chunk)

	return filename
