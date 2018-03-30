import argparse
import core
import time
import prawcore

class LinkTypeBot:
    TARGET_SUBREDDIT = "40kLoreCSSTest"
    SUBMISSION_ID_FILENAME = "link_type_bot_submission_id.txt"
    reddit = core.get_reddit()

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.description='Change the allowed link type of the sub-reddit.'

        parser.add_argument(
            "--link-type",
            dest="link_type",
            help="The type of link to allow for the sub-reddit. "
            "Should be one of: any link self",
            type=str)

        parser.add_argument(
            "--post-submission",
            dest="submission_action",
            help="Post a submission and sticky it if there is space.",
            action='store_true')

        parser.add_argument(
            "--unsticky-submission",
            dest="submission_action",
            help="Unsticky the previously posted submission.",
            action='store_false')

        parser.add_argument(
            "--show-media",
            dest="show_media",
            help="Set to show thumbnails for submissions.",
            action='store_true')

        parser.add_argument(
            "--no-show-media",
            dest="show_media",
            help="Set to not show thumbnails for submissions.",
            action='store_false')

        args = parser.parse_args()
        link_type = args.link_type
        submission_action = args.submission_action
        show_media = args.show_media

        if link_type not in ("any", "link", "self"):
            raise argparse.ArgumentTypeError("Unknown link_type value")

        if submission_action not in (True, False):
            raise argparse.ArgumentTypeError("Unknown post_action value")

        if show_media not in (True, False):
            raise argparse.ArgumentTypeError("Unknown show_media value")

        self.set_link_type(link_type, show_media)
        self.post_message(submission_action)

    def set_link_type(self, link_type, show_media):
        self.reddit.subreddit(self.TARGET_SUBREDDIT).mod.update(
            link_type=link_type, show_media=show_media)

    def post_message(self, submission_action):
        subject = "Visual art day - " + time.strftime("%d %B %Y")
        message = core.build_message("u/40kLoreModServitor", subject,
        self.get_message())

        if submission_action:
            subreddit = self.reddit.subreddit(self.TARGET_SUBREDDIT)
            submission = subreddit.submit(subject, selftext=message)
            submission.mod.distinguish()

            sticky_posts = []

            # Check for existing sticky posts and if two already exist, then
            # post the submission unstickied.
            try:
                sticky_posts.append(subreddit.sticky(1))
                sticky_posts.append(subreddit.sticky(2))
            except prawcore.NotFound:
                pass

            if len(sticky_posts) > 1:
                self.reddit.submission(submission.id).mod.sticky(state=False)
                self.log("Posted " + subject + " (unstickied)")
            else:
                self.reddit.submission(submission.id).mod.sticky()
                self.log("Posted " + subject + " (stickied)")

            # Write the submission ID to the file system so that it can be used
            # later on to unsticky the submission.
            self.save_submission_id(submission)
        else:
            submission_id = self.get_submission_id()
            submission = self.reddit.submission(submission_id)
            submission.mod.sticky(state=False)
            self.log("Unstickied " + submission.title)

    def save_submission_id(self, submission):
        with open(self.SUBMISSION_ID_FILENAME, "w") as submission_id_file:
            submission_id_file.write(submission.id)
            submission_id_file.close()

    def get_submission_id(self):
        submission_id_file = open(self.SUBMISSION_ID_FILENAME, "r")
        return submission_id_file.read()

    def get_message(self):
        message_body = (
            "Greetings loyal imperial citizens. Rejoice, for today is the day "
            "that remembrancers of the visual arts are to be celebrated.\n\n"
            "For the next 24 hours you are free to post direct links to images"
            "relevant to the lore of our great universe.\n\n"
            "Be warned that memes, shitposts and low-effort posts of all kinds"
            "remain the vilest form of heresy and will be dealt with severely."
            "Do not post any such content during this most holy of days.\n\n"
            "Should you require any assistance, you may [send a transmission "
            "to the High Lords of Terra]"
            "(https://www.reddit.com/message/compose?to=%2Fr%2F40kLore).\n\n"
            "The Emperor protects."
        )

        return message_body

    def log(self, log_message):
        with open('link_type_bot_log.txt', 'a') as logfile:
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            log_text = log_message + " @ " + time_now + "\n"
            logfile.write(log_text)
            logfile.close()

LinkTypeBot()
