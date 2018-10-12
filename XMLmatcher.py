#XMLMatcher
import xml.etree.ElementTree as ET
from XMLparsing.XMLparser import *

def list_creator(path_to_file):
    # type: (str) -> str
    """
    Reads an XML-like file and returns a list of tuples
    made of the text and the values in each TIMEX3 tag.
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

def list_compare_relaxed(list1,list2):
    cnt=0
    to_not_be_seen_postitions_list1=[]
    to_not_be_seen_postitions_list2=[]
    for num1 in range(len(list1)):
        for num2 in range(len(list2)):
            if list1[num1]==list2[num2] and num1 not in to_not_be_seen_postitions_list1 and num2 not in to_not_be_seen_postitions_list2:
                cnt = cnt+1
                to_not_be_seen_postitions_list1.append(num1)
                to_not_be_seen_postitions_list2.append(num2)
    '''
    RICORDATI DI FARE LA CORREZIONE PER CUI DEVI PRIMA SCEGLIERE IL MATCH PIU' GRANDE!!!!!!!!!!!
    '''
    for num1 in range(len(list1)):
        begin_1 = int(list1[num1][2])
        end_1 = int(list1[num1][3])
        for num2 in range(len(list2)):
            begin_2 = int(list2[num2][2])
            end_2 = int(list2[num2][3])

            overlap = (begin_1<=begin_2 and end_1>=end_2) or (begin_2<=begin_1 and end_2>=end_1) or \
                      (begin_1<=begin_2<=end_1) or (begin_2<=begin_1<=end_2) or \
                      (begin_1<=end_2<=end_1) or (begin_2<=end_1<=end_2)


            if list1[num1][1]==list2[num2][1] and overlap:
                cnt = cnt + 1
                to_not_be_seen_postitions_list1.append(num1)
                to_not_be_seen_postitions_list2.append(num2)
    return cnt
'''
file1=list_creator('/home/fabio/Documenti/ComputationalLingiusticProjects/data/train/annotated/train_01.gold.tml')
file2=list_creator('/home/fabio/Documenti/ComputationalLingiusticProjects/train_output.tml')

#print file2
print 'NUMBER OF EXPRESSIONS OF ORIGINAL GOLD STANDARD:'
print len(file1)
print 'NUMBER OF EXPRESSIONS OF OUR GOLD STANDARD:'
print len(file2)
print 'NUMBER OF MATCHED TIME EXPRESSIONS IS:'
print list_compare_relaxed(file1 , file2)
#print file1
'''

def counter_matches(original_file_path, my_file_path):
    '''Creating lists of elements from file path'''
    or_file = list_creator(original_file_path)
    my_file = list_creator(my_file_path)
    '''Counting the number of expression on each file and the number of matches'''
    nr_original_expressions = len(or_file)
    nr_my_expressions = len(my_file)
    nr_strict_matches = list_compare_strict(or_file,my_file)
    nr_relaxed_matches = list_compare_relaxed(or_file,my_file)

    return nr_original_expressions , nr_my_expressions , nr_strict_matches , nr_relaxed_matches

