#!/usr/bin/env python3

def main():
    #testing segmenting files
    segs = []

    with open("Test Files/test_img.jpg", "rb") as f:
        while True:
            s = f.read(1024)
            if not len(s):
                break
            segs.append(s)
    print(len(segs))


if __name__ == '__main__':
    main()
