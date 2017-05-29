from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests
import hashlib

MAX_FILE_SIZE = 100 * 1024 * 1024 # 100mb
CHUNK_SIZE = 1024 * 1024 # 1mb

def url_is_valid(url):
    if not url:
        return False
    try:
        URLValidator()(url)
    except ValidationError:
       return False
    return True

def get_md5(task, url):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    # Checking file size
    files_size = int(r.headers['content-length'])
    if files_size > MAX_FILE_SIZE:
        raise Exception('file can\'t be large then '
            + str(MAX_FILE_SIZE/1024/1024) + 'mb, your file size is: '
            + str(int(r.headers['content-length'])/1024/1024) + 'mb')

    # Calculating number of iterations
    iters = files_size / CHUNK_SIZE
    i = 0
    # Getting file by chunks and hasing them
    hash = hashlib.md5()
    for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:  # filter out keep-alive new chunks
            hash.update(chunk)
            i += 1
            # Setting progress status for get requests from clients
            task.update_state(state='PROGRESS',
                              meta={"PROGRESS": int((i/iters)*100)})

    return hash.hexdigest()
