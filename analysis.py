#!/usr/bin/python3

from subprocess import Popen, PIPE
import os
import sys
import operator
import glob
from argparse import ArgumentParser
from pprint import pprint

"""
Java File Breakdown
--------------------------------
Line:
	- Method declaration
	- 
Comment:
	- Line that starts with //
	- Line inbetween /* and */
Javadoc:
	- Line inbetween /** and */
Whitespace:
	- Nothing in the line (except whitespace or tab characters)

Program Breakdown
--------------------------------
Goals:
	- Scan a Java source file and output its characteristics
		- Line, comment, Javadoc, and whitespace line count, etc.
		- Maybe even more specific than that (declaration lines, import counts, etc.)

Basic Process:
	1) Obtain a file/folder from the arguments.
	2) Make sure the mime-type is "text/x-c" and it's extension is .java
	3) Try to compile it using javac (or the compiler given)
	4) Loop through each line of the file and determine the type of line
	5) Print out the data gathered


Parameters:
	- (Semi-optional) File(s) for scanning
		- A file with a mime-type of "text/x-c" and an extension of .java OR a folder
			- The folder will be searched for files with the criteria above
		- If this parameter is not specified, it will default to a folder called "src/", if it exists
	- (Optoinal) A debug option to print the status of everything the program is doing
	- (Optoinal) A flag to print out the file results individually if the target is a directory

Sample Output:
analyzer.py v1.0 (c) Matthew Dean

Filename.java

Code: 120 lines
Documentation: 23 lines
Whitespace: 14 lines
--------------------
Total: 157 lines

Output Notes:
	- Code/doc/whitespace order is determined by line count
"""

def error(error_str):
	parser.print_help()
	sys.stderr.write("\nError: " + error_str + "\n")
	sys.exit(1)
	
def debug(debug_str):
	if is_debug:
		print(debug_str)

def warning(msg, file_name, line_number):
	sys.stderr.write("Warning: {}:{}: {}\n".format(file_name, line_number, msg))

def check_file_meta(file):
	debug("Checking " + file)
	process = Popen(["file", "--mime-type", file], stdout=PIPE)
	mime_type = process.communicate()[0].decode('UTF-8').split()[1]
	extension = os.path.splitext(file)[-1]

	if not extension == ".java":
		return "File \"" + file + "\" does not have the Java source code extension (.java). File's extension was \"" + extension + "\""
	if not (mime_type == "text/x-c" or mime_type == "text/x-java-source" or mime_type == "text/plain"):
		return "File \"" + file + "\"'s mime-type was not text/x-c, text/plain or text/x-java-source (was \"" + mime_type + "\")"
	
	return None

def flip_dict(dict):
	return {y:x for x,y in dict.items()}

"""
Rules for determining a line's purpose
Whitespace: If line.isspace() returns True
Comment: Line STARTS WITH (disregarding whitespace) a //, or if any of the lines before this have an unclosed /*
         Also count lines with only the /* or */
Documentation: Anything inbetween /** and */
"""
def analyze(file):
	# Read the file line by line into a list, removing the trailing new line character
	with open(file) as f:
		#content_old = f.readlines()	
		content = [line.rstrip() for line in f]
	
	block_comment = False
	doc_block = False
	comments = whitespace = code = doc = total = 0

	for line in content:
		line = line.strip()
		total += 1
		if is_debug:
			sys.stdout.write(str(total) + "  " + line)
		if line == "":
			debug("WHITESPACE")
			whitespace += 1
			continue
		elif "*/" in line:
			if block_comment:
				block_comment = False
				comments += 1
				debug("COMMENT CLOSE")
			elif doc_block:
				doc_block = False
				doc += 1
				debug("DOC CLOSE")
			else:
				warning("Extra */", file, total)
			continue
		elif line.startswith("//") or block_comment:
			comments += 1
			debug("COMMENT (block_comment={}".format(block_comment))
			continue
		elif ("/*" in line and not "/**" in line) or block_comment:
			if not "*/" in line:
				block_comment = True
			comments += 1
			debug("COMMENT OPEN")
			continue
		elif "/**" in line or doc_block:
			if not "*/" in line:
				doc_block = True
			doc += 1 
			debug("DOC (doc_block={})".format(doc_block))
			continue
		else:
			code += 1
			debug("CODE")
			continue
	
	if total != comments + whitespace + code + doc:
		warning("Some lines were not counted", file, total)

	return {
		comments: "comments",
		doc: "documentation lines",
		whitespace: "whitespace lines",
		code: "lines of code"
	}

def output(results):
	if target_is_file:
		print("\n{}\n".format(target))
	else:
		print("\n{} ({} files)\n".format(target, file_count))
		if args.verbose:
			for f in file_list:
				# Remove the target dir from the file name
				print(f[len(target):])
			print() # New line

	total = 0
	for line_count in results.keys():
		total += line_count
	
	results_list = sorted(results.keys(), reverse=True)
	largest_width = len(str(results_list[0]))

	for line_count in results_list:
		# This part adds spaces to make the line count column justified to the right
		additional_spaces = largest_width - len(str(line_count))
		justified_line_count = ""
		for i in range(additional_spaces):
			justified_line_count += " "
		justified_line_count += str(line_count)

		print("{} {} ({}%)".format(justified_line_count, results[line_count], round(line_count / total * 100, 2)))
	
	total_str = "{} total lines".format(total)
	for i in range(len(total_str)):
		sys.stdout.write("-")
	print("\n" + total_str)

parser = ArgumentParser()
parser.add_argument("target", type=str, help="the file or directory to use")
parser.add_argument("-i", "--individual", action="store_true", help="output the result for every file instead of one grand total. only applies if target is a directory")
parser.add_argument("-d", "--debug", action="store_true", help="shows debug information about file parsing")
parser.add_argument("-v", "--verbose", action="store_true", help="shows the files that were analyzed")
args = parser.parse_args()

target = args.target
target_is_file = os.path.isfile(target)
is_debug = args.debug
file_count = 0
file_list = []
print("analyzer.py v1.0 (c) Matthew Dean\n")

if not os.path.exists(target):
	error("File does not exist: \"" + target + "\"")

results = {}
if target_is_file:
	error_msg = check_file_meta(target)
	if error_msg != None:
		# There was some error
		error(error_msg)
	# We have now verified that the file has a correct mime type and has a .java extension
	results = analyze(target)
else:
	# Add the trailing slash if it doesn't exist
	if not target.endswith("/"):
		target += "/"
	for dirpath, dirnames, filenames in os.walk(target):
		for f in filenames:
			relative_path = os.path.join(dirpath, f)
			error = check_file_meta(relative_path)
			if is_debug and error != None:
				debug(error)
			if error == None:
				# There is no error
				file_results = flip_dict(analyze(relative_path))

				# Add the file_results to the dir_results. Stolen from StackOverflow
				results = dict((n, results.get(n, 0) + file_results.get(n, 0)) for n in set(results)|set(file_results))
				file_count += 1
				file_list.append(relative_path)
	results = flip_dict(results)

output(results)
