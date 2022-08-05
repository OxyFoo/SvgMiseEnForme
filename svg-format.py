import os
from lib.tag import Tag
from lib.utils import printFullLine

# Config
dirRaw = './raw'
dirSvg = './svg'

# Directories & files verifications
if not os.path.isdir(dirRaw):   os.mkdir(dirRaw)
if not os.listdir(dirRaw):      exit('Directory "' + dirRaw + '" is empty.\nAborted...')
if not os.path.isdir(dirSvg):   os.mkdir(dirSvg)
if os.listdir(dirSvg):
    response = input('Directory "' + dirSvg + '" is not empty, remove all files ? (y/N) : ')
    if response.lower() != 'y': exit('Aborted...')
    for file in os.listdir(dirSvg):
        os.remove(dirSvg + '/' + file)



printFullLine()

svgFiles = os.listdir(dirRaw)
for filename in svgFiles:
    filepath = os.path.join(dirRaw, filename)
    if not filepath.endswith(".svg"): continue
    if not os.path.isfile(filepath): continue

    print('Processing file "' + filename + '"')

    # Get file content
    svgFile = open(filepath, 'rb')
    svgContent = svgFile.read()
    svgContent = svgContent.decode('utf8')
    svgFile.close()

    # Remove useless lines
    removeChars = [ '\n', '\r', '\t' ]
    for char in removeChars:
        svgContent = svgContent.replace(char, '')

    # Parse file content
    svg = Tag()
    svg.parse(svgContent)
    #svg.removeUnusedTags()

    # Save the new file
    svgFile = open(os.path.join(dirSvg, filename), 'w')
    svgFile.write(str(svg))
    svgFile.close()

printFullLine()