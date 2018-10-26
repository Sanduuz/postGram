#!/usr/bin/env python
#-*- coding: utf-8 -*-

try:
    import requests, re, sys, getpass, urllib, json, pyperclip
except ImportError:
    print "[!] Missing Dependencies!"
    install_ = str(raw_input("[?] Install? [Y/N]: "))
    if install_.upper() == "Y" or install_.upper() == "YES":
        print "[*] Importing pip..."
        import pip
        if pip.__version__.split('.')[0] > 9:
            exit("[!] pip seems to be running on version "+str(pip.__version__)+" which does not support module installation through scripts.\nPlease downgrade to 9.0.3 (max) [See README.md]")
        else:
            pip.main(["install", "requests"])
            pip.main(["install", "getpass"])
            pip.main(["install", "urllib"])
            pip.main(["install", "pyperclip"])
    elif install_.upper() == "N" or install_.upper() == "NO":
        print "[!] Script might not work properly! Please install the dependencies."

video_regex = r'og:video" content="(.*)"'
image_regex = r'og:image" content="(.*)"'
csrft_regex = r'csrf_token":"(.*?)"'

ses = requests.Session()

def login(username, password):
    loginURL = "https://www.instagram.com/accounts/login/ajax/"
    print "[*] Acquiring CSRF Token..."
    csrftoken = re.findall(csrft_regex, requests.get("https://www.instagram.com/accounts/login").text)[0]
    print "[+] CSRF Token Acquired:",csrftoken
    login_data = {"username":username, "password":password}
    headers = {"User-Agent":"postGram.py",
               "X-Instagram-AJAX":"1",
               "X-CSRFToken":csrftoken,
               "X-Requested-With":"XMLHttpRequest",
               "Referer":"https://www.instagram.com",
               "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
               "Cookie":"csrftoken="+csrftoken
    }
    loginReq = ses.post(loginURL, data=urllib.urlencode(login_data).encode('ascii'), headers=headers)
    resp = json.loads(loginReq.text)
    return resp

def getCredz():
    try:
        with open("./credentials", "r") as credz:
            credentials = credz.readlines()
            username = credentials[0].strip("\n")
            password = credentials[1]
            return True
    except IOError:
        return False

def main(postLink):
    try:
        postReq = ses.get(postLink)
        video_ = re.findall(video_regex, postReq.text)[0]
        if video_ == []:
            image_ = re.findall(image_regex, postReq.text)[0]
            if image_ == []:
                print "[-] Nothing found! Invalid link/user private."
            else:
                print "[+] Success!\nDownload link:",image_
                pyperclip.copy(image_)
                print "[*] Link copied to clipboard!"
        else:
            print "[+] Success!\nDownload link:",video_
            pyperclip.copy(video_)
            print "[*] Link copied to clipboard!"
    except KeyboardInterrupt:
        exit("[*] Exiting...")
    except EOFError:
        exit("[*] Exiting...")

if __name__ == "__main__":
    try:
        login_ = str(raw_input("[?] Login [Y/N]: "))
        if login_.upper() == "Y" or login_.upper() == "YES":
            while True:
                try:
                    credentalsDone = getCredz()
                    if credentialsDone == False:
                        username = str(raw_input("[?] Username: "))
                        password = getpass.getpass("[?] Password: ")
                    resp = login(username, password)
                    if resp['authenticated'] == True:
                        print "[+] Successfully logged in!"
                        if credentialsDone == False:
                            print "[?] Save credentials? (Insecure) [See README.md]"
                            save_ = str(raw_input("[?] Save credentials? [Y/N]: "))
                            if save_.upper() == "Y" or save_.upper() == "YES":
                                print "[*] Saving credentials..."
                                with open("./credentials", "w") as credFile:
                                    credFile.write(username)
                                    credFile.write("\n")
                                    credFile.write(password)
                                print "[+] Credentials successfully saved!"
                                credentialsDone = True
                        postLink = str(raw_input("[?] Link to post: "))
                        if "http" not in postLink:
                            postLink = "https://"+str(postLink)
                        main(postLink)
                    elif resp['authenticated'] == False:
                        print "[-] Login failed! Wrong username/password!"
                    else:
                        exit("[?] Unknown Error!")
                except KeyboardInterrupt:
                    exit("[*] Exiting...")
                except EOFError:
                    exit("[*] Exiting...")
        elif login_.upper() == "N":
            print "[!] Posts that are on private accounts can't be downloaded if you're not logged in."
            postLink = str(raw_input("[?] Link to post: "))
            if "http" not in postLink:
                postLink = "https://"+str(postLink)
            main(postLink)
    except KeyboardInterrupt:
        exit("[*] Exiting...")
    except EOFError:
        exit("[*] Exiting...")

