#XMLMatcher
import xml.etree.ElementTree as ET
from XMLparsing.XMLparser import *

def list_creator(path_to_file):
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
    list1 = []
    for child in root:
        list1.append((child.text, child.get("type"), child.get("char_begin"), child.get("char_end")))
    return list1

def list_compare_strict(list1,list2):
    cnt=0
    for elem1 in list1:
        for elem2 in list2:
            if elem1==elem2:
                cnt = cnt + 1
    return cnt

file1=list_creator('/home/fabio/Documenti/ComputationalLingiusticProjects/data/train/annotated/train_01.gold.tml')
file2=list_creator('/home/fabio/Documenti/ComputationalLingiusticProjects/train_output.tml')

#print file2
print 'NUMBER OF EXPRESSIONS OF ORIGINAL GOLD STANDARD:'
print length(file1)
print 'NUMBER OF EXPRESSIONS OF OUR GOLD STANDARD:'
print length(file2)
print 'NUMBER OF MATCHED TIME EXPRESSIONS IS:'
print list_compare_strict(file1,file2)
#print file1

