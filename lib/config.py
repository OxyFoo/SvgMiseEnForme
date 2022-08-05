class Config:
    '''
    Configuration class.
    '''

    DEBUG_LEVEL = 2
    '''
    Debug level.
    0: No debug
    1: Debug -> Errors / warnings
    2: Debug + verbose
    '''

    openTag = [
        'svg',
        'style',
        'g',
        'linearGradient'
    ]
    keepTag = [
        'svg',
        'g',
        'linearGradient',
        'path',
        'rect',
        'circle',
        'ellipse',
        'polygon',
        'polyline',
        'line',
        'text',
        'tspan',
        'textPath',
        'tref',
        'title',
        'desc',
        'metadata',
        'defs',
        'symbol',
        'use',
        'image',
        'pattern',
        'mask',
        'clipPath',
        'filter'
    ]
    keepAttributes = {
        'svg': [
            'xmlns',
            'viewBox'
        ]
    }