#!/bin/python3

import sys
import tempfile
import subprocess
import bs4

EDITOR = "nvim"

def main():
    # Check if $1 is present
    if len(sys.argv) < 2:
        print("No file specified")
        sys.exit(1)

    emailFile = sys.argv[1];
    headers: list[str] = []
    originalBody: list[str] = []

    with open(emailFile) as f:
            lines = f.readlines()
            inBody = False
            for line in lines:
                if len(line.strip()) == 0:
                    inBody = True
                    continue
                if inBody:
                    originalBody.append(line)
                else:
                    headers.append(line)


    # Create a temporary markdown file
    # That has the headers as a comment in a yaml block:
    tmpFile = tempfile.gettempdir() + "/thunderbird-ed-intermediary.md"
    with open(tmpFile, "w") as f:
        f.write("---\n")
        for header in headers:
            f.write("#" + header)
        f.write("---\n")
        f.write("\n")
        f.write("\n")

    
    # Open file with EDITOR
    subprocess.call([EDITOR, tmpFile])

    # Convert markdown to html
    html = subprocess.check_output(["pandoc", tmpFile]).decode("utf-8")

    # Replace first <p><br></p> with html using bs4
    originalBodyText = "".join(originalBody)
    soup = bs4.BeautifulSoup(originalBodyText, "html.parser")
    body = soup.body
    if body is None:
        print("Error parsing html, no body")
        sys.exit(1)
    firstP = body.find("p")
    if firstP is None:
        print("Error parsing html, no first <p>")
        sys.exit(1)
    firstP.replace_with(bs4.BeautifulSoup(html, "html.parser"))

    # Replace the whole .eml file with a new one, retaining the headers
    # but replacing the body with the new html body.
    with open(emailFile, "w") as f:
        for header in headers:
            f.write(header)
        f.write("\n")
        f.write(str(soup))
    
if __name__ == "__main__":
    main()

# vim: set foldmethod=marker:
