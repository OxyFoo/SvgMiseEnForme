#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__name__ = "svg-format"
__doc__ = "SVG parsing tool"
__author__ = "Gérémy Lecaplain"
__copyright__ = "Oxyfoo"
__version__ = "1.0"

import os
from lib.config import Config
from lib.tag import Tag
from lib.utils import Debug, GetFileContent, SaveFileContent, checkPythonVersion, defineHandler, printFullLine
from lib.reactnative import SvgToRN

# Config
Config.dirRaw = './raw'
Config.dirSvg = './svg'
Config.DEBUG_LEVEL = 1
Config.identSpace = '    '

checkPythonVersion()
defineHandler()
Config.CheckFolders()



printFullLine()

svgFiles = os.listdir(Config.dirRaw)
for filename in svgFiles:
    # Check if file is a valid svg file
    filepath = os.path.join(Config.dirRaw, filename)
    newFilePath = os.path.join(Config.dirSvg, filename)
    if not filepath.endswith(".svg"): continue
    if not os.path.isfile(filepath): continue

    Debug(0, 'Processing file "' + filename + '"')

    # Get svg content & parse it
    svgContent = GetFileContent(filepath)
    svg = Tag()
    svg.load(svgContent)

    # Edit svg content
    svg.removeTag('style')
    svg.applyStyles()
    #svg.removeTags(['style', 'stop'])
    #svg.keepAttributes('path', ['id', 'd'])
    #svg.removeAttributes('path', ['id'])

    # Convert & parse react-native format
    svg = SvgToRN(svg)
    if svg is None: continue

    # Save new svg content
    SaveFileContent(newFilePath, str(svg))

printFullLine()