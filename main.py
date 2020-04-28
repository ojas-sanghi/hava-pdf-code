from PyPDF2 import PdfFileMerger, PdfFileReader
import os

from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path

from multiprocessing import Pool

import time
import traceback

import text

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

def rename_file(file_int, data_list):
    current_file_name = "./combined/LastName_FirstName_DOB-YYYY-MM-DD_File-" + file_int + ".pdf"

    name = data_list[0]
    if name:
        name_list = name.split(" ")
        last_name = name_list[0].title()
        first_name = name_list[1].title()
    else:
        last_name = "ERROR"
        first_name = "ERROR"

    dob = data_list[1]
    if dob:
        dob_list = dob.split("/")

        year = dob_list[2]
        year = "19" + year

        month = dob_list[0]
        if len(month) == 1:
            month = "0" + month

        date = dob_list[1]
        if len(date) == 1:
            date = "0" + date
    else:
        year = "YYYY"
        month = "MM"
        date = "DD"

    new_file_name = f"./combined/{last_name}_{first_name}_DOB-{year}-{month}-{date}_File-{file_int}.pdf"

    try:
        os.rename(current_file_name, new_file_name)
    except FileExistsError:
        print("\nERR: Could not rename file for: " + str(file_int))
        print("File already seems to exist..: " + new_file_name)
        print("Deleting new file made..\n")

        os.remove(current_file_name)

def do_thing(file_int):
    file_int = str(file_int)

    temp_file_path = combine_pdf(file_int)
    print("done combining, saving imgs: " + file_int)

    paths = convert_pdf_image(temp_file_path, file_int)
    print("done saving imgs, doing ocr: " + file_int)

    do_ocr(file_int, paths)
    print("done ocr, finding data: " + file_int)

    data_list = text.find_info(file_int)
    print("found data, renaming file: " + file_int)

    rename_file(file_int, data_list)

    print("ALL DONE FOR: " + file_int)
    return file_int

def main():
    path = "./files/"
    files = [f for f in os.listdir(path)]

    pool = Pool(6)
    start_time = time.time()

    done = []

    try:
        done = pool.map(do_thing,(x for x in files))
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
        sys.exit()
    except Exception:
        print(traceback.format_exc())

    for f in done:
        if not f:
            continue
        if f in files:
            files.remove(f)

    print("~ ~ not done for some reason: ")
    print(files, end = "~ ~ \n\n")

    print("--- %s seconds ---" % (time.time() - start_time))
    sys.exit(0)


if __name__ == "__main__":
    main()

##
# we should also detect the "DOB/AGE/" part too
# thatll be nice, so we have 2 methods of finding it
