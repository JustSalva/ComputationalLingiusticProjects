# -*- coding: utf-8 -*-

# standard
import argparse as ap
import sys

# third
import yaml
from nltk.tree import Tree


__author__ = "Anaïs Tack"
__email__ = "anais.tack@uclouvain.be"


EMPTY_PARSE = '()'


def count_correct(gold_spans, parser_spans):
    return sum(len(set(g_sent).intersection(set(p_sent)))
               for g_sent, p_sent in zip(gold_spans, parser_spans))


def count_all(spans):
    return sum(len(sent) for sent in spans)


def precision(gold_spans, parser_spans):
    c = count_correct(gold_spans, parser_spans)
    p = count_all(parser_spans)
    return c / p if p != 0 else 0


def recall(gold_spans, parser_spans):
    c = count_correct(gold_spans, parser_spans)
    g = count_all(gold_spans)
    return c / g if g != 0 else 0


def f1_score(precision, recall):
    if precision == 0 and recall == 0:
        return 0
    else:
        return 2 * precision * recall / (precision + recall)


class SpanTree(object):

    def __init__(self, string=None):
        self.tree = Tree.fromstring(string) if string else None

    def compute_spans(self, labeled=False):
        spans = []
        if self.tree:
            leaves = self.tree.leaves()
            leftmost_i = 0  
            for subtree in self.tree.subtrees():
                subleaves = subtree.leaves()
                label = subtree.label()
                span = self.find_span(leaves, subleaves, start=leftmost_i)
                pair = span + (label,) if labeled else span
                spans.append(pair)
                # set current left index to account for subtree duplicates
                leftmost_i = span[0]
                if leftmost_i == span[1]:  # go past singletons
                    leftmost_i += 1
        assert len(spans) == len(set(spans)), "Error in computing spans!"
        return sorted(spans)

    @staticmethod
    def find_span(leaves, subleaves, start=0):
        n_subleaves = len(subleaves)
        for i, leaf in filter(lambda i: i[0] >= start, enumerate(leaves)):
            if leaf == subleaves[0] and subleaves == leaves[i:i+n_subleaves]:
                span = (i, i + n_subleaves - 1)
                return span


class ConstituencyEvaluator(object):
    """
    Adaptation of nltk.parse.evaluate.DependencyEvaluator
    """

    def __init__(self, parsed_sents, gold_sents):
        self._parsed_sents = parsed_sents
        self._gold_sents = gold_sents

    def eval(self):

        if len(self._parsed_sents) != len(self._gold_sents):
            raise ValueError("The total number of sentences must be equal "
                             "for both system and gold! system: %d, gold: %d"
                             % (len(self._parsed_sents), len(self._gold_sents)))

        results = {}
        for version, labeled in (('labeled', True), ('unlabeled', False)):
            parser_spans, gold_spans = self._return_spans(labeled=labeled)

            p = precision(gold_spans, parser_spans)
            r = recall(gold_spans, parser_spans)
            f1 = f1_score(p, r)
            results[version] = {
                'precision': p,
                'recall': r,
                'f1_score': f1}

        return results

    def _return_spans(self, labeled=False):
        parsed, gold = tuple([tree.compute_spans(labeled=labeled)
                              for tree in tree_list]
                             for tree_list in (self._parsed_sents,
                                               self._gold_sents))
        return parsed, gold


def read_parse_trees(input_file):
    with open(input_file, 'r') as input_fh:
        for line in filter(None, map(lambda s: s.strip(), input_fh)):
            if line == EMPTY_PARSE:
                yield SpanTree()
            else:
                yield SpanTree(line)


def main(args):
    assert isinstance(args, ap.Namespace)
    
    output_trees = []
    gold_trees = []
    for output_file, gold_file in zip(sorted(args.system_files),
                                      sorted(args.gold_files)):
        new_output_trees = read_parse_trees(output_file)
        new_gold_trees = read_parse_trees(gold_file)
        output_trees.extend(new_output_trees)
        gold_trees.extend(new_gold_trees)

    evaluator = ConstituencyEvaluator(parsed_sents=output_trees,
                                      gold_sents=gold_trees)

    yaml.safe_dump(evaluator.eval(), sys.stdout, default_flow_style=False)


def create_parser():
    parser = ap.ArgumentParser(description="Computes (un)labelled PARSEVAL "
                                           "metrics (micro-averaged "
                                           "precision, recall and "
                                           "F1-score).")
    parser.add_argument("-s", "--system-files", nargs='+',
                        metavar='system_file', required=True)
    parser.add_argument("-g", "--gold-files", nargs='+', metavar='gold_file',
                        required=True)
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args)
