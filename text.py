# temp
import sys

import traceback

def find_nth_occurrence(ini_str, sub_str, n):
    # Finding nth occurrence of substring
    val = -1
    for i in range(0, n):
        val = ini_str.find(sub_str, val + 1)
    return val

def dob1_algo2_name_check(name):
    if name == "":
        return False

    if not name.isupper():
        return False

    if not ", " in name:
        return False

    if name.startswith("PHS"):
        return False

    if name.count(",") != 1:
        return False

    return True

def dob1_algo2(lines, index):
    dob = lines[index]
    space_index = 4

    name = False

    # extract the dob
    dob = dob[space_index + 1 : dob.find(",")]
    # get rid of the 19 (like from 1933)
    correct_dob = dob[:len(dob)-4]
    correct_dob += dob[len(dob)-2:]

    for i in range(1, 11):
        new_name = lines[index - i]
        if not dob1_algo2_name_check(new_name):
            continue
        else:
            name = new_name
            break
    if name:
        # get rid of a middle name, if any
        if name.count(" ") > 1:
            first_space = name.find(" ")
            second_space = name.find(" ", first_space + 1)
            name = name[:second_space]
            name = name.replace(",", "")

    return [name, correct_dob]

def dob1_algo1_name_check(name):
    if name == "":
        return False

    if not name.isupper():
        return False

    if not "," in name:
        return False

    return True

def dob1_algo1(lines, index):
    dob = lines[index]
    name = lines[index - 1]

    # get rid of a middle name, if any
    if name.count(" ") > 1:
        first_space = name.find(" ")
        second_space = name.find(" ", first_space + 1)
        name = name[:second_space]

    if not dob1_algo1_name_check(name):
        name = lines[index - 2]
    if not dob1_algo1_name_check(name):
        name = False

    if name:
        name = name.replace(",", "")

    correct_dob = dob[4:]
    return [name, correct_dob]

# dob1 -> DOB:
def dob1_algo_chooser(lines):
    dob_indexes = [n for (n, e) in enumerate(lines) if e.startswith("DOB:")]

    for dob_index in dob_indexes:
        dob = lines[dob_index]

        algo1_result = None
        algo2_result = None

        # if there's not a space, it's algo1
        if dob[4] != " ":
            algo1_result = dob1_algo1(lines, dob_index)

        if dob[4] == " ":
            if dob[-8] == ",":
                algo2_result = dob1_algo2(lines, dob_index)

        if algo1_result:
            if not False in algo1_result:
                return algo1_result
        if algo2_result:
            if not False in algo2_result:
                return algo2_result
        continue
    return False


def dob2_name_check(name):
    if name == "":
        return False

    if not " , " in name:
        return False

    if not name.startswith("Patient:"):
        return False

    if name.count(",") != 1:
        return False

    return True

# dob2 -> "DOB/"
def dob2_algo(lines, index):
    dob = lines[index]

    name = False
    correct_name = False

    # extract the dob
    dob = dob[13:23]
    # get rid of the 19 (like from 1933)
    correct_dob = dob[:len(dob)-4]
    correct_dob += dob[len(dob)-2:]

    for i in range(1, 11):
        new_name = lines[index - i]
        if not dob2_name_check(new_name):
            continue
        else:
            name = new_name
            break
    if name:
        first_start = find_nth_occurrence(name, " ", 1)
        second_end = find_nth_occurrence(name, " ", 4)

        # extract the name
        correct_name = name[first_start + 1 : second_end]
        correct_name = correct_name.replace(", ", "")

    return [correct_name, correct_dob]

def dob2_algo_chooser(lines):
    dob_indexes = [n for (n, e) in enumerate(lines) if e.startswith("DOB/Age/")]

    for dob_index in dob_indexes:
        result = None

        result = dob2_algo(lines, dob_index)

        if result:
            if not False in result:
                return result
        continue
    return False

def dob3_name_check(name):
    if name == "":
        return False

    if not name.startswith("Patient Name:"):
        return False

    return True

# dob3 -> "Date of Birth:"
def dob3_algo(lines, index):
    dob = lines[index]
    space_index = 12

    name = False
    correct_name = False

    # extract the dob
    dob = dob[15 : dob.find(" ", 15)]
    # get rid of the 19 (like from 1933)
    correct_dob = dob[:len(dob)-4]
    correct_dob += dob[len(dob)-2:]

    for i in range(1, 11):
        new_name = lines[index - i]
        if not dob3_name_check(new_name):
            continue
        else:
            name = new_name
            break
    if name:
        name_start_index = find_nth_occurrence(name, " ", 2) + 1
        name_mid_index = find_nth_occurrence(name, " ", 3)
        name_end_index = find_nth_occurrence(name, " ", 4)

        first_name = name[name_start_index : name_mid_index]
        last_name = name[name_mid_index + 1 : name_end_index]

        correct_name = last_name + " " + first_name

    return [correct_name, correct_dob]

def dob3_algo_chooser(lines):
    dob_indexes = [n for (n, e) in enumerate(lines) if e.startswith("Date of Birth: ")]

    for dob_index in dob_indexes:
        result = None

        result = dob3_algo(lines, dob_index)

        if result:
            if not False in result:
                return result
        continue
    return False

def dob4_name_check(name):
    if name == "":
        return False

    if not name.startswith("Patient Name:"):
        return False

    return True

# dob3 -> "Date of Birth:"
def dob4_algo(lines, index):
    name = lines[index]

    end_space = find_nth_occurrence(name, " ", 2)
    correct_name = name[:end_space]
    correct_name = correct_name.replace(",", "")

    return [correct_name, False]

def dob4_algo_chooser(lines):
    name_indexes = [n for (n, e) in enumerate(lines) if "CardioNet Summary Report" in e]

    for name_index in name_indexes:
        result = None

        result = dob4_algo(lines, name_index)

        if result:
            if result[0]:
                return result
        continue
    return False

def master_algo_chooser(lines):
    dob1_result = dob1_algo_chooser(lines)
    if dob1_result:
        if not False in dob1_result:
            return dob1_result

    dob2_result = dob2_algo_chooser(lines)
    if dob2_result:
        if not False in dob2_result:
            return dob2_result

    dob3_result = dob3_algo_chooser(lines)
    if dob3_result:
        if not False in dob3_result:
            return dob3_result

    dob4_result = dob4_algo_chooser(lines)
    if dob4_result:
        if dob4_result[0]:
            return dob4_result

    # We couldn't find anything :(
    return [False, False]

def find_info(file_int, test = False):
    # Note: test mode depends on the .txt file (from OCR) already existing
    file = "./text/out_text" + file_int + ".txt"
    lines = []

    with open(file) as f:
        lines = [line.rstrip() for line in f]

    result = master_algo_chooser(lines)

    if test:
        print(result)
        sys.exit(0)
    return result

if __name__ == "__main__":
    file_int = "5620"
    print(find_info(file_int, True))