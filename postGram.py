#!/usr/bin/env python
#-*- coding: utf-8 -*-

# postGram is a Tool For Downloading Instagram Posts With the Post Link.

# If You Have a Mobile Link, Input the Link in Quotes ("/').

try:
    from bs4 import BeautifulSoup
    import requests, sys
except ImportError:
    print "Missing Dependencies!"
    install_ = str(raw_input("Install Dependencies? [Y/N]: ")).upper()
    if install_ == "Y" or install_ == "YES":
        import pip
        pip.main(["install", "bs4"])
        pip.main(["install", "lxml"])
        pip.main(["install", "requests"])
    elif install_ == "N" or install_ == "NO":
        exit("\nCan't Continue Without Dependencies!")
    else:
        exit("\n")

def getPostDownloadableLinkPic(postLink):
    req = requests.get(postLink)
    if req.status_code == 200:
        src = req.text
        txt = BeautifulSoup(src, "lxml")
        postLink = txt.find('meta', property="og:image")
        print "Post Downloadable Link:",postLink.attrs['content']
    elif req.status_code == 404:
        print "Account Private"
    else:
        print "Status Code:",req.status_code

def getPostDownloadableLinkVid(postLink):
    try:
        req = requests.get(postLink)
        if req.status_code == 200:
            src = req.text
            txt = BeautifulSoup(src, "lxml")
            postLink = txt.find('meta', property="og:video")
            if postLink == None:
                print "Not a Video!"
            else:
                print "Post Downloadable Link:",postLink.attrs['content']
        elif req.status_code == 404:
            print "Post Not Found / Account Private"
        else:
            print "Status Code:",req.status_code
    except Exception as errstr:
        exit("\nError Occured! Check Your Internet Connection!\n"+str(errstr))

def main():
    try:
        postLink = str(sys.argv[1])
        picOrVid = str(sys.argv[2])
        if postLink == None or picOrVid == None:
            print "Usage: python postGram.py *post link* *[P]icture/[V]ideo*"
        if picOrVid == "P" or picOrVid == "PICTURE" or picOrVid == "p" or picOrVid == "picture" or picOrVid == "Picture":
            if "http://" not in postLink:
                postLink = "http://"+postLink
            getPostDownloadableLinkPic(postLink)
        elif picOrVid == "V" or picOrVid == "VIDEO" or picOrVid == "v" or picOrVid == "video" or picOrVid == "Video":
            getPostDownloadableLinkVid(postLink)
    except EOFError:
        exit("\nExiting...")
    except KeyboardInterrupt:
        exit("\nExiting...")
    except IndexError:
        exit("\nUsage: python postGram.py link [P]icture/[V]ideo")

if __name__ == "__main__":
    main()
