# Twitter Feed

_Version 0.1.1_ — _Developed to try out the Twitter API_

Reads a user's Twitter feed via the Twitter API and stores the content
into a `.csv` file.

The `.csv` file can then be imported into Microsoft Excel, or any other
software that can read Comma Separate Value files.

Requires Python 3.x, tested with Python 3.6.4.

## Usage

This software utilizes the Twitter API, which requires authentication.

Visit https://apps.twitter.com to get a free API key.  This will give
you two values, a _Consumer Key_ and a _Consumer Secret_; you'll need
both.

Unix:

    $ export TWITTER_API_CONSUMER_KEY="abc123...xzy789"
    $ export TWITTER_API_CONSUMER_SECRET="xyzzy...plugh"
    $ python3 ./TweeterFeed.py name1 name2 name3...
    
Windows:

    $ set TWITTER_API_CONSUMER_KEY="abc123...xzy789"
    $ set TWITTER_API_CONSUMER_SECRET="xyzzy...plugh"
    $ python3 ./TweeterFeed.py name1 name2 name3...
    
## About Generated CSV Files
Generated `.csv` files are likely to contain Unicode characaters, and this
may cause a problem for some software.

The first line of the `.csv` file will contain a header, describing the fields;
what fields are presented varies depending on the version of this
software.

All fields are quoted. This is because some of the numbers and dates
obtained are pretty detailed, and Microsoft Excel (for one) has a
problem parsing them correctly.  Usually a File / Import... will work,
although you may have to select all the columns and change them from
Generate to Text format.


# First Time Setup and Newbies
You'll need Python 3 and the latest copy of pip installed first.

Both of these commands should return version numbers, if properly
installed.

    $ python --version
    $ pip --version
    
Check out this project:

    $ git clone git@github.com:wls/TweetFeed.git
    
Then install the dependencies:

    $ pip install -r requirements.txt
    