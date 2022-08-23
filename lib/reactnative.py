import json
import requests

from lib.tag import Tag
from lib.utils import getStringBetween
from lib.debug import Debug

PAYLOAD_PATH = './lib/payload.json'
URL = 'https://api.react-svgr.com/api/svgr'
USER_AGENT = 'Mozilla/5.0 (X11; CrOS aarch64 15048.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
PAYLOAD = {}

BODY_PARTS = [
    'left_ear',
    'left_eye',
    'left_eyebrow',
    'right_ear',
    'right_eye',
    'right_eyebrow',
    'nose',
    'mouth',
    'head',
    'bust',
    'left_arm',
    'left_forearm',
    'left_hand',
    'right_arm',
    'right_forearm',
    'right_hand',
    'left_thigh',
    'left_leg',
    'left_foot',
    'right_thigh',
    'right_leg',
    'right_foot'
]
BODY_PART_OUTLINE = '_outline'

def getPayload(code: str) -> dict:
    '''
    Get payload for the request with code.

    Parameters
    ----------
    code : str
        The svg content.
    '''

    global PAYLOAD

    # Get payload from file if not already done
    if PAYLOAD == {}:
        f = open(PAYLOAD_PATH, 'r')
        if f is None:
            Debug.Error('Payload file not found')
        PAYLOAD = json.load(f)
        f.close()

    newPayload = PAYLOAD.copy()
    newPayload['code'] = code
    return newPayload

def convertSvgToRN(svg: str):
    '''
    Convert svg text to react-native text.

    Parameters
    ----------
    svg : str
        The svg text.

    Returns
    -------
    str
        The react-native text or None if failed.
    '''

    payload = getPayload(svg)

    try:
        response = requests.post(URL, json=payload, headers={'User-Agent': USER_AGENT})
        if response.status_code == 200:
            output = response.json()
            return output['output']
        else:
            Debug.Error('SVG conversion failed ({})'.format(response.status_code))
    except Exception as e:
        Debug.Error('SVG conversion failed')
        Debug.Error(e)

    return None

def isBodyPart(id: str):
    if id in BODY_PARTS:
        return True
    if id.endswith(BODY_PART_OUTLINE) and id[:-len(BODY_PART_OUTLINE)] in BODY_PARTS:
        return True
    return False

def SvgToRN(svg: Tag):
    bodyParts = {}
    bodyOutlines = {}

    # Count parts to convert
    current = 0
    total = 0
    for child in svg.children:
        id = child.getAttribute('id')
        if isBodyPart(id):
            total += 1
        else:
            Debug.Warn('Group "{}" is not body part!'.format(id))

    if total == 0:
        Debug.Warn('No body parts found, abort this file')
        return None

    for child in svg.children:
        id = child.getAttribute('id')
        if isBodyPart(id):
            current += 1
            print('', end='\r')
            Debug.Info('SVG->RN conversion part: {}/{}'.format(current, total), end='')

            rn = convertSvgToRN('<svg>' + str(child) + '</svg>')
            rn = rn.replace('\n', '')
            contentInfo = getStringBetween(rn, '<G', '</G>', True)
            if contentInfo is None:
                print()
                Debug.Error('Body part "{}" not found'.format(id))
                continue
            if not id.endswith(BODY_PART_OUTLINE):
                bodyParts[id] = contentInfo['content']
            else:
                bodyOutlines[id[:-len(BODY_PART_OUTLINE)]] = contentInfo['content']
    print()
    Debug.Info('SVG->RN conversion done')

    # Get tags
    allTags = []
    allParts = { **bodyParts, **bodyOutlines }
    for part in allParts:
        tag = ''
        readTag = False
        content = allParts[part]

        for character in content:
            if character == '<':
                readTag = True
                continue
            if readTag and character == '/':
                tag = ''
                readTag = False
                continue
            if readTag and character == ' ':
                if not tag in allTags:
                    allTags.append(tag)
                readTag = False
                tag = ''
                continue
            if readTag:
                tag += character
                continue

    # Make header
    header = "import * as React from 'react';\n"
    header += "import { " + ', '.join(allTags) + " } from 'react-native-svg';"

    # Make body
    body = 'const component = {\n'
    body += '    svg: {\n        '
    body += ',\n        '.join(['{}: {}'.format(part, bodyParts[part]) for part in bodyParts])
    body += '\n    },\n'
    body += '    outline: {\n        '
    body += ',\n        '.join(['{}: {}'.format(part, bodyOutlines[part]) for part in bodyOutlines])
    body += '\n    }\n'
    body += '}'

    # Make footer
    footer = 'export default component;'

    return header + '\n\n' + body + '\n\n' + footer