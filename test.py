# i use this file to test the data extraction from some output text file

import sys
outfile = "./text/out_text5529.txt"
lines = []

with open(outfile) as f:
    lines = [line.rstrip() for line in f]

dob_index = None

dob_indexes = [n for (n, e) in enumerate(lines) if e.startswith("DOB:")]

def validate_name(name):
    if name == "":
        return False

    if not name.isupper():
        return False

    if not "," in name:
        return False

    return True

def last_name_check(first_name, last_name):
    if not last_name.isupper():
        last_name = "ERROR"
    else:
        last_name = last_name.title()

    if not first_name.isupper():
        first_name = "ERROR"
    else:
        first_name = first_name.title()

    bad_char_index = last_name.find("|")
    if not bad_char_index == -1:
        last_name = last_name[:bad_char_index] + last_name[bad_char_index+1:]

    bad_char_index = first_name.find("|")
    if not bad_char_index == -1:
        first_name = first_name[:bad_char_index] + first_name[bad_char_index+1:]

    return [last_name, first_name]


for dob_index in dob_indexes:
    dob = lines[dob_index]
    name = lines[dob_index-1]
    print(name)
    # if this name isn't valid then try going to the line above it
    if not validate_name(name):
        name = lines[dob_index-2]
        print(name)
        # if this is wrong too then try the next DOB index
        if not validate_name(name):
            continue
        else:
            break
    else:
        break

name = name.replace(" ", "")
dob = dob.replace(" ", "")
name_split = name.split(",")

last_name = name_split[0]
first_name = name_split[1]

last_name, first_name = last_name_check(first_name, last_name)

print(dob)
year = str(19) + dob[10:]
date = dob[7:9]
month = dob[4:6]
print(year)
print(month)
print(date)