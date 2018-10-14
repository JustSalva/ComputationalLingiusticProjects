from XMLmatcher import *

def all_performances(original_gold_path, my_gold_path):
    """It takes as input the file paths of the two gold standard documents. It runs the matching
    functions of XMLmatcher.py and do computation for precision, recall and F1 indices."""
    results = counter_matches(original_gold_path, my_gold_path)
    #Computing evaluators
    precision_strict = float(results[2])/results[1]
    precision_relaxed = float(results[3])/results[1]
    recall_strict = float(results[2])/results[0]
    recall_relaxed = float(results[3])/results[0]
    F1_strict = 2 * (precision_strict*recall_strict) / (precision_strict+recall_strict)
    F1_relaxed = 2 * (precision_relaxed*recall_relaxed) / (precision_relaxed+recall_relaxed)

    return precision_relaxed, recall_relaxed, F1_relaxed, F1_strict

original_file = 'data/train/annotated/train_02.gold.tml'
my_file =  'result/train/train_02.output.tml'

print all_performances( original_file, my_file)