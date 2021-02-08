#!usr/bin/python3
import sys
import re
import os

###########################################################################################################################################
# TODO: WRITE IN VARIABLES HERE
# I know these should be arguments but I usually run this script a bazillion times and don't want to think about variables more than once.

input_file = "" # file containing HIVE-XXXXX jiras we're searching for. Format doesn't matter, we'll just be searching this for "HIVE-XXXXX" strings
local_repo_path = "path/to/local/hive/repo" # path to local hive repo that we're searching for backports
branch = "" # e.g. HDP-3.1-maint. Pull before running this script so you don't forget to AGAIN, KAREN!
outfile_directory = "" # directory where you want your output to go. output file will be at outfile_directory/branch_name-commits.txt and is tab-separated.

###########################################################################################################################################

# glean set of HIVE jiras from input file.
file = open(input_file, 'r')
apache_jira_numbers = set()
for line in file:
  jira_numbers_in_line = re.findall('HIVE-(\d{5})', line)
  for number in jira_numbers_in_line:
    apache_jira_numbers.add(number)

# Check git log of local branch and collect all mentions of these HIVE jiras
outfileName = outfile_directory + branch + "-commits.txt"
print("Branch:", branch)
print("Output file:", outfileName)
print("IS YOUR BRANCH UP-TO-DATE?\n")
# grep branch for each commit
os.chdir(local_repo_path)
os.system('git checkout ' + branch)

outfile = open(outfileName, 'w')
outfile.write("Branch: " + branch + "\t\tLEFT TO CHECK (Worry, but no verdict/note):\t=SUM(C3:C) - COUNTA(D3:D)\n")
outfile.write("Apache Jira\tNumber of commits in branch mentioning Jira\tWorry?\tVerdict/Notes\tCommits in branch mentioning Jira; or Apache Hive Jira if none...\n")

apache_jira_numbers_list = list(apache_jira_numbers)
for number in apache_jira_numbers_list:
  output = os.popen("git log --grep HIVE-" + number + " | grep HIVE-").read()

  outfile.write("HIVE-" + number + "\t")  # column 0: HIVE-xxxxx

  outputList = output.split("\n")
  numCommits = len(outputList) - 1
  outfile.write(str(numCommits) + "\t")   # column 1: number of commits containing HIVE-XXXXX
  if numCommits != 1:
    outfile.write("1")
  outfile.write("\t")                     # column 2: should we be worried? i.e. the number of commits != 1 (either not there or might have been reverted....)
  outfile.write("\t")                     # column 3: left empty for notes and verdict
  if numCommits == 0:
    outfile.write("https://issues.apache.org/jira/browse/HIVE-" + number)
  else:
    for e in outputList:
      outfile.write(e + "\t")               # columns 4+: commits in branch mentioning jira OR if there are none, a URL to Apache Hive Jira
  outfile.write("\n")

outfile.close()
file.close()
