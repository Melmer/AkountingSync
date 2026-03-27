# AkountingSync
Sync scripts to be able to sync the sales information to Akounting.



## Setup

pip install -r requirements.txt
cp .env.example .env   # fill in your own tokens
python3 sync.py        # test manually

## Cron Setup

crontab -e
```

Add (every hour):
```
0 * * * * cd /pad/naar/etsy-akaunting-sync && /usr/bin/python3 sync.py >> sync.log 2>&1
```

