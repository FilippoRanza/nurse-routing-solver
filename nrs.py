#! /usr/bin/python3

from argparse import ArgumentParser
import json

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('instance', help='Request file')
    parser.add_argument('-o', '--output', 
                        help='Specify output file')
    

    return parser.parse_args()


def load_instance(file_name):
    with open(file_name) as data:
        out = json.load(data)
    return out

def main():
    args = parse_args()
    instance = load_instance(args.instance)
    print(instance)

if __name__ == '__main__':
    main()
