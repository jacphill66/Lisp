import Lexing
import REP
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # rep = REP.REP("(if false (+ 1 (+ 1 (- 1 2)) ) (* 2 4))")
    # rep = REP.REP("(do (+ 1 2))")
    # rep = REP.REP("(do (set apples 2) (+ 1 apples) )")

    # rep = REP.REP("(let ((a 1) (b 10)) (+ a b))")
    # rep = REP.REP("(do (set sum (fn (a b) (+ a b))) (sum 1 2))")
    # rep = REP.REP("(do (set fact (fn (a b) (if (> a 1) (fact (- a 1) (* a b))  b))) (fact 2 1))")
    # rep = REP.REP("(do (set count (fn (a) (if (> a 1) (+ 1 (count (- a 1))) 1))) (count 150))")
    # rep = REP.REP("(do (set fib (fn (n) (if (> n 2) (+ (fib (- n 1)) (fib (- n 2))) 1))) (fib 10))")
    # rep = REP.REP("(print 1)")
    # rep = REP.REP("(do (set count (fn (a) (if (< a 1000000) (do (print a) (count (+ 1 a) )) a) ) ) (count 1))")
    # rep = REP.REP("(list 1 2 3 4 5 4 3 2 (car (cdr (list (list (list 1 2 3 4)) 1 ))))")
    # rep = REP.REP("(list (quote if) (quote 1) (quote 2))")
    # rep = REP.REP("(do (set lst (quote (1 2 3 4 5))) (quasi-quote (1 2 3 (splice-unquote lst)  4 5)))")
    # rep.rep()
    # rep.print_sexpr("'(+ 1 2 (+ 1 2) )")
    # print(REP.rep("( (fn (a b) (+ a b)) 3 4)"))
    # print(REP.rep("(let ((a 1) (b 2) (c 3) (d 4) (e 5)) e)"))
    # print(REP.rep("(quasi-quote (1 2 3 4)"))
    # print(REP.rep("(quote (quasi-quote (1 2 3 4))"))
    # print(REP.rep("(quasi-quote (unquote ((fn (x) (print x)) 2)))"))
    # REP.rep("(quasi-quote (1 2 3 4 5 (splice-unquote (list 6 7 8 (quasi-quote (9 10 11 12 (splice-unquote (list 13 14 15 16)))))) 17 (splice-unquote (list 18 19 20 21)) 22)")
    # [1, 2, 3, 4, 5, 6, 7, 8, [9, 10, 11, 12, 13, 14, 15, 16], 17, 18, 19, 20, 21, 22]
    # REP.rep("(quasi-quote (1 2 3 4 5 (splice-unquote (list 6 7 8))")
    # REP.rep("'(let ((a 1)) (+ a 1)) `(if ~false ~1 ~2)")
    # REP.rep("")
    # REP.rep("(cons 1 (cons 1 2))")
    # REP.rep("(cons (cons 1 2) 1)")
    # print_hi('PyCharm')
    # REP.rep("'(1 . 2)")
    # REP.rep("(do (set fib (fn (n) (if (> n 2) (+ (fib (- n 1)) (fib (- n 2))) 1))) (fib 10))")
    # REP.rep("(quasi-quote (1 2 3 4 5 (splice-unquote (list 6 7 8 (quasi-quote (9 10 11 12 (splice-unquote (list 13 14 15 16)))))) 17 (splice-unquote (list 18 19 20 21)) 22)")
    # REP.rep("(do (set fib (fn (n) (if (> n 2) (+ (fib (- n 1)) (fib (- n 2))) 1))) (fib 10))")
    # REP.rep("(def-macro unless2 (fn (pred a b) (list 'if (list 'not pred) a b))) (unless2 false 7 8)")
    # REP.rep("(def-macro unless (fn (pred a b) `(if ~pred ~b ~a))) (unless false 7 8)")
    # REP.rep("(def-macro one (fn () 1)) (+ 1 (one))")
    # REP.rep("(def-macro identity (fn (x) x)) (identity (quote (1 2 3 4))")
    # REP.rep("((fn (x) x) '(1 2 3 4))")
    # REP.rep("(+ 1 2)")
    # REP.rep("(print \"apples\")")
    # REP.rep("(+ 1 2)")
    # REP.rep("(cons (cons (car (cdr '(1 2 3))) 1) '(1 2 3 4))")
    # REP.rep("(cons '(1  2) ())")
    # REP.rep("(nil? ())")
    REP.rep("(set fib (fn (n) (if (> n 2) (+ (fib (- n 1)) (fib (- n 2))) 1))) (print (fn? 'fib))")
    REP.rep("\"apples\"")
    REP.rep("(exec \"cd\"")
    # REP.rep("(fn? 'fib)")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
