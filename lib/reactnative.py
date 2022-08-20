import json
import requests

from lib.utils import Debug

PAYLOAD_PATH = './lib/payload.json'
URL = 'https://api.react-svgr.com/api/svgr'
USER_AGENT = 'Mozilla/5.0 (X11; CrOS aarch64 15048.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
PAYLOAD = {}

def GetPayload(code):
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

def ConvertSvgToRN(svg):
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
            Debug(0, 'SVG converted to RN format')
            return output['output']
        else:
            Debug(0, 'Error: SVG conversion failed')
            Debug(1, response.status_code)
    except Exception as e:
        Debug(0, 'Error: SVG conversion failed')
        Debug(1, e)

    return None

def ParseRNSvg(rn):
    '''
    Parse react native text: remove comments, empty and useless lines
    And sort code by body parts

    Parameters
    ----------
    rn : str
        The react native text.
    '''

    lines = rn.split('\n')
    output = lines[4:-5]
    output = '\n'.join(output)

    Debug(0, 'New SVG parsed')

    return output

def SvgToRN(svg):
    return svg