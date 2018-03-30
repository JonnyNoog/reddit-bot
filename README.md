Moderator bot for r/40kLore
================

Python scripts for handling:

* incoming PMs with a view to assigning flair based on their content.
* Changing the type of posts allowed on the sub-reddit (any, link, self).

Requires Python 2.x or newer and PRAW 4.x or newer.

These scripts are used by https://reddit.com/r/40kLore.

These scripts expect a file called `secrets.py` to be in the same directory, with this structure:

    SECRETS = {
        'client_id': 'client_id_goes_here',
        'client_secret': 'client_secret_goes_here',
        'username': 'bot_account_username_goes_here',
        'password': 'bot_account_password_goes_here'
    }

Thanks to https://github.com/gavin19/reddit-flair-bot for the original code.

## LICENSE

The MIT License (MIT)

Copyright (c) 2015 JonnyNoog

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
