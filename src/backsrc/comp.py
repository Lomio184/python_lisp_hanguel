import time
from multiprocessing import *
from src.backsrc.coreSrc.lex import Lexical_Stack
from src.backsrc.coreSrc.makeOut import MakeOut
# import psutil
import sys
from termcolor import colored
import colorama

colorama.init(autoreset=True)


def mainToken():
    print("Is this debug mode?(0=yes, 1=no)")
    # mode = int(input())
    mode = 0
    if mode == 0:
        print(colored("--Scheme Debug Mode--", 'yellow', 'on_red'))
    elif mode == 1:
        print(colored("--Scheme Publishing Mode--", 'yellow', 'on_blue'))
        sys.tracebacklimit = 0
    start = time.time()
    test = Lexical_Stack("(let ((i 1))"
                         "  ( let ((j (+ i 2 )))"
                         "      ( - i j)))"
                         ""
                         "(let (( i 2 )"
                         "  ( j ( * i 2 )))"
                         "      ( + i j ))"
                         ""
                         "(define x (+ 1 2 ))"
                         "( + x 3 )"
                         "(define y ( let ((i 1)) ( + i 4 )))"
                         "( + x y )"
                         ""
                         "( define z (let ((i 1 ))"
                         "  (set! i ( + i 3 )) i))"
                         ""
                         "( + 2 3 )"
                         ""
                         "( print \"hello\" \" \" ( + y 2 ))"
                         ""
                         "(+ z 2 )"
                         ""
                         "( + z x y )"
                         ""
                         "(define tree '( 1 2 ))"
                         ""
                         "( print tree \" \" z \"=( + z z z z )\" (+ z z z z z ))"
                         ""
                         "( map + tree tree tree )"
                         "(map ( lambda (x) ( * x x ) ) '( 1 2 3 ))")
    test.tokenize()
    make = MakeOut(test.stack)
    make.out()
    rea = make.result
    for _ in range(len(rea)):
        print(rea[_])
    print("Execute Time : ", time.time() - start)
    # print('cpu times : ', psutil.cpu_times_percent(interval=None, percpu=False))
    # print('cpu core  : ', psutil.cpu_count(True)
    # print('vtl mem   : ', psutil.virtual_memory())
    # prc = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if 'python' in p.info['name']]
    # print('act pcs   :', prc)

#
if __name__ == '__main__':
    mainToken()
    # with Pool(processes=4) as pool:
    #     pool.apply(mainToken)
    #     pool.close()