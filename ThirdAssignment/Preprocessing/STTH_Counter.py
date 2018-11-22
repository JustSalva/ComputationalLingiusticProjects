from nltk.tokenize import word_tokenize

def file_counters(file):
    sentence_counter=0
    token_counter = 0
    word_dict = dict()
    hapax_counter = 0
    with open(file,'r') as dataset:
        for sentence in dataset:
            sentence_counter += 1
            sentence_tokens = word_tokenize(sentence)
            for token in sentence_tokens:
                token_counter += 1
                if token in word_dict:
                    word_dict[token] += 1
                else:
                    word_dict[token] = 1
        for key in word_dict:
            if word_dict[key]==1:
                hapax_counter += 1

    return sentence_counter, word_dict, token_counter, hapax_counter



s_counter, w_dict, t_counter, h_counter = file_counters('/home/fabio/Documenti/ComputationalLingiusticProjects/ThirdAssignment/data/train/train.input.txt')
print('NUMBER OF SENTENCES IN TRAIN IS:',s_counter)
print('NUMBER OF TYPES IN TRAIN IS:', len(w_dict.keys()))
print('NUMBER OF TOKENS IN TRAIN IS:',t_counter)
print('NUMBER OF HAPAX LEGOMENA IN TRAIN IS:',h_counter,'\n\n')

s_counter, w_dict, t_counter, h_counter = file_counters('/home/fabio/Documenti/ComputationalLingiusticProjects/ThirdAssignment/data/test/test.input.txt')
print('NUMBER OF SENTENCES IN TEST IS:',s_counter)
print('NUMBER OF TYPES IN TEST IS:', len(w_dict.keys()))
print('NUMBER OF TOKENS IN TEST IS:',t_counter)
print('NUMBER OF HAPAX LEGOMENA IN TEST IS:',h_counter)


