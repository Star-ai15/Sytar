
# Star Token Airdrop Bot

## Deploy (Vercel Cron / AWS Lambda)
1. Set environment variable `PRESALE_SECRET` = base64 of your presale wallet secret key
2. Install deps: `pip install -r requirements.txt`
3. Run `python main.py` or deploy as a scheduled function (every minute)

The bot scans new SOL deposits to the presale wallet and sends equivalent STAR tokens automatically.
