# Treadmill

I use [Pinboard](https://pinboard.in) to keep track of thousands of bookmarks. Each can have a title, description, tags, and be marked to be read later. Unfortunately I don't always take the time to fill all this information out every time I add a bookmark.

Treadmill is currently just a super simple Python script that sends an email every morning with:

* 5 "dirty" bookmarks that don't have tags or a proper title
* 1 bookmark that was marked to be read later and isn't dirty, as assigned reading

## Usage

You'll probably want a server somewhere that's always up to run this on.

Clone the repo and then add 2 files to it:

* **config.json** - JSON file with the keys:
  - "email" - your email address
  - "api_key" - your Mailgun API key
  - "mailgun_domain" - your Mailgun domain (the sandbox domain they give you works well)
* **token** - A file that just contains your Pinboard API token, which you can find [on this page](https://pinboard.in/settings/password)

Run `crontab -e` and add a line like the following to run the script every day at 6 AM:

```
0 6 * * * Mon /home/you/treadmill/treadmill.py
```

