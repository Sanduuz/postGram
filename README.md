# postGram2 | Download Instagram Posts

A tool for downloading posts from public instagram profiles.

---

## What is postGram?
postGram is a tool made for downloading Instagram posts from public users.

---

## Supported Operating Systems
 * Windows
 * Linux
 * Android

---

## Usage
```
python postGram2.py
```

### Bugs

If you are trying to install the dependencies through 
postGram, make sure your `pip --version` is max 9.0.3.

pip version 10.0.* doesn't support installing dependencies through the pip module in scripts.

You can downgrade to version 9.0.3 with `python -m pip install pip==9.0.3`

If you find any bugs, please report them to me ASAP!

You can contact me at:
* Instagram: @sanduuz
* E-mail: 19jdmz5js@protonmail.ch
* Wickr: @sanduuz
* Wire: @sanduuz

---

## What's New
### postGram v2
+ Improved data searching algorithm
+ Added login functionality for downloading private posts
+ Automatically copies link to clipboard
+ Allows saving credentials to configuration file. [INSECURE | SEE MORE INFO BELOW]
### postGram v1.1
+ Tweaks [if http:// not included in link, automatically added]
### postGram v1.0
+ Core Built

---

### Saving credentials
#### Saving credentials to configuration file makes logging in faster, but more insecure.
#### The credentials are saved in plaintext to a file called credentials.
#### Use this at your own risk and I am NOT responsible for anything you do with this.
#### Currently you can save only 1 account to the file, but in the future I'm working towards saving many accounts to the file.

---
---
---

# postGram | Download Instagram Posts [OUTDATED]

A tool for downloading posts from public instagram profiles.

---

## What is postGram?
postGram is a tool made for downloading Instagram posts from public users.

---

## Supported Operating Systems
 * Windows
 * Linux
 * Android

---

## Usage
```
python postGram.py link P/V
```

P stands for pictures and V for videos.

If you use the P flag for videos, you will get the thumbnail of the video.

### Examples:
```
python postGram.py "https://www.instagram.com/p/BkF4khTHctp/?utm_source=ig_share_sheet&igshid=ls9gad4okp34" P
```

```
python postGram.py https://www.instagram.com/p/BkF4khTHctp/ P
```

```
python postGram.py https://www.instagram.com/p/BdKx1XqBuqr V
```

#### Note:
Links copied from Instagram application might have extension /?utm_source=ig_share_sheet&igshid=*value*.
If using this application on phone, either remove the extension or input the link in quotes. ("/')

---

## Installation Guide (Android)
Installation Guide for Android. Windows and Linux systems doesn't need any installation.

You need a terminal emulator like Termux.

The installation is for installing lxml on python.

First try to install lxml by `pip2 install lxml`.

Errors will probably occur, but to fix them, try the next command.

`apt update && apt upgrade && apt dist-upgrade`

`apt install python2 python2-dev clang libcrypt libcrypt-dev libxml2 libxml2-dev libxml2-utils libxslt libxslt-dev`

After that try to install lxml again.

`pip2 install lxml`

It should work, if it didn't make sure to message me. (Contact Information Found Below)

To run the script, remember to use python2!

`python2 postGram.py`

---

### Bugs

If you are trying to install the dependencies through 
postGram, make sure your `pip --version` is max 9.0.3.

pip version 10.0.* doesn't support installing dependencies through the pip module in scripts.

You can downgrade to version 9.0.3 with `python -m pip install pip==9.0.3`

If you find any bugs, please report them to me ASAP!

You can contact me at:
* Instagram: @sanduuz
* E-mail: 19jdmz5js@protonmail.ch
* Wickr: @sanduuz
* Wire: @sanduuz

---

## What's New
### postGram v1.1
+ Tweaks [if http:// not included in link, automatically added]
### postGram v1.0
+ Core Built
