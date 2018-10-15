import xml.etree.ElementTree as ET
from xml.dom import minidom


def reader(path_to_file):
    # type: (str) -> str
    """
    Reads an XML-like file and returns the content of the text tag
    :rtype: str
    :return: the text requested as a string
    :param path_to_file: name of the file to be red
    """
    with open(path_to_file, 'rb') as file:
        tree = ET.parse(file)
    root = tree.getroot()
    return tree.find(".//TEXT").text


def writer(tree):
    # type: (ET.ElementTree) -> str
    """
    Writes a XML tree into a file
    :rtype: str
    :return: the xml file requested as a string
    :param tree: tree to be written into the file
    """
    # root = ET.Element("TimeML")
    # items = ET.SubElement(root, 'items')
    # item1 = ET.SubElement(items, 'item')
    # item2 = ET.SubElement(items, 'item')
    # tree = ET.ElementTree(root)
    string = ET.tostring(tree.getroot(),
                         encoding='utf-8',
                         method="xml")
    return prettify(string)

    # string_tree = ET.tostring(tree)
    # myfile = open(filename, "w")
    # myfile.write(string_tree)


def prettify(string):
    # type: (str) -> str
    """
    Rewrite the xml files in a more human-readable format
    :rtype: str
    :return: the xml file requested well formatted
    :param string: xml to be prettified as a string
    """
    xml = minidom.parseString(string)
    pretty_xml_as_string = xml.toprettyxml(encoding='utf8')
    return pretty_xml_as_string


def saveFile(filename, tree):
    # type: (str, ET.ElementTree) -> None
    """
    Saves a tree to a file
    :param filename: name of the file to be saved
    :param tree: tree to print
    """
    content = writer(tree)
    with open(filename, "w") as f:
        f.write(content)


def createTimeML():
    # type: () -> ET.ElementTree
    """
    Creates an empty TIMEML tree
    :return: the created tree
    """
    root = ET.Element("TimeML")
    tree = ET.ElementTree(root)
    return tree


def addItem(tree, char_begin, char_end, type, content):
    # type: (ET.ElementTree, int, int, str, str) -> None
    """
    Adds an item to the given tree
    :param tree: tree to which we can add the item
    :param char_begin: number of the first char of the content in the text
    :param char_end: number of the last char of the content in the text
    :param type: type of time occurrence
    :param content: string extracted from the text
    """
    timeX3 = ET.SubElement(tree.getroot(), 'TIMEX3')
    # timeX3.set('attribute', 'value')
    timeX3.set('char_begin', str(char_begin))
    timeX3.set('char_end', str(char_end))
    timeX3.set('type', type)
    # not required
    timeX3.set('tid', "")
    timeX3.set('value', "")
    timeX3.text = content


#print reader("data/train/input/train_01.input.tml")
#test_tree = createTimeML()
#addItem(test_tree, 10, 13, 'dddd', 'ciao')
#saveFile("prova", test_tree)
#print writer(test_tree)
