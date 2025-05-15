import sys
import os
import argparse

def extract_name(filename):  								# Extract each name in the list
	names = []
	with open(filename, 'r') as file:
		for line in file:
			names.append(line.strip().lower())
	return names

def parse_name(fullname, specialChar: bool, min: int):								# Split up first, middle and last name
	parts = fullname.split(' ')
	first = parts[0]
	last = parts[-1]

	patterns = [																	#Define simple patterns
		    first + last,
		    first[0] + last,
		    first + last[0],
		    last + first,
		    last + first[0],
		    last[0] + first,
		    first + first,
		    last + last,
		    first + last + "123",
		    first + last + "1234",
		    first + last + "1234567",
		    first + last + "987",
		    first + last + "789",
		    first + last + "12345678",
		    first[0].upper() + last.title(),
		    first.title() + last[0:len(last)-1] + last[-1].upper(),
		    (first + last).upper(),
		    (first + last).title(),
		]

	middle_patterns = []
	if len(parts) > 2:																# If middle name exist
		middle = parts[1:-1]
		middle_patterns = [
	   		first[0] + middle[-1][0] + last,
		    first[0].upper() + middle[-1][0].upper() + last.title()
		]
	if middle_patterns:
		for item in middle_patterns:
			patterns.append(item)

	if specialChar is True:																	# If special chars required
		special_patterns = []
		for char in ['@','&','.']:															# Add characters in the middle
			special_patterns.append((first + char + last))
			special_patterns.append((last + char + first))

		org_len = len(patterns)
		for char in ['!','$','@','*']:													# Add characters to the end of keywords	
			for item in patterns[0:org_len]:
				patterns.append(item + char)
				patterns.append(char + item)
				patterns.append(char + item + char)

		for item in special_patterns:
			patterns.append(item)

	for item in patterns:
		if min:
			print(minimum(item, min))
		else:
			print(item)

def minimum(key: str, count: int):													# Optional argument for when minimum chars are required
	for i in range(1,count+1):
		if len(key) < count:
			key = key + str(i)
	return key

def main():
	parser = argparse.ArgumentParser(description="A simple wordlist generator")
	parser.add_argument("-f", "--file", required=True, help="Path to the list of name")
	parser.add_argument("-s", "--add-special", action="store_true", help="Add special characters to the wordlist")
	parser.add_argument("-m", "--min-length", type=int, default=0, help="Specify a minimum of characters required")

	args = parser.parse_args()
	if not os.path.isfile(args.file):												#Check for valid file
		print(f"File not found: {args.file}")
		sys.exit(1)

    	#Debug
	print("List selected: ", args.file)
	print("Add special characters: ", args.add_special)
	print("Minimum length: ", args.min_length)

	names = extract_name(args.file)
	for name in names:
		parse_name(name, args.add_special, args.min_length)

if __name__ == '__main__':
	main()
