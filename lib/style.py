from lib.utils import getStringBetween

class Style:
    styles = {}

    def reset():
        Style.styles = {}

    def parse(content):
        while content:
            content = content.strip()
            styleClassInfo = getStringBetween(content, '.', '}')
            if styleClassInfo is None:
                break

            styleClass = styleClassInfo['content']
            styleClassNameInfo = getStringBetween(styleClass, '.', '{', False)
            if styleClassNameInfo is None:
                break

            styleClassName = styleClassNameInfo['content']
            styleClassContent = styleClass.split('{')[1].split('}')[0]

            properties = {}
            for p in styleClassContent.split(';'):
                p = p.strip()
                if not p or not ':' in p: continue

                propertyName = p.split(':')[0].strip()
                propertyValue = p.split(':')[1].strip()
                properties[propertyName] = propertyValue

            Style.styles[styleClassName] = properties
            content = content.replace(styleClass, '', 1)

    def getAttributes(className):
        if className in Style.styles:
            return Style.styles[className]
        return None
