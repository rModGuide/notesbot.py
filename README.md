# usernotes_notifier.py
Notify a subreddit when a user has received a set number of toolbox usernotes.

To run this bot, set up your login credentials using your reddit preferences.  Then enter them in the appropriate space.

Then set your threshold at the top and run the script.  

When the bot runs it will monitor the mod log for wikirevise actions indicating a new usernote was left.  It will ignore actions for other types of wikirevise actions such as saving your automoderator config.  When a user receives a new note and their total count of notes equals the threshold you set, a new modmail discussion will be sent.  If the bot has mail perms, it will send as a new mod discussion.  If not, it will send as a regular modmail message.  

To use the bot you'll need to install the PMTW module.  https://pypi.org/project/pmtw/
