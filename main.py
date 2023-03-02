import numpy
import multiprocessing
from pprint import pprint
import time

def perfomance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"час виконання функції {func.__name__}: {end_time - start_time} секунд.\n")
        return result
    return wrapper

def is_lucky(number):
    digits = [int(d) for d in number]
    first_sum = sum(digits[:3])
    second_sum = sum(digits[3:])
    return first_sum == second_sum

def lucky_tickets_count(chunk):
    results = len([digit for digit in chunk if is_lucky(digit)])
    return results

@perfomance
def multiprocess(num_threads, chunks):
    pprint("паралельно  з діленням на частини")
    with multiprocessing.Pool(processes=num_threads) as pool:
        results = pool.map(lucky_tickets_count, chunks)
        pprint(sum(results))

@perfomance
def multiprocess_without_chunks(num_threads, tickets_list):
    pprint("паралельно без ділення на частини")
    with multiprocessing.Pool(processes=num_threads) as pool:
        results = pool.map(is_lucky, tickets_list)
        pprint(len([result for result in results if result]))

@perfomance
def default(chunks):
    pprint("в один потік з діленням на частини")
    count = 0
    for chunk in chunks:
        count+=lucky_tickets_count(chunk)
    pprint(count)

if __name__ == '__main__':
    num_threads = multiprocessing.cpu_count()
    tickets_list = [str(i).zfill(6) for i in range(1, 1000000)] # створюємо ліст тікетів від 000001 до 999999
    chunks = numpy.array_split(tickets_list, num_threads)        # розбиваємо його на частини кратно кількості ядер процесору

    multiprocess(num_threads, chunks)
    multiprocess_without_chunks(num_threads, tickets_list)
    default(chunks)

