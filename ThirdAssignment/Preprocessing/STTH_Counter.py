from nltk.tokenize import word_tokenize

def file_counters(file):
    '''Reading a file, I tokenize every line (increasing the sentence counter) and
    I set up a dictionary with key as word and the iterations as value. The hapax legomena
    are the keys whose value is 1.'''
    hapax_list=[]
    sentence_counter=0
    token_counter = 0
    word_dict = dict()
    hapax_counter = 0
    with open(file,'r') as dataset:
        for question in dataset:
            #all_sentences = sent_tokenize(question)
            sentence_counter += 1 #len(all_sentences)
            sentence_tokens = question.split()
            #ALTERNATIVELY:
            #sentence_tokens=[]
            #for sentence in all_sentences:
            #    all_tokens = word_tokenize(sentence)
            #    for token in all_tokens:
            #        sentence_tokens.append(token)
            #print(sentence_tokens, sentence_counter)
            for token in sentence_tokens:
                token_counter += 1
                if token in word_dict:
                    word_dict[token] += 1
                else:
                    word_dict[token] = 1
        for key in word_dict:
            if word_dict[key]==1:
                hapax_counter += 1
                hapax_list.append(key)
                #print(key)

    return sentence_counter, word_dict, token_counter, hapax_counter, hapax_list

def unknown_tokens_counter(file):
    '''The idea is that I tokenize the parsed text, and I look for the
    <unknown> token using two sentinels: 'open' look at the '<' token, and
    unk look at the 'unknown' token. If sentinels are True and I find
    '>' token, I increase the counter.'''
    unk_token_counter = 0
    sentinel_open = False
    sentinel_unk = False
    with open(file,'r') as dataset:
        for tree in dataset:
            tree_tokens = word_tokenize(tree)
            #print(tree_tokens)
            for token in tree_tokens:
                if token=='<':
                    sentinel_open = True
                elif token=='unknown' and sentinel_open==True:
                    sentinel_unk = True
                elif token=='>' and sentinel_open==True and sentinel_unk==True:
                    unk_token_counter += 1
                    sentinel_unk = False
                    sentinel_open = False
                else:
                    sentinel_unk = False
                    sentinel_open = False

    return unk_token_counter



s_counter, w_dict, t_counter, h_counter, h_list = file_counters('./../data/train/train.input.txt')
print('NUMBER OF SENTENCES IN TRAIN IS:',s_counter)
print('NUMBER OF TYPES IN TRAIN IS:', len(w_dict.keys()))
print('NUMBER OF TOKENS IN TRAIN IS:',t_counter)
print('NUMBER OF HAPAX LEGOMENA IN TRAIN IS:',h_counter,'\n\n')
print(h_list, len(h_list))

s_counter, w_dict, t_counter, h_counter, h_list = file_counters('./../data/test/test.input.txt')
print('NUMBER OF SENTENCES IN TEST IS:',s_counter)
print('NUMBER OF TYPES IN TEST IS:', len(w_dict.keys()))
print('NUMBER OF TOKENS IN TEST IS:',t_counter)
print('NUMBER OF HAPAX LEGOMENA IN TEST IS:',h_counter,'\n\n')

number_of_unknown_tokens = unknown_tokens_counter('./../data/train/train.unknown.txt')
print('NUMBER OF UNKNOWN TOKENS IS:',number_of_unknown_tokens)




