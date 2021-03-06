#!/usr/bin/env python
#-*- coding: utf-8 -*-

try:
	import requests, re, sys, getpass, urllib, json, webbrowser, pyperclip
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
			pip.main(["install", "webbrowser"])
	elif install_.upper() == "N" or install_.upper() == "NO":
		print "[!] Script might not work properly! Please install the dependencies."

#video_regex = r'og:video" content="(.*)"'
#image_regex = r'og:image" content="(.*)"'
video_regex = r'"video_url":"(.*?)"'
csrft_regex = r'csrf_token":"(.*?)"'
image_regex = r'display_resources":\[{"src":"(.*?)"' # This could be actually better.

logged_in = False

ses = requests.Session()

def loadConfig():
	try:
		with open("config.txt") as config_file:
			config_data_raw = config_file.read().strip()
		config_data_parsed = json.loads(config_data_raw)
		return config_data_parsed
	except:
		exit("[!] Error while parsing configuration file! See example configuration from README.md")

def login(username, password):
	loginURL = "https://www.instagram.com/accounts/login/ajax/"
	print "[*] Acquiring CSRF Token..."
	csrftoken = re.findall(csrft_regex, requests.get("https://www.instagram.com/accounts/login").text)[0]
	print "[+] CSRF Token Acquired:",csrftoken
	login_data = {"username":username, "password":password}
	headers = {
				"User-Agent":"postGram.py",
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
			return (True, username, password)
	except IOError:
		return (False, "Great...")

def main(postLink, settings):
	try:
		postReq = ses.get(postLink, allow_redirects=False)
		video_ = re.findall(video_regex, postReq.text)
		if video_ == []:
			image_ = re.findall(image_regex, postReq.text)
			if image_ == []:
				print "[-] Nothing found! Invalid link/user private."
			else:
				if len(image_) == 1:
					print "[+] Success!\nDownload link:",image_[0].replace("\\u0026","&")
					if settings["open_browser"] == True:
						webbrowser.open_new_tab(image_[0].replace("\\u0026","&"))
						print "[*] Post opened in new tab."
					if settings["copy_link"] == True:
						pyperclip.copy(str(image_[0].replace("\\u0026","&"))) 			# ARE THESE TOO AGGRESSIVE?
						print "[*] Link copied to clipboard."
					exit()
				elif len(image_) > 1:
					print "[*] Detected as slide post."
					linkAmount = 1
					for link in image_[1:]:
						print "[Image: {}] Success!\nDownload link: {}".format(linkAmount, link.replace("\\u0026","&"))
						if settings["open_browser"] == True:
							webbrowser.open_new_tab(image_[linkAmount].replace("\\u0026","&"))
							print "[*] Post opened in new tab."
						linkAmount += 1
					exit()
		else:
			image_ = re.findall(image_regex, postReq.text)
			if image_ == []:
				pass
			else:
				if len(image_) == 1:
					print "[+] Success!\nDownload link:",image_[0].replace("\\u0026","&")
					if settings["open_browser"] == True:
						webbrowser.open_new_tab(image_[0].replace("\\u0026","&"))
						print "[*] Post opened in new tab."
					if settings["copy_link"] == True:
						pyperclip.copy(str(image_[0].replace("\\u0026","&"))) 			# ARE THESE TOO AGGRESSIVE?
						print "[*] Link copied to clipboard."
					exit()
				elif len(image_) > 1:
					print "[*] Detected as slide post."
					linkAmount = 1
					for link in image_[1:]:
						print "[Image: {}] Success!\nDownload link: {}".format(linkAmount, link.replace("\\u0026","&"))
						if settings["open_browser"] == True:
							webbrowser.open_new_tab(image_[linkAmount].replace("\\u0026","&"))
							print "[*] Post opened in new tab."
						linkAmount += 1
			if len(video_) == 1:
				print "[+] Success!\nDownload link:",video_[0].replace("\\u0026","&")
				if settings["open_browser"] == True:
					webbrowser.open_new_tab(video_[0].replace("\\u0026","&"))
					print "[*] Post opened in new tab."
				if settings["copy_link"] == True:
					pyperclip.copy(str(video_[0].replace("\\u0026","&")))
					print "[*] Link copied to clipboard."
				exit()
			elif len(video_) > 1:
				print "[*] Detected as slide post."
				linkAmountDisp = 1
				linkAmount = 0
				for link in video_:
					print "[Video: {}] Success!\nDownload link: {}".format(linkAmountDisp, video_[linkAmount].replace("\\u0026","&"))
					if settings["open_browser"] == True:
						webbrowser.open_new_tab(video_[linkAmount].replace("\\u0026","&"))
						print "[*] Post opened in new tab."
					linkAmount += 1
					linkAmountDisp += 1
				exit()
	except KeyboardInterrupt:
		exit("[*] Exiting...")
	except EOFError:
		exit("[*] Exiting...")
	except requests.exceptions.ConnectionError:
		print "[!] Invalid link!"
	except requests.exceptions.InvalidSchema:
		print "[!] Invalid link!"
	except requests.exceptions.InvalidURL:
		print "[!] Invalid link!"

if __name__ == "__main__":
	while True:
		try:
			settings = loadConfig()
			if settings["prompt_login"] == False:
				print "[!] The \"prompt_login\" field is set to false in the configuration file."
				print "[-] You won't be able to download any posts from private accounts!"
				postLink = str(raw_input("[?] Link to post: "))
				if postLink == "":
					print "[*] Please input the link."
				else:
					if "http" not in postLink:
						postLink = "https://"+str(postLink)
					main(postLink, settings)
			elif settings["prompt_login"] == True:
				if logged_in == False:
					login_ = str(raw_input("[?] Login [Y/N]: "))
					if login_.upper() == "Y" or login_.upper() == "YES":
						while True:
							try:
								loadedFromConf = False
								loadFromConf = str(raw_input("[?] Load From Credentials File [Y/N]: "))
								if loadFromConf.upper() == "Y" or loadFromConf.upper() == "YES":
									credentialsDone = getCredz()
									if credentialsDone[0] == False:
										print "[!] Credentials file is missing! Please re-enter your credentials."
										username = str(raw_input("[?] Username: "))
										password = getpass.getpass("[?] Password: ")
										break
									elif credentialsDone[0] == True:
										username = credentialsDone[1]
										password = credentialsDone[2]
										loadedFromConf = True
										break
								elif loadFromConf.upper() == "N" or loadFromConf.upper() == "NO":
									username = str(raw_input("[?] Username: "))
									password = getpass.getpass("[?] Password: ")
									break
								else:
									print "[!] Invalid option '{}'".format(loadFromConf)
							except KeyboardInterrupt:
								exit("\n[*] Exiting...")
							except EOFError:
								exit("\n[*] Exiting...")
							except requests.exceptions.ConnectionError:
								exit("\n[!] Invalid link! Exiting...")
						resp = login(username, password)
						if resp['authenticated'] == True:
							print "[+] Successfully logged in as {}!".format(username)
							logged_in = True
							if loadedFromConf == False:
								print "[?] Save credentials? (Insecure) [See README.md]"
								while True:
									try:
										save_ = str(raw_input("[?] Save credentials? [Y/N]: "))
										if save_.upper() == "Y" or save_.upper() == "YES":
											print "[*] Saving credentials..."
											with open("./credentials", "w") as credFile:
												credFile.write(username)
												credFile.write("\n")
												credFile.write(password)
												print "[+] Credentials successfully saved!"
												credentialsDone = True
												break
										elif save_.upper() == "N" or save_.upper() == "NO":
											postLink = str(raw_input("[?] Link to post: "))
											if postLink == "":
												print "[*] Please input the link."
											else:
												if "http" not in postLink:
													postLink = "https://"+str(postLink)
												main(postLink, settings)
										else:
											print "[!] Invalid option '{}'".format(save_)
									except KeyboardInterrupt:
										exit("\n[*] Exiting...")
									except EOFError:
										exit("\n[*] Exiting...")
									except requests.exceptions.ConnectionError:
										exit("\n[!] Invalid link! Exiting...")
							elif loadedFromConf == True:
								postLink = str(raw_input("[?] Link to post: "))
								if postLink == "":
									print "[*] Please input the link."
								else:
									if "http" not in postLink:
										postLink = "https://"+str(postLink)
									main(postLink, settings)
							else:
								exit("[!] Unknown Error Occured! Please report this to Sanduuz.")
						elif resp['authenticated'] == False:
							print "[-] Login failed! Wrong username/password!"
						else:
							exit("[!] Unknown Error Occured! Please report this to Sanduuz.")
					elif login_.upper() == "N":
						print "[!] Posts that are on private accounts can't be downloaded if you're not logged in."
						postLink = str(raw_input("[?] Link to post: "))
						if postLink == "":
							print "[*] Please input the link."
						else:
							if "http" not in postLink:
								postLink = "https://"+str(postLink)
							main(postLink, settings)
					else:
						print "[!] Invalid option '{}'".format(login_)
				elif logged_in == True:
					postLink = str(raw_input("[?] Link to post: "))
					if postLink == "":
						print "[*] Please input the link."
					else:
						if "http" not in postLink:
							postLink = "https://"+str(postLink)
						main(postLink, settings)
				else:
					print "[!] Invalid option '{}'".format(login_)
			else:
				print "[!] Invalid value in configuration file for \"prompt_login\"!"
				print "\"prompt_login\" should be set to True/False."
				exit()
		except KeyboardInterrupt:
			exit("\n[*] Exiting...")
		except EOFError:
			exit("\n[*] Exiting...")
		except requests.exceptions.ConnectionError:
			exit("\n[!] Invalid link! Exiting...")
