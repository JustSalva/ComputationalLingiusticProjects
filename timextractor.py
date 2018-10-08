# standard libs go here
import argparse as ap
import sys

# third-party libs go here

# project libs go here


def main(args):
    assert isinstance(args, ap.Namespace)

    # CHANGE ME
    lines = args.input_file.read().splitlines()
    args.output_file.write("\n".join(lines))


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument('input_file', type=ap.FileType('r'))
    parser.add_argument('-o', '--output-file', type=ap.FileType('w'), default=sys.stdout)

    args = parser.parse_args()
    main(args)
