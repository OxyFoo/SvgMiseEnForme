from lib.config import Config
from lib.style import Style
from lib.utils import getStringBetween
from lib.debug import Debug

class Tag:
    '''
    A tag in a SVG file.
    '''

    def __init__(self):
        '''
        Initialize a tag.
        '''

        self.tag = None
        self.attributes = {}
        self.children: list[Tag] = []
        self.isOpen = False

    def __str__(self, level=0):
        '''
        Return the string representation of the tag.

        Parameters
        ----------
        level : int
            The level of the tag, use to indent the string.
        '''

        if self.tag is None:
            Debug.Error('Tag not initialized')
            return ''

        # Get self attributes & children
        attributes = ['']
        for key in self.attributes:
            attributes.append(key + '="' + self.attributes[key] + '"')
        attributes = ' '.join(attributes)
        children = ''.join([child.__str__(level=level+1) for child in self.__getChildren()])

        # Get indentation
        ident = ''
        endLine = ''
        if Config.identSpace is not None:
            ident = Config.identSpace * level
            endLine = '\n'

        # Open tag
        if self.isOpen:
            selfTag = ident + '<' + self.tag + attributes + '>' + endLine
            selfTagClose = ident + '</' + self.tag + '>' + endLine
            return selfTag + children + selfTagClose

        # Close tag
        return ident + '<' + self.tag + attributes + '/>' + endLine

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

    def getAttribute(self, name) -> str:
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

        if name in self.attributes:
            return self.attributes[name]
        return None

    def remAttribute(self, name):
        '''
        Remove an attribute from the tag.

        Parameters
        ----------
        name : str
            The name of the attribute to remove, if it exists.
        '''

        if name in self.attributes:
            del self.attributes[name]

    def __addChild(self, child):
        '''
        Add a child to the tag.

        Parameters
        ----------
        child : Tag
            The child to add.
        '''
        self.children.append(child)

    def __getChildren(self):
        '''
        Get the children of the tag.

        Returns
        -------
        list[Tag]
            The children of the tag.
        '''
        return self.children

    def removeTag(self, tagName):
        '''
        Remove all tags with the given name.

        Parameters
        ----------
        tagName : str
            The name of the tag to remove.
        '''

        for child in self.__getChildren()[::-1]:
            if child.tag == tagName:
                self.children.remove(child)
            elif child.isOpen:
                child.removeTag(tagName)

    def removeTags(self, tagsName):
        '''
        Remove all tags with the given name.

        Parameters
        ----------
        tagName : list
            The name of the tags to remove.
        '''

        for tag in tagsName:
            self.removeTag(tag)

    def keepAttributes(self, tagName, attributes):
        '''
        Keep only the attributes of the tag.
        Remove the attributes not in the list.

        Parameters
        ----------
        tagName : str
            The tagName to keep the attributes.
        attributes : list
            The attributes to keep.
        '''

        for child in self.__getChildren():
            if child.tag == tagName:
                attributeKeys = list(child.attributes.keys())
                for attribute in attributeKeys:
                    if attribute not in attributes:
                        child.remAttribute(attribute)
            if child.isOpen:
                child.keepAttributes(tagName, attributes)

    def removeAttributes(self, tagName, attributes):
        '''
        Remove the attributes of the tag.

        Parameters
        ----------
        tagName : str
            The tagName to keep the attributes.
        attributes : list
            The attributes to keep.
        '''

        for child in self.__getChildren():
            if child.tag == tagName:
                for attribute in attributes:
                    child.remAttribute(attribute)
            if child.isOpen:
                child.removeAttributes(tagName, attributes)

    def load(self, content):
        '''
        Load the tag from the content.

        Parameters
        ----------
        content : str
            The content of the tag.
        '''

        Style.reset()
        self.__parse(content)
        Debug.Info('SVG parsed')

    def __parse(self, content):
        '''
        Parse the content of the tag.

        Parameters
        ----------
        content : str
            The content of the tag.

        Algorithm
        ---------
        - Get tag & attributes
        - Get all main groups in self content
        - For each group, add empty child tag
                - Parse group content
        '''

        # Get tag informations
        tagInfo = getStringBetween(content, '<', ' ', False)
        if tagInfo is None:
            Debug.Error('Tag not found')
            Debug.Log('Content: ' + content)
            return

        # Set tag
        tag = tagInfo['content']
        self.tag = tag
        self.isOpen = Tag.__tagIsOpen(tag, content)
        Debug.Log('- ' + tag + ' (' + ('is open' if self.isOpen else 'not open') + ')')

        # Get attributes
        tagAttributesInfo = getStringBetween(content, '<' + tag, '>', False)
        if tagAttributesInfo is None:
            Debug.Error('Attributes not found')
            return

        # Set attributes
        tagAttributes = tagAttributesInfo['content']
        self.__parseAttributes(tagAttributes)
        Debug.Log('Attr: ' + tagAttributes)

        # Get children from content for open tags
        if self.isOpen:
            # Get content
            tagContentInfo = getStringBetween(content[tagInfo['pos'] + len(tag) + 1:], '>', '</' + tag + '>', False)
            if tagContentInfo is None:
                Debug.Error('Tag content not found')
                return

            tagContent = tagContentInfo['content']
            Debug.Log('Cont: ' + tagContent)

            if tag == 'style':
                Style.parse(tagContent)
                return

            # Get all groups
            while tagContent:
                Debug.Log('-------------------')
                tagContent = tagContent.strip()

                # Get first tag
                childTagInfo = getStringBetween(tagContent, '<', ' ', False)
                if childTagInfo is None:
                    Debug.Error('Child tag not found')
                    return

                # Get all first child content
                childTag = childTagInfo['content']
                childTagIsOpen = Tag.__tagIsOpen(childTag, tagContent)
                childTagFullInfo = None

                if childTagIsOpen:
                    childTagFullInfo = getStringBetween(tagContent, '<' + childTag, '</' + childTag + '>', True)
                else:
                    childTagFullInfo = getStringBetween(tagContent, '<' + childTag, '/>', True)
                if childTagFullInfo is None:
                    Debug.Error('TagFull is None ({} childTag: {})'.format('open' if childTagIsOpen else 'not open', childTag))
                    return

                # Add child tag to self
                childTag = childTagFullInfo['content']
                newTag = Tag()
                newTag.__parse(childTag)
                self.__addChild(newTag)

                # Remove child tag from content
                tagContent = tagContent.replace(childTag, '', 1)
                Debug.Log('Remove: ' + childTag)

    def __parseAttributes(self, content):
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

    def __tagIsOpen(tagName, content):
        '''
        Check if the tag is open.

        Parameters
        ----------
        tagName : str
            The name of the tag.
        content : str
            The content of the tag.

        Returns
        -------
        bool
            True if the tag is open, False otherwise.
        '''

        tagName = '<' + tagName
        newContent = content.split(tagName)[1].split('>')[0].strip()
        return not newContent.endswith('/')

    def applyStyles(self):
        '''
        Apply the styles to the tags.
        '''

        for child in self.__getChildren():
            className = child.getAttribute('class')
            if className is not None and className in Style.styles:
                attributes = Style.styles[className]
                for attribute in attributes:
                    child.addAttribute(attribute, attributes[attribute])
                child.remAttribute('class')
            child.applyStyles()
