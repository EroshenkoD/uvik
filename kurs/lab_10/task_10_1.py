"""
Image parser
Write a program that downloads images (at least 10) from the given site (choose whatever you want).

Note: use threads for this task (at least 3 threads should be spawned)

Bonus task: parse all the images from the site using bs4
"""
import re
import requests
import time
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread


NUM_PAGE = 5
NUM_IMG = 5
NUM_THREADS = 5
BASIC_PART = "img"
THREAD_PART = "thread_img"
q = Queue()


def download_img(img_url, part_to_save):
    res = requests.get(img_url, stream=True)
    filename = f"{part_to_save}/{img_url.split('/')[-1]}"
    with open(filename, "wb") as f:
        for block in res.iter_content(1024):
            f.write(block)


def get_list_car_img(url_site, col_picture):
    list_url_photo = []
    page = requests.get(url_site)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        list_car = soup.findAll("picture")
        col_picture = len(list_car) if col_picture > len(list_car) else col_picture
        for j in range(col_picture):
            cur_car = list_car[j]
            url_photo = re.search(r"src=.+jpg", str(cur_car))
            list_url_photo.append(url_photo.group(0)[5:])
    return list_url_photo


def find_and_download_img_thread(q_for_thread, col_picture, part_to_save):
    while True:
        site_url = q_for_thread.get()
        list_url_photo = get_list_car_img(site_url, col_picture)
        for url_for_img in list_url_photo:
            download_img(url_for_img, part_to_save)
        q.task_done()


if __name__ == "__main__":

    start_time = time.time()
    for num_page in range(NUM_PAGE):
        url = f"https://auto.ria.com/uk/legkovie/?page={num_page}"
        list_img = get_list_car_img(url, NUM_IMG)
        for url_img in list_img:
            download_img(url_img, "img")
    print("Basic: %s seconds" % round((time.time() - start_time), 2))

    start_time = time.time()

    for num_page in range(NUM_PAGE):
        q.put(f"https://auto.ria.com/uk/legkovie/?page={num_page}")

    for t in range(NUM_THREADS):
        worker = Thread(
            target=find_and_download_img_thread, args=(q, NUM_IMG, THREAD_PART)
        )
        worker.daemon = True
        worker.start()

    q.join()
    print("Thread: %s seconds" % round((time.time() - start_time), 2))
