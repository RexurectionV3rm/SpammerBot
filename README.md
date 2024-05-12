# SPAMMER BOT 📣

The Spammer Bot is a bot finalized to advertise your products in specified buy and sell groups.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following packages.

```bash
pip install pyrogram, pyromod, tgcrypto, apscheduler
```
The packages are needed to make the bot work properly.
TgCrypto is "optional", however it would make the bot signficantly faster.

Change the following settings:
```python
API_ID = 1 # YOUR API ID
API_HASH = "1" # YOUR API HASH
BOT_TOKEN = "1" # YOUR BOT_TOKEN
USE_PROXIES = False # DEFAULT False, TO USE PROXIES, LOAD PROXIES IN "proxies.txt"
```
Into your API keys, if you don't have API keys you can create an App to generate them [here](https://my.telegram.org/apps).
You can choose either using proxies or not by changing the boolean to "True" or "False".

## Usage

You can easily understand how the bot works by starting it.
To start spamming, you must firstly add atleast 1 group, and a VoIP.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
