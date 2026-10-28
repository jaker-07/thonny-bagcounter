# JAKE RR THONNY PYTHON PROJECT CLAUDE VERSION
# install 'antrhopic' in Thonny

import tkinter                           # AI-sourced (Claude): tkinter is used for the file picker below
from tkinter import filedialog
import os                                # AI-sourced (Claude): os and sys are used to open the output file at the end
import sys
import base64                            # AI-sourced (Claude): turns PDFs/images into text so they can be sent
import anthropic                         # AI-sourced (Claude): used to send the file to Claude


# AI-sourced (Claude): sends the file to Claude and asks it to count the pink and green bags
def count_bags(filename):
    bag_file = open(filename, "rb")      # "rb" reads the raw bytes, so it works for any file type
    file_bytes = bag_file.read()
    bag_file.close()
    data = base64.standard_b64encode(file_bytes).decode()

    if filename.lower().endswith(".pdf"):
        file_block = {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": data}}
    elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
        file_block = {"type": "image", "source": {"type": "base64", "media_type": "image/png" if filename.lower().endswith(".png") else "image/jpeg", "data": data}}
    else:                                # anything else is sent as plain text
        file_block = {"type": "text", "text": file_bytes.decode("utf-8", errors="ignore")}

    client = anthropic.Anthropic(api_key=" ")       # anthropic.Anthropic(api_key="sk-ant-...") if Thonny can't find your key
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=16000,
        messages=[{"role": "user", "content": [
            file_block,
            {"type": "text", "text": "Count the pink and green bags in this file. Reply with ONLY two numbers, pink first, like: 12,9"},
        ]}],
    )

    answer = next(block.text for block in response.content if block.type == "text")
    pink, green = answer.split(",")      # "12,9" becomes "12" and "9"
    return int(pink), int(green)         # sends both counts back to where the function was called


print("A file window will open: select your bag colour file and press Open.")
print("On a Mac, if the window doesn't appear, click the bouncing Python icon in the Dock.")
print("The result will be saved as bag_count_output.txt and open automatically.")

# AI-sourced (Claude): file picker, opens a window to browse folders and select the bag colour file
root = tkinter.Tk()
root.withdraw()                          # hides the empty main tkinter window
root.attributes("-topmost", True)        # keeps the file picker in front (works on Windows)
filename = ""
while len(filename) == 0:                # cancelling returns nothing, so the picker reopens until a file is chosen
    filename = filedialog.askopenfilename()
root.destroy()                           # closes tkinter once the file is chosen

pink, green = count_bags(filename)

output_file = open("bag_count_output.txt", "w")   # "w" creates a new file to write in
output_file.write(f"There are {pink} students who have pink bags and {green} students who have green bags.")
output_file.close()                               # closing saves the file

# AI-sourced (Claude): opens the output file automatically in the computer's default text app
if sys.platform == "win32":              # Windows
    os.startfile("bag_count_output.txt")
else:                                    # macOS
    os.system("open bag_count_output.txt")