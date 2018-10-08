# standard libs go here
import argparse as ap
import sys

# third-party libs go here

# project libs go here
from corpusUtilities import tokenize
import XMLparsing.XMLparser as p


def main(args):
    assert isinstance(args, ap.Namespace)

    # CHANGE ME
    tokenized_text = []
    tokenize(args.input_file, tokenized_text)
    tokenized_text

    test_tree = p.createTimeML()
    p.addItem(test_tree, 10, 13, 'dddd', 'ciao')
    # END OF MAIN
    if args.output_file is None:
        print p.writer(test_tree)
    else:
        p.saveFile(args.output_file, test_tree)


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument('input_file', type=str)
    parser.add_argument('-o', '--output-file', type=str, default=None)

    args = parser.parse_args()
    main(args)
