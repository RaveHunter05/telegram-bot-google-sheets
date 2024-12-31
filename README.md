# Small Program For Manage Subscriptions Data Using Google Sheets API and Telegram Bot With Python

This is a small program that uses the google sheets API to manage subscriptions data and a telegram bot to notify the user about the new subscriptions. The program lists all the subscriptions, paid and unpaid clients separately.

## Features
- List all subscriptions, paid and unpaid clients separately.

## How to use
1. Clone the repository.
2. Install the required packages using the following command:
```bash
pip install -r requirements.txt
```

3. Create a google sheets and share it with the email address provided in the `credentials.json` file.
4. Run the program using the following command:
```bash
python main.py
```

## > [!NOTE]
> This program is written for educational purposes only. It is not intended to be used in a production environment.

## > [!WARNING]
> The program uses the google sheets API to interact with the google sheets. Make sure to keep the `credentials.json` file secure.

## > [!TIP]
> You can use the `--help` flag to see the available options.

## > [!IMPORTANT]
> The program requires the `credentials.json` file to interact with the google sheets. Make sure to keep it secure.
- In order to make the telegram bot work, you need to create a telegram bot and get the token. You can follow the instructions [here](https://core.telegram.org/bots#6-botfather) to create a telegram bot and get the token.

