# PostgreSQL Backup and Telegram Notification Script

This project is a Python script for creating PostgreSQL database dumps, compressing them, sending them to Telegram, and automatically deleting old dumps.

## Description

The script performs the following actions:

1. Creates dumps of specified PostgreSQL databases.
2. Compresses the dumps using `gzip`.
3. Sends the compressed dumps to Telegram using the Telegram Bot API.
4. Deletes dumps older than one week to save disk space.

## Requirements

- Python 3.6 or higher
- PostgreSQL
- Installed dependencies from the requirements.txt file
- Telegram Bot Token and Chat ID

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:lev007-ops/postgres_dump_telegram.git
   cd postgres_dump_telegram
   ```

2. Create a virtual environment (optional):

```bash
python3 -m venv .venv
```

3. Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

4. Create a .env file in the root directory of the project and add the following lines:

```bash
BACKUP_DIR=/path/to/backup_dir
TOKEN=YOUR_TELEGRAM_BOT_TOKEN
CHAT_ID=YOUR_CHAT_ID
LOG_FILE=/path/to/backup_log.log  # Optional
```

5. Create a databases.json file in the root directory of the project and add information about your databases:

    ```json
    [
       {
           "name": "dbname1",
           "user": "user1",
           "host": "hostname1",
           "port": "5432"
       },
       {
           "name": "dbname2",
           "user": "user2",
           "host": "hostname2",
           "port": "5432"
       }
   ]
   ```

1. Set up the .pgpass file in the user's home directory for automatic connection to PostgreSQL databases:

    ```bash
    hostname1:5432:dbname1:user1:password1
    hostname2:5432:dbname2:user2:password2
    ```

    Ensure the file has the correct permissions:

    ```bash
    chmod 600 ~/.pgpass
    ```

## Usage

Run the script manually:

```bash
python backup_and_send.py
```

To automatically run the script daily, set up a cron job:

```bash
crontab -e
```

Add the following line to run the script every day at 2 AM:

```bash
0 2 * * * /path/to/postgres_dump_telegram/.venv/bin/python3 /path/to/backup_and_send.py
```

## Logging

The script uses the `loguru` library for logging. Logs are saved both to the console and to the file specified in the `LOG_FILE` environment variable.

## Support

If you have any questions or issues, please create an issue in this repository.

## Лицензия

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
