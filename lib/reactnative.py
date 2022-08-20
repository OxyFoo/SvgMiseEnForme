import json
import requests

from lib.tag import Tag
from lib.utils import Debug, getStringBetween

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

def GetPayload(code: str) -> dict:
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
            Debug(1, 'Error: Payload file not found')
        PAYLOAD = json.load(f)
        f.close()

    newPayload = PAYLOAD.copy()
    newPayload['code'] = code
    return newPayload

def ConvertSvgToRN(svg: str):
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

    payload = GetPayload(svg)

    try:
        response = requests.post(URL, json=payload, headers={'User-Agent': USER_AGENT})
        if response.status_code == 200:
            output = response.json()
            return output['output']
        else:
            Debug(0, 'Error: SVG conversion failed')
            Debug(1, response.status_code)
    except Exception as e:
        Debug(0, 'Error: SVG conversion failed')
        Debug(1, e)

    return None

def SvgToRN(svg: Tag):
    bodyParts = {}

    # Count parts to convert
    current = 0
    total = 0
    for child in svg.children:
        id = child.getAttribute('id')
        if id in BODY_PARTS:
            total += 1

    if total == 0:
        Debug(1, 'Error: No body parts found, abort this file')
        return None

    for child in svg.children:
        id = child.getAttribute('id')
        if id in BODY_PARTS:
            current += 1
            print('\rSVG->RN conversion part: {}/{}'.format(current, total), end='')

            rn = ConvertSvgToRN('<svg>' + str(child) + '</svg>')
            rn = rn.replace('\n', '')
            contentInfo = getStringBetween(rn, '<G', '</G>', True)
            if contentInfo is None: continue
            bodyParts[id] = contentInfo['content']
    Debug(0, 'SVG->RN conversion done')
    print()

    # Get tags
    allTags = []
    for part in bodyParts:
        tag = ''
        readTag = False
        content = bodyParts[part]

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
    body += '    svg: {\n'
    for part in bodyParts:
        content = bodyParts[part]
        body += '        ' + part + ': ' + content + ',\n'
    body += '    }\n'
    body += '}'

    # Make footer
    footer = 'export default component;'

    return header + '\n\n' + body + '\n\n' + footer