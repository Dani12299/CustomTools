import os
import sys
import argparse
from itertools import product

def generate_teencode(namelist: list, limit: int):
	teen_dict = {
		'a': ['4', '@'],
		'b': ['8'],
		'e': ['3'],
		'g': ['9'],
		'h': ['#'],
		'i': ['1', '!'],
		'l': ['1'],
		'o': ['0'],
		's': ['5', '$'],
		't': ['7', '+'],
	}

	for word in namelist:
		char_options = []
		for c in word:
			if c in teen_dict:
				char_options.append([c] + teen_dict[c])
			else:
				char_options.append([c])

		variants = [''.join(p) for p in product(*char_options)]
		for item in variants[:limit]:
			print(item)

def main():
	parser = argparse.ArgumentParser(description='Add "Teen Code" to the wordlist')
	parser.add_argument("-l", "--limit", type=int, default=10, help="Limit the number of variants allowed on a single word")
	parser.add_argument("-f", "--file", required=True, help="path to wordlist file")
	args = parser.parse_args()

	if not os.path.isfile(args.file):
		print(f"File not found: {args.file}")
		sys.exit(1)

	names = []
	with open(args.file, 'r') as file:
		for line in file:
			names.append(line.strip().lower())

	sorted_names = sorted(set(names))

	generate_teencode(sorted_names, args.limit)

if __name__ == '__main__':
	main()