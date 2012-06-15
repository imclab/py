functions = {
    'square' :  lambda x: x * x,
    'cube' :    lambda x: x * x * x,
    'poly' :    lambda x: (2*x) ** 2 + 4*x + 4
}

args = dict(num=2, id=4)

def try_it():
    # print functions['square'](5)
    # print functions['cube']  (5)
    # print functions['poly']  (5)
    play(args)

def play(num, id=0):
    print num * id


if __name__ == "__main__":
    try_it()