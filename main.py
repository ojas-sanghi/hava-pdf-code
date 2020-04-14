from PyPDF2 import PdfFileMerger, PdfFileReader
import os

from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path

from multiprocessing import Pool

import time

def combine_pdf(file_int):
    merger = PdfFileMerger()
    # relative path to the folder
    path = "./files/" + file_int + "/"

    # get a list of the files in the folder
    files = [path + f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for f in files:
        # make sure it's a pdf
        # don't re-combine an already combined file (if we're over-writing a combined file for whatever reason)
        if f.endswith(".pdf") and not f.endswith(file_int + ".pdf"):
            # combine the files
            merger.append(f)

    # Write to an output PDF document
    file_name = "LastName_FirstName_DOB-YYYY-MM-DD_File-" + file_int + ".pdf"
    file_path = "./combined/" + file_name
    output = open(file_path, "wb")
    merger.write(output)
    output.close()
    return file_path

def convert_pdf_image(file_path, file_int):
    paths = convert_from_path(file_path, 500, thread_count=4, output_folder = "./files/" + file_int + "/", fmt="jpeg", paths_only=True)
    return paths

def do_ocr(file_int, paths):
    outfile = "./text/out_text" + file_int + ".txt"
    f = open(outfile, "a")

    for path in paths:
        text = str(((pytesseract.image_to_string(Image.open(path)))))
        text = text.replace('-\n', '')
        f.write(text)
    f.close()

def validate_name(name):
    if name == "":
        return False

    if not name.isupper():
        return False

    if not "," in name:
        return False

    return True

def final_name_check(first_name, last_name):
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

def find_info(file_int):
    outfile = "./text/out_text" + file_int + ".txt"
    lines = []

    with open(outfile) as f:
        lines = [line.rstrip() for line in f]

    dob_index = None

    dob_indexes = [n for (n, e) in enumerate(lines) if e.startswith("DOB:")]

    for dob_index in dob_indexes:
        dob = lines[dob_index]
        name = lines[dob_index-1]
        # if this name isn't valid then try going to the line above it
        if not validate_name(name):
            name = lines[dob_index-2]
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
    try:
        first_name = name_split[1]
    except Exception as e:
        print("~~~---NAMING ISSUE HELP---~~~")
        print(e)
        print("~~~---ISSUE WITH: " + file_int + "---~~~")
        last_name = "ERROR"
        first_name = "ERROR"
        return [dob, last_name, first_name]

    last_name, first_name = final_name_check(first_name, last_name)

    return [dob, last_name, first_name]

def rename_file(file_int, data_list):
    current_file_name = "./combined/LastName_FirstName_DOB-YYYY-MM-DD_File-" + file_int + ".pdf"

    dob = data_list[0]
    year = str(19) + dob[10:]
    month = dob[4:6]
    date = dob[7:9]

    last_name = data_list[1]
    first_name = data_list[2]

    new_file_name = f"./combined/{last_name}_{first_name}_DOB-{year}-{month}-{date}_File-{file_int}.pdf"

    os.rename(current_file_name, new_file_name)

def do_thing(file_int):
    file_int = str(file_int)

    temp_file_path = combine_pdf(file_int)
    print("finished combining: " + file_int)

    paths = convert_pdf_image(temp_file_path, file_int)
    print("finished converting and saving imgs: " + file_int)

    do_ocr(file_int, paths)
    print("ocr done, finding data: " + file_int)

    data_list = find_info(file_int)
    print("found data, renaming file: " + file_int)

    rename_file(file_int, data_list)

    print("ALL DONE FOR: " + file_int)


if __name__ == "__main__":
    pool = Pool(10)

    # inclusive on start, EXCLUSIVE on the end
    start = 5450
    end = 5550

    start_time = time.time()

    try:
        pool.map(do_thing,(x for x in range(start, end)))
        # pool.map(do_thing,(x for x in nums))
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
        sys.exit()
    except Exception as e:
        print(e)

    print("--- %s seconds ---" % (time.time() - start_time))

##
# we should also detect the "DOB/AGE/" part too
# thatll be nice, so we have 2 methods of finding it
