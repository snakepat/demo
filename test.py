# import time
import os

# class cached(object):
#     def __init__(self, f):
#         self.f = f
#         self.cache = {}

#     def __call__(self, *args):
#         if args in self.cache:
#             return self.cache[args]
#         else:
#             result = self.f(*args)
#             self.cache[args] = result
#             return result

#     def get_cache(self):
#         return self.cache

# @cached
# def fibonacci(n):
#     if n == 0:
#         return 0
#     elif n == 1:
#         return 1
#     else:
#         return fibonacci(n-1) + fibonacci(n-2)

if __name__ == "__main__":
    # start_time = time.time()
    # result = fibonacci(40)
    # end_time = time.time()
    a = [2,3,4,5,5,3,232,2,22,2,2]
    for i in range(len(a)):
        print(i)
    print(os.getcwd())

    # print(f"The 40th Fibonacci number is: {result}")
    # print(f"Execution time: {end_time - start_time:.6f} seconds.")

    # # Now, if we call fibonacci(40) again, it will be much faster
    # start_time = time.time()
    # result = fibonacci(40)
    # end_time = time.time()

    # print(f"The 40th Fibonacci number is: {result}")
    # print(f"Execution time: {end_time - start_time:.6f} seconds.")

    # # Accessing the cache content
    # cache_content = fibonacci.get_cache()
    # print("Cache content:")
    # for key, value in cache_content.items():
    #     print(f"{key}: {value}")
