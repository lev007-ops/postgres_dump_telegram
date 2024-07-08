import subprocess
import requests
import datetime
from environ import Env
import json
from loguru import logger
import os

env = Env()
Env.read_env()

DUMP_DIR = env.str('DUMP_DIR')
TOKEN = env.str('TOKEN')
CHAT_ID = env.str('CHAT_ID')
LOG_FILE = env.str('LOG_FILE', default='dump_log.log')

# Настройка loguru
logger.add(LOG_FILE, rotation="1 week", retention="1 month", level="INFO")


def read_databases(path: str):
    with open(path, 'r') as file:
        json_data = json.load(file)
    return json_data


def create_dump(db_info):
    dump_file = f'{DUMP_DIR}/{db_info["name"]}_{datetime.datetime.now().strftime("%Y%m%d")}.sql'
    env = os.environ.copy()
    env['PGPASSWORD'] = db_info['password']
    logger.info(f"Creating dump for database {db_info['name']}")
    subprocess.run(['pg_dump', '-U', db_info['user'], '-h', db_info['host'],
                   '-p', db_info['port'], db_info['name'], '-f', dump_file], env=env)
    return dump_file


def compress_file(file_path):
    logger.info(f"Compressing file {file_path}")
    subprocess.run(['gzip', file_path, '-f'])
    return f'{file_path}.gz'


def send_file_telegram(file_path):
    logger.info(f"Sending file {file_path} to Telegram")
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
    with open(file_path, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': CHAT_ID}
        response = requests.post(url, data=data, files=files)
    return response.json()


def delete_old_dumps(directory, days=7):
    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(days=days)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if file_path.endswith(".sql") or file_path.endswith(".gz"):
                file_mtime = datetime.datetime.fromtimestamp(
                    os.path.getmtime(file_path))
                if file_mtime < cutoff:
                    logger.info(f"Deleting old dump file {file_path}")
                    os.remove(file_path)


def dump_and_send():
    for db_info in read_databases("databases.json"):
        try:
            dump_file = create_dump(db_info)
            gzip_file = compress_file(dump_file)
            send_file_telegram(gzip_file)
            logger.info(f'Successfully backed up and sent {db_info["name"]}')
        except Exception as e:
            logger.error(f'Failed to back up {db_info["name"]}: {e}')

    delete_old_dumps(DUMP_DIR)


if __name__ == '__main__':
    dump_and_send()
