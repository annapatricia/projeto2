from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import Pool

import progressbar
import urllib.request

pbar = None


def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


def download_database(url, filename):
    try:
        print("Tentando baixar a url " + url)
        urllib.request.urlretrieve(url, filename, show_progress)
    except Exception as e:
        print("Erro ao baixar a url " + url)


if __name__ == '__main__':
    databases = open('databases', 'r')

    urls_filenames = []

    for line in databases.readlines():
        line = line.replace('\n', '')

        urls_filenames.append(tuple(line.split(' ')))

    databases.close()

    with ThreadPoolExecutor(max_workers=4) as executor:
        for urls_filename in urls_filenames:
            executor.submit(download_database, urls_filename[0], urls_filename[1])

    print("TERMINOU")
