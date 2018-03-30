#!/usr/bin/env python
import sys
import os
import time
import core

try:
    from flairs import FLAIRS
except ImportError as ex:
    print("flairs.py file can't be accessed\n")
    print(ex)
    sys.exit()
except SyntaxError as ex:
    print("There is a syntax error in the flair list\n")
    print(ex)
    sys.exit()

class FlairBot:
    # User blacklist
    BLACKLIST = [] # For example: ['sampleuser', 'sampleUSER2']

    # Sub-reddit to operate on.
    TARGET_SUBREDDIT = "40kLore"

    # Turn on output to log file in current directory - log.txt.
    LOGGING = True

    # Allow users to set their own flair text or not.
    ALLOW_CUSTOM_FLAIR_TEXT = False

    # PRAW object.
    reddit = core.get_reddit()

    # Class variable to hold the unread PMs.
    pms = None

    def __init__(self):
        if self.LOGGING:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))

        self.fetch_pms()

    def fetch_pms(self):
        # Get a listing of all unread PMs sent to the bot user account.
        self.pms = self.reddit.inbox.messages.unread(limit=None)

        if self.pms is not None:
            self.process_pms()

    def process_pms(self):
        for pm in self.pms:
            flair_id = str(pm.subject)
            author = str(pm.author)
            flair_text = str(pm.body)

            if author.lower() in (user.lower() for user in self.BLACKLIST):
                continue

            if flair_id in FLAIRS:
                # Extra categories beyond the one corresponding to the
                # spritesheet name aren't required for actual display of flair,
                # and can potentially mess up flair display. The extra
                # categories are only relevant for the JS filter code running on
                # the flair selection page. So remove any extra categories.
                flair_id_parts = flair_id.split(" ")
                flair_position = flair_id_parts[0]
                flair_sheet_name = flair_id_parts[1]

                if not self.ALLOW_CUSTOM_FLAIR_TEXT or not flair_text:
                    flair_text = str(FLAIRS[flair_id])

                try:
                    self.reddit.subreddit(self.TARGET_SUBREDDIT).flair.set(
                        author,
                        flair_text,
                        flair_position + " " + flair_sheet_name)

                    pm.reply(self.get_message(author, flair_id, "success"))
                except:
                    pm.mark_read()
            else:
                pm.reply(self.get_message(author, flair_id, "failure"))

            if self.LOGGING:
                self.log(author, flair_id, flair_text)

            pm.mark_read()

        sys.exit()

    def get_success_message(self, author, flair_id):
        flair_name = FLAIRS[flair_id]
        message = (
            "Greetings loyal imperial citizen, designation `" + author + "`. "
            "Your request for flair assignment has been considered by the Cult "
            "Mechanicus and you have been found worthy "
            "(praise the Emperor). Your chosen flair icon (designation `"
            + flair_name + "`) is now in effect.\n\n"
            "Your loyalty to the Imperium continues to be monitored and "
            "assessed. All transgressions will be reported to the Holy "
            "Inquisition.\n\n"
            "The Emperor protects."
        )

        return message

    def get_failure_message(self, author, flair_id):
        message = (
            "Greetings imperial citizen, designation `" + author + "`. Your "
            "request for flair assignment has been considered by the Cult "
            "Mechanicus and rejected. Your requested flair icon (designation `"
            + flair_id + "`) is not found on the Mechanicum sanctioned list of "
            "authorised flair icons. Your loyalty to the Imperium has now been "
            "brought into question and this transgression has been reported to "
            "the Holy Inquisition.\n\n"
            "In future, ensure that you do not alter the automatically "
            "generated flair request message in any way before sending it. "
            "Should you require assistance or hope to beg forgiveness, you may "
            "[send a transmission to the High Lords of Terra]"
            "(https://www.reddit.com/message/compose?to=%2Fr%2F40kLore).\n\n"
            "The Emperor protects."
        )

        return message

    def get_message(self, author, flair_id, message_type):
        if message_type == "success":
            message = self.get_success_message(author, flair_id)
        elif message_type == "failure":
            message = self.get_failure_message(author, flair_id)
        else:
            raise ValueError("Unknown message_type")

        subject = "Flair assignment " + message_type
        body = core.build_message(author, subject, message)

        return body

    def log(self, author, flair_id, flair_text):
        with open('flair_bot_log.txt', 'a') as logfile:
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

            log_text = "Author: " + author + " - Flair ID: '" + flair_id + \
            "' Flair text: '" + flair_text + "' @ " + time_now + "\n"

            logfile.write(log_text)
            logfile.close()

FlairBot()
