import time


def make_series(iterations, param1, param2):
    start = time.time()
    result = 0
    for i in range(1, iterations):
        j =  i*param1 - param2
        result -= 1/j
        j = i*param1 + param2
        result += 1/j
    print (result)
    
    end = time.time()
    return end - start


print(make_series(100000000, 4, 1))