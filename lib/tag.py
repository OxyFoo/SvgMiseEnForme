# Generated by Github Copilot (except parse functions)

from lib.config import Config
from lib.utils import Debug, getStringBetween

class Tag:
    '''
    A tag in a SVG file.
    '''

    def __init__(self, parent = None):
        '''
        Initialize a tag.

        Parameters
        ----------
        parent : Tag|None
            The parent of the tag.
        '''

        self.parent = parent
        self.tag = None
        self.attributes = {}
        self.children = []
        #self.parse(content)

    def __str__(self):
        '''
        Return the string representation of the tag.
        '''
        if self.tag is None:
            Debug(1, 'Error: tag not initialized')
            #print(self.tag)
            #print('- Attrib: ' + self.attributes.__str__())
            #print('- Childs: ' + str(len(self.getChildren())))
            return ''

        attributes = ['']
        for key in self.attributes:
            attributes.append(key + '="' + self.attributes[key] + '"')
        attributes = ' '.join(attributes)
        children = ''.join([str(child) for child in self.getChildren()])

        #print(self.tag)
        #print('- Attrib: ' + attributes)
        #print('- Childs: ' + str(len(self.getChildren())))

        if self.tag in Config.openTag:
            return '<' + self.tag + attributes + '>' + children + '</' + self.tag + '>'
        return '<' + self.tag + attributes + '/>'

    def addAttribute(self, name, value):
        '''
        Add an attribute to the tag.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : str
            The value of the attribute.
        '''
        self.attributes[name] = value

    def addChild(self, child):
        '''
        Add a child to the tag.

        Parameters
        ----------
        child : Tag
            The child to add.
        '''
        self.children.append(child)

    def parse(self, content):
        '''
        Parse the content of the tag.

        Parameters
        ----------
        content : str
            The content of the tag.
        '''

        while content:
            Debug(2, '-------------------')

            content = content.strip()
            firstTagInfo = getStringBetween(content, '<', ' ', False)
            if firstTagInfo is None: # No tag found
                Debug(1, 'Error: tag not found')
                Debug(1, 'Content: ' + content)
                return

            firstTag = firstTagInfo['content']
            Debug(2, '- ' + firstTag + ' (' + ('is open' if firstTag in Config.openTag else 'not open') + ')')
            #Debug(2, 'Current: ' + content)

            if firstTag in Config.openTag:
                tagAttributes = getStringBetween(content, '<' + firstTag, '>', False)
                tagContent = getStringBetween(content[firstTagInfo['pos'] + len(firstTag) + 1:], '>', '</' + firstTag + '>', False)
                if tagAttributes is None or tagContent is None:
                    Debug(1, 'Error: tag not found or attributes not found')
                    return

                Debug(2, 'Attr: ' + tagAttributes['content'])
                Debug(2, 'Cont: ' + tagContent['content'])
                Debug(2, 'Prnt: ' + str(self.parent))

                self.tag = firstTag
                self.parseAttributes(tagAttributes['content'])

                if firstTag in Config.keepTag:
                    newTag = Tag(self)
                    newTag.parse(tagContent['content'])
                    self.addChild(newTag)

                # Get remain content
                tagFull = getStringBetween(content, '<' + firstTag, '</' + firstTag + '>', True)
                if tagFull is None:
                    Debug(1, 'Error: tagFull is None')
                    return
                content = content.replace(tagFull['content'], '', 1)
                Debug(2, 'Remove: ' + tagFull['content'])
            else:
                newTag = Tag(self)
                newTag.tag = firstTag

                tagAttributes = getStringBetween(content, '<' + firstTag, '/>', False)
                if tagAttributes is None:
                    Debug(1, 'Error: tag not found or attributes not found')
                    return

                Debug(2, 'Cont:' + content)
                Debug(2, 'Attr: ' + tagAttributes['content'])
                Debug(2, 'Prnt: ' + str(self.parent))

                newTag.parseAttributes(tagAttributes['content'])
                self.parent.addChild(newTag)

                # Get remain content
                tagFull = getStringBetween(content, '<' + firstTag, '/>', True)
                if tagFull is None:
                    Debug(1, 'Error: tagFull is None')
                    return
                content = content.replace(tagFull['content'], '', 1)
                Debug(2, 'Remove: ' + tagFull['content'])

    def parseAttributes(self, content):
        '''
        Parse the attributes of the tag.

        Parameters
        ----------
        content : str
            The content of the tag.
        '''
        while content:
            content = content.strip()
            attribute = content.split('=')[0].split(' ')[-1]
            info = getStringBetween(content, attribute + '="', '"', False)
            if info is None: break
            self.addAttribute(attribute, info['content'])
            content = content.replace(attribute + '="' + info['content'] + '"', '')

    def getAttribute(self, name):
        '''
        Get the value of an attribute.

        Parameters
        ----------
        name : str
            The name of the attribute.

        Returns
        -------
        str
            The value of the attribute.
        '''
        return self.attributes[name]

    def getChildren(self):
        '''
        Get the children of the tag.

        Returns
        -------
        list
            The children of the tag.
        '''
        return self.children