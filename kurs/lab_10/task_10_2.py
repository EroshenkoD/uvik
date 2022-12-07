import os
from time import time
from multiprocessing import Process
from multiprocessing import Queue


NUM_CPU = os.cpu_count()
SYMBOL = "q"
Queue = Queue()
LEN_STRING = 4000000


def create_string_symbols(name_file, symbol, len_string):
    symbol_string = ""
    for i in range(len_string):
        symbol_string += symbol
    with open(name_file, "w") as f:
        f.write(symbol_string)


def create_string_symbols_multiprocessing(q_name_file, symbol, len_string):
    while not q_name_file.empty():
        create_string_symbols(q_name_file.get(), symbol, len_string)


if __name__ == "__main__":
    print(f"number CPU: {NUM_CPU}")

    start_time = time()
    for num_page in range(NUM_CPU):
        create_string_symbols(f"files/file_{num_page}.txt", SYMBOL, LEN_STRING)
    print("Basic: %s seconds" % round((time() - start_time), 2))

    start_time = time()
    list_processing = []
    for num_page in range(NUM_CPU):
        Queue.put(f"files_processing/file_{num_page}.txt")

    for p in range(NUM_CPU):
        process = Process(
            target=create_string_symbols_multiprocessing,
            args=(
                Queue,
                SYMBOL,
                LEN_STRING,
            ),
        )
        list_processing.append(process)
        process.start()

    for p in list_processing:
        p.join()
    print("Processing: %s seconds" % round((time() - start_time), 2))
