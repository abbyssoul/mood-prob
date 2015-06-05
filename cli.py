# import fileinput
import sys
import argparse

from emotions import intelligence, parser


def print_stats(emotional_entity):
    print "EI: {}".format(emotional_entity.stats)
    for emoji, power in emotional_entity.emotions():
        print "\t'{}': {}".format(emoji, power)
        sys.stdout.flush()

def main():
    arg_parser = argparse.ArgumentParser(description='Batch create HC randomly named rooms')
    arg_parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    arg_parser.add_argument('files', nargs='+', default=["-"],
                        help='A list of files to read data from')

    args = arg_parser.parse_args()

    emo_parser = parser.EmojiParser()

    for file_name in args.files:
        if file_name == '-':
            emotional_entity = intelligence.Intelligence("<Nameless one>", emo_parser)
            for line in sys.stdin:
                emotional_entity.update(line)
                print_stats(emotional_entity)
        else:
            with open(file_name) as f:
                emotional_entity = intelligence.Intelligence(file_name, emo_parser)
                for line in f:
                    emotional_entity.update(line)
                print_stats(emotional_entity)

    # print_stats(emotional_entity)


if __name__ == "__main__":
    main()
