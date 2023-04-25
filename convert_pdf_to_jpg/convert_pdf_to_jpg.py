# This is for my IJRR submission. I need to convert all the PDF files to JPEG files
import os
from pathlib import Path
from glob import iglob
import subprocess

HOME_DIR = os.path.expanduser('~')
PAPER_IMAGES_DIR = HOME_DIR + "/Downloads/BTP/images"
OUTPUT_DIR = HOME_DIR + "/Downloads/BTP/images_jpg"


def convert_all_paper_files():
    print("Running")
    # for subdir, dirs, files in os.walk(PAPER_IMAGES_DIR):
    #     print(dirs)
    #     for file in files:
    #         if not file.endswith(".pdf"):
    #             continue
    #         print(file)
    # file_glob = PAPER_IMAGES_DIR + "/**/*"
    # file_list = [f for f in iglob(file_glob, recursive = True) if f.endswith('.pdf')]
    file_list = [f for f in Path(PAPER_IMAGES_DIR).glob('**/*') if f.is_file() and f.as_posix().endswith(".pdf")]
    # print(file_list)
    for f in file_list:
        print(f)
        output_file = Path(OUTPUT_DIR) / f.relative_to(PAPER_IMAGES_DIR).with_suffix("")
        f_escaped = f.as_posix().replace(" ", "\\ ")
        output_escaped = output_file.as_posix().replace(" ", "\\ ")
        cmd = f"pdftoppm -jpeg -r 300 -cropbox -singlefile {f_escaped} {output_escaped}"
        print(f"Executing {cmd}")
        subprocess.Popen(cmd, shell=True)
        print(output_file)




if __name__ == "__main__":
    convert_all_paper_files()