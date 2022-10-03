#  Usernotes Notifier Bot v 1.0 by u/BuckRowdy
#  Notify a subreddit when a user gets too many toolbox usernotes.

# Import modules.  PMTW is not a standard module and must be installed.
from datetime import datetime as datetime
import time
from time import strftime, localtime, timezone
import pmtw
import re
import json

reddit = praw.Reddit(
	user_agent="UserNotes Notifier Bot v1.0 by u/BuckRowdy",
	username = '',
	password = '',
	client_id="",
	client_secret=""
	
)
print("Connecting to reddit...")
print("Starting up...")
print(f"Logged in as: {reddit.user.me()}")

# Set user threshold for which you want to be notified.
note_threshold = 5

# Initialize a user blacklist dictinary to store user infomation to prevent repetitive modmails.
user_blacklist = {}

#Time stamp information
currentSysTime = time.localtime()

	 
# Load the user blacklist from a text file.  If file doesn't exist, it will be created.  You must specify your file path, and the file extension is .json
# Given a folder named 'bots' in your documents folder on windows, your file path would be something like: C:\Users\USERNAME\Documents\bots\usernotes_log.json
# for MacOS it would be ~/Documents/bots/usernotes_log.json.  Linux: /home/COMPUTERNAME/Documents/bots/usernotes_log.json
with open("/FILE/PATH/TO/YOUR/USERNOTES_BLACKLIST.json", "r+") as outfile:	
	try:
		user_blacklist = json.load(outfile)
	except Exception:
		pass  

	# Start the mod log stream and skip posts already in the log.
	# The bot runs on r/mod, if you want to exempt a subreddit entirely, change 'mod' to 'mod-subreddit'.  
	print("Listening for new usernotes...")
	for log in reddit.subreddit('mod').mod.stream.log(skip_existing=True):
		log_subreddit = log.subreddit
		sub_name = reddit.subreddit(f"{log_subreddit}")
		# Grab the log description, a string from which the reddit username will need to be extracted. 
		log_details = log.description
		#To set a different threshold for one specific subreddit.
		if log.subreddit == 'SUBREDDIT_NAME':
			note_threshold = 30
					
		if log.action == "wikirevise":
			# Notes left with toolbox, flair_helper, and pmtw all use this syntax when leaving a note on a user: 'create new note on (new) user u/USERNAME'.
			# Regex searches the string from the attribute, log.description for the reddit username and extracts it. 
			match = re.search(
				r"\bcreate new note on ([\w-]{3})?.?user \x27?([\w-]{3,20})", log_details
			)
			# If a valid username is extracted from the log description, count and categorize the notes then add to a list.
			if match:
				# Username will be pulled from the second match group, the first match group checks for 'new' which is not always present.
				username = match.group(2)
				# Print a time reference to the terminal so you can orient yourself as to when the last usernote was left.
				print("New usernote found - " + time.strftime('%m/%d/%Y @ %H:%M:%S', currentSysTime))
				print(f"Note found for r/{sub_name} left by u/{log.mod}")
				# Required code for PMTW.
				# When running on r/mod, the second argument, 'sub_name' must be an subreddit object, and not a string.  This is passed from line 48.
				notes = pmtw.Usernotes(reddit, sub_name)
				settings = pmtw.Settings(reddit, sub_name)
				users_notes = notes.get_user_notes(username)
				# Create a list for the usernote report with reddit table markdown formatting. 
				note_list = []
				table_header = 'Note | When | Warn Type | Mod | Link\n---|---|----|----|----\n'
				# Count the number of usernotes, and add a formatted list entry for each one. 
				for notecount, note in enumerate(users_notes):
					note_list.append(
						f"{note.note} | {datetime.fromtimestamp(note.time)} | {note.warning} | {note.mod} | [link]({note.link})"
					)
					# Notecount begins at zero, so adding one to this number gives us the correct number of notes. 
					notecount = notecount + 1
				print(f"Total Notes for u/{username}: {notecount}")
				#Format the usernote entries for a reddit table.  
				for note in note_list:
					new_notelist = "\n".join(note_list)
					
				# Once the number of notes on an account equals the threshold number, the main bot function is triggered. 
				if notecount >= note_threshold:
					if username in user_blacklist:
						if log_subreddit in user_blacklist[username]:
							print(f"This user is already in the user blacklist for {log_subreddit}.")
					else:
						message_title = f"Usernotes update: u/{username} now has {notecount} notes in r/{sub_name}."
						message_body = f"**I found the following notes for u/{username}**:\n\n"+table_header+new_notelist		
						reddit.subreddit(f"{sub_name}").message(
							subject=message_title, message=message_body
						)
						user_blacklist[username] = log_subreddit
					
						print(f"Message was sent and user added to blacklist for {log_subreddit}.\n")
						with open("/FILE/PATH/TO/YOUR/USERNOTES_BLACKLIST.json", "r+") as outfile:
							json.dump(user_blacklist, outfile) 


						
