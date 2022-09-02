#  Usernotes Notifier Bot v.1.0 by u/BuckRowdy

from datetime import datetime
import praw
import time
import pmtw
import re

reddit = praw.Reddit(
    user_agent="Usernotes Notifier Bot v.1.0 by u/BuckRowdy",
    client_id="",
    client_secret="",
    username = "",
    password = "",
)
print("Connecting to reddit...")
print("Starting up...")
print(f"Logged in as: {reddit.user.me()}\n")

# Set a threshold for the number of notes you want to be notified of.
note_threshold = 5

#  Stream the mod log.  Use skip_existing so that it won't process old entries.
for log in reddit.subreddit("mod").mod.stream.log(skip_existing=True):
    # Pass mod log action attributes into variables for later use.
    log_subreddit = log.subreddit
    # The way the subreddit name is assigned on this line is necessary for PMTW to properly process usernotes.
    sub_name = reddit.subreddit(f"{log_subreddit}")
    log_details = log.description

    # Monitor the mod log for 'wikirevise' actions, the corresponding mod action for usernote additions.
    if log.action == "wikirevise":
        # Extract the reddit username from the mod log entry when a usernote is left.
        match = re.search(
            r"\bcreate new note on ([\w-]{3})?.?user \x27?([\w-]{3,20})", log_details
        )
        # If a match is found, extract the second matching group which will be the reddit username.
        if match:
            username = match.group(2)
            print(f"New Note left in r/{sub_name}")
            # Activate PMTW, a module for working with toolbox's usernotes.
            notes = pmtw.Usernotes(reddit, sub_name)
            settings = pmtw.Settings(reddit, sub_name)
            # Fetch usernotes with PMTW.
            users_notes = notes.get_user_notes(username)
            note_list = [
                f"**I found the following notes for u/{username}** starting with the most recent:"
            ]
            # Count the notes associated with the user.
            for notecount, note in enumerate(users_notes):
                note_list.append(
                    f"Note: '{note.note}' on {datetime.fromtimestamp(note.time)} - Warn type: {note.warning}"
                )
                notecount = notecount + 1
            print(f"Total Notes for u/{username}: {notecount}")
            # Format the note list on separate lines to make it easier to read.
            for note in note_list:
                new_notelist = "\n\n".join(note_list)
            # If the user has over a set number of usernotes, start a mod discussion, if the bot doesn't have mail perms it will send a new modmail message.
            if notecount >= note_threshold:
                message_title = f"Usernotes update on u/{username}"
                message_body = f"This message is to let you know that u/{username} now has **{notecount}** usernotes on their account in r/{sub_name}. Please investigate as necessary.\n\n{new_notelist}"
                reddit.subreddit(f"{sub_name}").message(
                    subject=message_title, message=message_body
                )
                print("Message sent.\n\n")
