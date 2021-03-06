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

    return str(round(precision_relaxed*100,2))+ " & "+ str(round(recall_relaxed*100,2))+ " & "+ str(round(F1_relaxed*100,2))+ " & "+ str(round(F1_strict*100,2))

original_file = 'data/test/annotated/test_08.gold.tml'
my_file =  'result/test/test_08.output.tml'
print all_performances( original_file, my_file)