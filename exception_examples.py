class ThisIsACustomException(Exception):
    pass


sample_dict = {"a": 1}

print(sample_dict)
print(sample_dict['a'])

a = 1
b = 0

try:
    if b == 0:
        raise ThisIsACustomException
    c = a / b
except KeyError:
    print("we have encountered a KeyError")
except ZeroDivisionError:
    c = a / 1
except ThisIsACustomException:
    print('We have encountered our custom exception')
finally:
    print("We have reached the finally block")


print ('we have made to the end')
