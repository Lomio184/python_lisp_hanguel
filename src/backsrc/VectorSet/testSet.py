pgm1 = """
        (DEFUN fact (n) (+ n 2 ( * 8 n 2 3 32)))\n(fact (10))\n(fact (2))\n(fact (3))\n
                         (+ 2 2 22 )\n(IF (> 4 2) ( + 2 2( * 2 4 )))\n
                         (DEFINE a 10)\n(DEFINE b 34)\n( + a 10 20 30 ( + 2 a ( * 4 4 )))\n
                         (+ b 2)\n\n\n( + 2 2 b )
                         \n\n( + 2 2 ( * 4 10 b ) )
                         \n
                         \n
                         (DEFINE c 20)\n
                         ( + c 20 ( * c 2 ))\n(MAIN)\n(DEFINE a -3.14)\n(+ a 1)\n(TYPE a)"""

pgm2 = '(DEFUN add (n m) ( * n m))\n(add ( add(4 2) add(2 4)))'
pgm3 = '(DEFUN rec(n) (IF (== n 1 ) (n) (+ (rec(- n 1) (n)))))\n(rec (10))'
pgm4 = "(DEFUN add (n m) ( * n m))\n(add ( add(4 2) add(2 4)))\n(DEFINE a  10 )\n(PRINT (+ a 2 3 4 ( * 2 2)))\n(PRINT (10))\n(PRINT (add (4 2 )))"
pgm5 = "(PRINT (\"hello world\"))\n(DEFUN add (n m) ( * n m))\n(PRINT (add (4 4)))\n(PRINT (add (add (4 2 ) add( 2 4 ))))"
pgm6 = """(DEFINE a 10 )\n( PRINT (CDR (*1 2 3 4 a)))\n(PRINT (\"hello world\"))\n
                         (PRINT (POW a a))\n(DEFINE b 2.56)\n
                         (PRINT (ROUND 3.56 ))\n(ROUND b)\n( + b 3)\n
                         (IF ( < 1 2 ) (+ 2 2) ( + 3 4))"""
pgm_first_stress_test1 = """(PRINT (\"hello world\"))\n(DEFUN add (n m) ( * n m))\n(PRINT (add (4 4)))\n
                         (PRINT (add (add (4 2 ) add( 2 4 ))))\n(+ 2 2 ( * 8 7 ( * 7 9 )))\n
                         (DEFINE x 20)\n(DEFUN tw (a) (* a 20 ))\n( tw (x))\n
                         (PRINT (tw (x)))\n(DEFUN aab (n) ( + n 2 ))\n(PRINT (aab(10)))\n
                         \n(PRINT (aab(10)))\n(PRINT (aab(10)))\n(PRINT (aab(10)))\n(PRINT (aab(10)))\n
                         \n(PRINT (aab(10)))\n(PRINT (aab(10)))\n(PRINT (aab(10)))\n(PRINT (aab(10)))\n
                         \n(PRINT (aab(10)))\n(PRINT (aab(10)))\n(PRINT (aab(10)))\n(PRINT (aab(10)))\n
                         (IF ( > 5 4 ) (PRINT(+ 2 2)) ( PRINT(\"안녕\")))"""
pgm_subroutine = """(LIST (rea) ( 2 3 4 5 6 7 8 9 10 ))\n
                         (DEFUN add (n) ( + n 1 ))\n
                         (PRINT (add(add(add(add(rea[1]))))))"""
pgm_recursive = "(DEFUN add (n) (IF (< n 2 ) (n) (+ n add(- n 1))))\n(PRINT \"fibo :\" (add (10)))"
pgm_recursive2 = """(DEFINE x 10)\n(PRINT \"(+ x 2) => result :\" (+ x 2 ))\n
                    (DEFUN fib (n) (IF (< n 2) (n) (+ n fib(- n 1))))\n
                    (PRINT \"fib(10) => result :\" ( fib (11) ))\n
                    (DEFUN fact (n) (IF (== n 1 ) (n) ( * n fact(- n 1 ))))\n(PRINT \"fact(5) => result :\" (fact (5)))"""
pgm_test3 = "\n(DEFUN add (n) (+ n 2))\n(DEFINE a add)\n( a(1.42))\n(PRINT (TYPE a) )"

def fib(n):
    if n < 2:
        return n
    return n + fib(n-1)

print(fib(10))