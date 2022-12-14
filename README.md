# notesbot.py
Notify a subreddit when a user has received too many toolbox usernotes.

To run this bot, you'll need to edit the script with your information.

- Set up the bot's login credentials via your reddit preferences.
- Enter the path for a text file that will be used to store a user blacklist (so they won't be notifed about again).  See comments in code for more info.
- Set your notes threshold at which you want to be notified about. 
- Install PMTW via pip https://pypi.org/project/pmtw/  

Notesbot listens to a mod log stream for new entries of "wikirevise" which is the action logged when a usernote is left.  When it's listening it will appear stalled or not working.  Once a new note is left it will print to the console. 

When a user receives a new note bringing their total count of notes equal to the threshold you set, a new modmail will be sent.  If the bot doesn't have mail perms, a standard modmail message will be sent.  This is the prefered notification method so that you can archive messages.  

A user blacklist is stored as a dictionary with usernames and subreddits as keys and values.  Once a user crosses the threshold, a new notification is sent and the user is added to the blacklist.  The blacklist is then written to a text file so that it is persistent across runs and/or crashes.  You will need to specify the location for your text file, known as the file path or path.  
