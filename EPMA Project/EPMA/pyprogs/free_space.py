import os

try:
    os.chdir("./PNG/")
    li = os.listdir()
    for _ in li:
        if("placeholder.txt" in _):
            continue
        os.remove(f"./{_}")
    os.chdir("./../SVG/")
    li = os.listdir()
    for _ in li:
        if("placeholder.txt" in _):
            continue
        os.remove(f"./{_}")
    os.chdir("./../unplaced/")
    li = os.listdir()
    for _ in li:
        if("placeholder.txt" in _):
            continue
        os.remove(f"./{_}")
    print("Success")
except Exception as e:
    print("Failure")
    print(e)