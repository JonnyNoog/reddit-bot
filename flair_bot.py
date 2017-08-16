#!/usr/bin/env python
import sys
import os
from random import randint
from time import gmtime, strftime
from datetime import datetime
import math
import praw

try:
    from flair_list import FLAIRS
except ImportError as ex:
    print("flairs.py file can't be accessed\n")
    print(ex)
    sys.exit()
except SyntaxError as ex:
    print("There is a syntax error in the flair list\n")
    print(ex)
    sys.exit()
try:
    from secrets import SECRETS
except ImportError as ex:
    print("secrets.py file can't be accessed\n")
    print(ex)
    sys.exit()
except SyntaxError as ex:
    print("There is a syntax error in the secrets list\n")
    print(ex)
    sys.exit()

class FlairBot:
    # User blacklist
    BLACKLIST = [] # For example: ['sampleuser', 'sampleUSER2']

    # Set a descriptive user agent to avoid getting banned.
    # Do not use the word 'bot' in your user agent.
    reddit = praw.Reddit(
        client_id=SECRETS["client_id"],
        client_secret=SECRETS["client_secret"],
        username=SECRETS["username"],
        password=SECRETS["password"],
        user_agent='40kLore Auto Flair'
    )

    # Turn on output to log file in current directory - log.txt.
    LOGGING = True

    # Allow users to set their own flair text or not.
    ALLOW_CUSTOM_FLAIR_TEXT = False

    # Class variable to hold the unread pms.
    pms = None

    def __init__(self):
        if self.LOGGING:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))

        self.fetch_pms()

    def fetch_pms(self):
        # Get a listing of all unread PMs sent to the bot user account.
        self.pms = self.reddit.inbox.unread(limit=None)

        if self.pms is not None:
            self.process_pms()

    def process_pms(self):
        for pm in self.pms:
            flair_id = str(pm.subject)
            author = str(pm.author)
            pm_body = str(pm.body)

            split_pm_body = pm_body.split("\n")
            flair_text = ""
            target_subs = ""

            if len(split_pm_body) == 1:
                target_subs = split_pm_body[0]
            else:
                flair_text = split_pm_body[0]
                target_subs = split_pm_body[1]

            if author.lower() in (user.lower() for user in self.BLACKLIST):
                continue

            if flair_id in FLAIRS:
                # Extra categories beyond the one corresponding to the spritesheet
                # name aren't required for actual display of flair, and can
                # potentially mess up flair display. The extra categories are
                # only relevant for the JS filter code running on the flair
                # selection page.
                flair_id_parts = flair_id.split(" ")
                flair_position = flair_id_parts[0]
                flair_sheet_name = flair_id_parts[1]

                if not self.ALLOW_CUSTOM_FLAIR_TEXT or not flair_text:
                    flair_text = str(FLAIRS[flair_id])

                target_subreddits = target_subs.split(" ")

                for target_subreddit in target_subreddits:
                    try:
                        self.reddit.subreddit(target_subreddit).flair.set(author, flair_text, \
                        flair_position + " " + flair_sheet_name)
                        pm.reply(self.get_message(author, flair_id, "success"))
                    except:
                        pm.mark_read()

            else:
                pm.reply(self.get_message(author, flair_id, "failure"))

            if self.LOGGING:
                self.log(author, flair_id, pm_body, flair_text)

            pm.mark_read()

        sys.exit()

    def get_current_imperial_date(self):
        current_date_time = datetime.now()
        start_of_year = datetime(current_date_time.year, 1, 1)
        end_of_year = datetime(current_date_time.year, 12, 31)
        difference_to_date = current_date_time - start_of_year
        seconds_since_start_of_year = difference_to_date.total_seconds()
        total_seconds_in_year = (end_of_year - start_of_year).total_seconds()

        year_fraction = math.floor((seconds_since_start_of_year / total_seconds_in_year) * 1000)
        year = current_date_time.strftime("%y").zfill(3)

        return "0 " + "%03d" % year_fraction + " " + year + " M3"

    def get_thought_for_the_day(self):
        thought_for_the_day = [
            "Blessed is the mind too small for doubt",
            "Blind faith is a just cause",
            "Appeasement is a curse",
            "Compromise is akin to treachery",
            "A small mind is easily filled with faith",
            "Doubt forms the path to damnation",
            "Faith in the Emperor is its own reward",
            "Forgiveness is a sign of weakness",
            "Happiness is a delusion of the weak",
            "Hope is the first step on the road to disappointment"
        ]

        return thought_for_the_day[randint(0, 9)]

    def get_success_message(self, author, flair_id):
        flair_name = FLAIRS[flair_id]
        message = (
            "Greetings loyal imperial citizen, designation `" + author + "`. Your request for flair "
            "assignment has been considered by the Cult Mechanicus and you have been found worthy "
            "(praise the Emperor). Your chosen flair icon (designation `" + flair_name + "`) is "
            "now in effect.\n\n"
            "Your loyalty to the Imperium continues to be monitored and assessed. All "
            "transgressions will be reported to the Holy Inquisition.\n\n"
            "The Emperor protects."
        )

        return message

    def get_failure_message(self, author, flair_id):
        message = (
            "Greetings imperial citizen, designation `" + author + "`. Your request for flair "
            "assignment has been considered by the Cult Mechanicus and rejected. Your requested "
            "flair icon (designation `" + flair_id + "`) is not found on the Mechanicum sanctioned "
            "list of authorised flair icons. Your loyalty to the Imperium has now been brought "
            "into question and this transgression has been reported to the Holy Inquisition.\n\n"
            "In future, ensure that you do not alter your automatically generated flair request "
            "message in any way before sending it. Should you require assistance or hope to beg "
            "forgiveness, you may [send a transmission to the High Lords of Terra]"
            "(https://www.reddit.com/message/compose?to=%2Fr%2F40kLore).\n\n"
            "The Emperor protects."
        )

        return message

    def get_message(self, author, flair_id, message_type):
        ref = "%016d" % randint(0, 9999999999999999)

        if message_type == 'success':
            message = self.get_success_message(author, flair_id)
        elif message_type == 'failure':
            message = self.get_failure_message(author, flair_id)
        else:
            raise ValueError("Unknown message_type")

        body = (
            "\\+ + + + + + + + + + + + + + TRANSMITTED: Terra\n\n"
            "\\+ + + + + + + + + + + + + + RECEIVED: /u/" + author + "\n\n"
            "\\+ + + + + + + + + + + + + + DATE: " + self.get_current_imperial_date() + "\n\n"
            "\\+ + + + + + + + + + + + + + TELEPATHIC DUCT: Snoo\n\n"
            "\\+ + + + + + + + + + + + + + REF: HLT/" + ref + "/LA\n\n"
            "\\+ + + + + + + + + + + + + + AUTHOR: /u/40kLoreModServitor\n\n"
            "\\+ + + + + + + + + + + + + + SUBJECT: Flair assignment " + message_type + "\n\n"
            "\\+ + + + + + + + + + + + + + THOUGHT FOR THE DAY: " \
            + self.get_thought_for_the_day() + "\n\n"
            "\\>>BEGIN TRANSMISSION<<\n\n"
            "\\>>PROCESSING<<\n\n"
            "\\>>DOWNLOAD COMPLETE<<\n\n"
            + message + "\n\n"
            "\\>>END CODED MESSAGE<<\n\n"
            "\\>>TRANSMISSION TERMINATED<<"
        )

        return body

    def log(self, author, flair_id, pm_body, flair_text):
        with open('log.txt', 'a') as logfile:
            time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            log_text = "Added: " + author + " - Flair ID: '" + flair_id + "' Flair text: '" \
            + str(flair_text) + "' PM body: '" + pm_body + \
            "' @ " + time_now + "\n"
            logfile.write(log_text)

FlairBot()
