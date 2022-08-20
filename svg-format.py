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
from lib.utils import Debug, GetFileContent, SaveFileContent, Init, defineHandler, printFullLine
from lib.reactnative import SvgToRN

# Config
Config.clearOnStart = True
Config.dirRaw = './raw'
Config.dirSvg = './svg'
Config.DEBUG_LEVEL = 1
Config.identSpace = '    '
Config.convertToRN = True

Init()
defineHandler()
Config.CheckFolders()



startTime = os.times()
printFullLine()

svgFiles = os.listdir(Config.dirRaw)
for filename in svgFiles:
    # Get svg content
    svgContent = GetFileContent(filename)
    if svgContent is None: continue

    # Parse svg content
    svg = Tag()
    svg.load(svgContent)

    # Edit svg content
    svg.removeTag('style')
    svg.applyStyles()
    #svg.removeTags(['style', 'stop'])
    #svg.keepAttributes('path', ['id', 'd'])
    #svg.removeAttributes('path', ['id'])

    # Convert & parse react-native format
    if Config.convertToRN:
        svg = SvgToRN(svg)
        if svg is None: continue

    # Save new svg content
    SaveFileContent(filename, str(svg))

printFullLine()
endTime = os.times()
elapsedTime = round(endTime[0] - startTime[0], 2)
Debug(0, 'SVG files parsed in {} seconds'.format(elapsedTime))