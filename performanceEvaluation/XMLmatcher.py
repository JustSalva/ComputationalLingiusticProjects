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
        list1.append((child.text, child.get("type"), child.get("char_begin"), child.get("char_end"),child.get("tid")))
    return list1

def list_compare_strict(list_old,list_new):
    '''It takes the two string of expressions and counts how many matches strictly.
    list1 should correspond to the original gold standard file, list2 to our output file.'''
    print "STRICT MATCHING CALLED:"
    cnt=0
    to_not_be_seen_positions_list_new = []
    to_not_be_seen_positions_list_old = []
    for num_old in range(len(list_old)):
        for num_new in range(len(list_new)):
            if list_old[num_old][0:4]==list_new[num_new][0:4]:
                cnt = cnt + 1
                to_not_be_seen_positions_list_new.append(num_new)
                to_not_be_seen_positions_list_old.append(num_old)
    """This part is for matching the expressions as YYYY-YYYY, I do search for elements in old list,
    the I repeat again for old list. If tid is the same, I look for the union on new list, plus an overlap 
    check.
    """
    for num_old_1 in range(len(list_old)):
        if '1000'<=list_old[num_old_1][0]<='2020' and list_old[num_old_1][1]=="DURATION" and num_old_1 not in to_not_be_seen_positions_list_old:
            for num_old_2 in range(len(list_old)):
                begin_old_2 = int(list_old[num_old_2][2])
                end_old_2 = int(list_old[num_old_2][3])
                if list_old[num_old_1][0]!=list_old[num_old_2][0] and list_old[num_old_2][1]=="DURATION" and list_old[num_old_2][4]==list_old[num_old_1][4] and num_old_2 not in to_not_be_seen_positions_list_old:
                    for num_new in range(len(list_new)):
                        begin_new = int(list_new[num_new][2])
                        end_new = int(list_new[num_new][3])
                        overlap = (begin_old_2 <= begin_new and end_old_2 >= end_new) or (
                                    begin_new <= begin_old_2 and end_new >= end_old_2) or \
                                  (begin_old_2 <= begin_new <= end_old_2) or (begin_new <= begin_old_2 <= end_new) or \
                                  (begin_old_2 <= end_new <= end_old_2) or (begin_new <= end_old_2 <= end_new)
                        if list_new[num_new][0]==str(list_old[num_old_1][0])+"-"+str(list_old[num_old_2][0]) and list_new[num_new][1]=="DURATION" and overlap and num_new not in to_not_be_seen_positions_list_new:
                            print "MATCHING AN YEAR INTERVAL!"
                            cnt = cnt + 1
                            to_not_be_seen_positions_list_old.append(num_old_1)
                            to_not_be_seen_positions_list_old.append(num_old_2)
                            to_not_be_seen_positions_list_new.append(num_new)
                            print list_old[num_old_1]
                            print list_old[num_old_2],"\n MATCHES"
                            print list_new[num_new]

    for num_new in range(len(list_new)):
        if num_new not in to_not_be_seen_positions_list_new:
                print "NOT MATCHED IN OUR FILE: ",list_new[num_new]
    for num_old in range(len(list_old)):
        if num_old not in to_not_be_seen_positions_list_old:
                print "NOT MATCHED IN ORIGINAL FILE: ",list_old[num_old]
    print "cnt is:", cnt
    return cnt

def list_compare_relaxed(list_old,list_new):
    '''It takes the two string of expressions and counts how many matches relaxedly.
    list1 should correspond to the original gold standard file, list2 to our output file.'''
    print "RELAXED MATCHING CALLED:"
    cnt=0
    to_not_be_seen_positions_list_old=[]
    to_not_be_seen_positions_list_new=[]
    '''First of all strict matches must be counted and excluded for future matching'''
    for num_old in range(len(list_old)):
        for num_new in range(len(list_new)):
            if list_old[num_old][0:4]==list_new[num_new][0:4]:
                cnt = cnt + 1
                to_not_be_seen_positions_list_new.append(num_new)
                to_not_be_seen_positions_list_old.append(num_old)
    """This part is for matching the expressions as YYYY-YYYY, I do search for elements in old list,
    the I repeat again for old list. If tid is the same, I look for the union on new list, plus an overlap 
    check.
    """
    for num_old_1 in range(len(list_old)):
        if '1000'<=list_old[num_old_1][0]<='2020' and list_old[num_old_1][1]=="DURATION" and num_old_1 not in to_not_be_seen_positions_list_old:
            for num_old_2 in range(len(list_old)):
                begin_old_2 = int(list_old[num_old_2][2])
                end_old_2 = int(list_old[num_old_2][3])
                if list_old[num_old_1][0]!=list_old[num_old_2][0] and list_old[num_old_2][1]=="DURATION" and list_old[num_old_2][4]==list_old[num_old_1][4] and num_old_2 not in to_not_be_seen_positions_list_old:
                    for num_new in range(len(list_new)):
                        begin_new = int(list_new[num_new][2])
                        end_new = int(list_new[num_new][3])
                        overlap = (begin_old_2 <= begin_new and end_old_2 >= end_new) or (
                                    begin_new <= begin_old_2 and end_new >= end_old_2) or \
                                  (begin_old_2 <= begin_new <= end_old_2) or (begin_new <= begin_old_2 <= end_new) or \
                                  (begin_old_2 <= end_new <= end_old_2) or (begin_new <= end_old_2 <= end_new)
                        if list_new[num_new][0]==str(list_old[num_old_1][0])+"-"+str(list_old[num_old_2][0]) and list_new[num_new][1]=="DURATION" and overlap and num_new not in to_not_be_seen_positions_list_new:
                            print "MATCHING AN YEAR INTERVAL!"
                            cnt = cnt + 1
                            to_not_be_seen_positions_list_old.append(num_old_1)
                            to_not_be_seen_positions_list_old.append(num_old_2)
                            to_not_be_seen_positions_list_new.append(num_new)
                            print list_old[num_old_1]
                            print list_old[num_old_2],"\n MATCHES"
                            print list_new[num_new]

    '''Now we check the positions of expressions. Overlap variable is used to check char_begin and 
    char_end. max_length is used to memorize which is the longest variable to match in my expressions,
    in order to match with maximal length.'''
    for num_new in range(len(list_new)):
        begin_new = int(list_new[num_new][2])
        end_new = int(list_new[num_new][3])
        max_length = 0
        memo = None
        for num_old in range(len(list_old)):
            begin_old = int(list_old[num_old][2])
            end_old = int(list_old[num_old][3])
            #overlap is used to know if there is overlapping between two expressions according to char_begin and char_end
            overlap = (begin_old<=begin_new and end_old>=end_new) or (begin_new<=begin_old and end_new>=end_old) or \
                      (begin_old<=begin_new<=end_old) or (begin_new<=begin_old<=end_new) or \
                      (begin_old<=end_new<=end_old) or (begin_new<=end_old<=end_new)
            if list_old[num_old][1]==list_new[num_new][1] and overlap and num_old not in to_not_be_seen_positions_list_old and num_new not in to_not_be_seen_positions_list_new:
                current_length = len(list_old[num_old][0].split())
                max_length = max(max_length, current_length)
                if max_length==current_length:
                    memo = num_old
        if memo!=None:
            cnt = cnt + 1
            to_not_be_seen_positions_list_old.append(memo)
            to_not_be_seen_positions_list_new.append(num_new)
            print list_old[memo],"MATCHES", list_new[num_new]
    for num_new in range(len(list_new)):
        if num_new not in to_not_be_seen_positions_list_new:
                print "NOT MATCHED IN OUR FILE: ",list_new[num_new]
    for num_old in range(len(list_old)):
        if num_old not in to_not_be_seen_positions_list_old:
                print "NOT MATCHED IN ORIGINAL FILE: ",list_old[num_old]
    return cnt

'''
file1=list_creator('/home/fabio/Documenti/ComputationalLingiusticProjects/data/train/annotated/train_05.gold.tml')
file2=list_creator('/home/fabio/Documenti/ComputationalLingiusticProjects/result/train/train_05.output.tml')

#print file2
print 'NUMBER OF EXPRESSIONS OF ORIGINAL GOLD STANDARD:'
print len(file1)
print 'NUMBER OF EXPRESSIONS OF OUR GOLD STANDARD:'
print len(file2)
print 'NUMBER OF MATCHED TIME EXPRESSIONS IS:'
print list_compare_strict(file1 , file2)
print 'NUMBER OF MATCHED TIME EXPRESSIONS IS:'
print list_compare_relaxed(file1 , file2)
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

