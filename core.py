import datetime
import random
import sys
import math
import praw
import thoughts

try:
    from secrets import SECRETS
except ImportError as ex:
    print("secrets.py file can't be accessed\n")
    print(ex)
    sys.exit()
except SyntaxError as ex:
    print("There is a syntax error in the secrets.py\n")
    print(ex)
    sys.exit()

# Set a descriptive user agent to avoid getting banned.
# Do not use the word 'bot' in your user agent.
def get_reddit():
    return praw.Reddit(
        client_id=SECRETS["client_id"],
        client_secret=SECRETS["client_secret"],
        username=SECRETS["username"],
        password=SECRETS["password"],
        user_agent='40kLoreModServitor'
    )

def imperial_date_now():
    current_date_time = datetime.datetime.now()
    start_of_year = datetime.datetime(current_date_time.year, 1, 1)
    end_of_year = datetime.datetime(current_date_time.year, 12, 31)
    difference_to_date = current_date_time - start_of_year
    seconds_since_start_of_year = difference_to_date.total_seconds()
    total_seconds_in_year = (end_of_year - start_of_year).total_seconds()

    year_fraction = math.floor(
        (seconds_since_start_of_year / total_seconds_in_year) * 1000)

    year = current_date_time.strftime("%y").zfill(3)

    return "0 " + "%03d" % year_fraction + " " + year + " M3"

def build_message(author, subject, message):
    ref = "%016d" % random.randint(0, 9999999999999999)
    body = (
        "\\+ + + + + + + + + + + + + + TRANSMITTED: Terra\n\n"
        "\\+ + + + + + + + + + + + + + RECEIVED: /u/" + author + "\n\n"
        "\\+ + + + + + + + + + + + + + DATE: " + imperial_date_now() + "\n\n"
        "\\+ + + + + + + + + + + + + + TELEPATHIC DUCT: Snoo\n\n"
        "\\+ + + + + + + + + + + + + + REF: HLT/" + ref + "/LA\n\n"
        "\\+ + + + + + + + + + + + + + AUTHOR: /u/40kLoreModServitor\n\n"
        "\\+ + + + + + + + + + + + + + SUBJECT: " + subject + "\n\n"
        "\\+ + + + + + + + + + + + + + THOUGHT FOR THE DAY: " \
        + thoughts.get_thought_for_the_day() + "\n\n"
        "\\>>BEGIN TRANSMISSION<<\n\n"
        "\\>>PROCESSING<<\n\n"
        "\\>>DOWNLOAD COMPLETE<<\n\n"
        + message + "\n\n"
        "\\>>END CODED MESSAGE<<\n\n"
        "\\>>TRANSMISSION TERMINATED<<"
    )

    return body
