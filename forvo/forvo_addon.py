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

from __future__ import with_statement
from anki.hooks import addHook
from aqt.utils import showInfo
from aqt import mw
from aqt.qt import *
import forvo
import tempfile
import sys

def onDownload(v):
	word = ""

	if v.editor.note is not None:
		word = v.editor.note.values()[0]

	if word == "":
		word, ok = QInputDialog.getText(v, "Word to download", "Downloaded from Forvo")
	else:
		ok = True

	if ok and word:
		d = tempfile.mkdtemp()
		filename = forvo.download(word, d)

		if filename:
			v.editor.addMedia(filename)
		else:
			showInfo("Audio not available for " + word)

def onContextClick(view,menu):
	a = menu.addAction(_("Download Audio"))
	a.connect(a, SIGNAL("triggered()"), lambda v=view: onDownload(v))

addHook("EditorWebView.contextMenuEvent", onContextClick)

