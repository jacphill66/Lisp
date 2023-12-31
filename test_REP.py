import REP
# at least (or for starters) five tests per test case


def test_built_in_functions():
    # List function
    assert REP.rep("(list 1 2 3 4)") == [1, 2, 3, 4]

    assert REP.rep("(list 1 2 3 (list 4 5 (list 6 7 8 9)))") == [1, 2, 3, [4, 5, [6, 7, 8, 9]]]

    # print function
    assert REP.rep("(print 1)") == 1

    # Arithmetic
    assert REP.rep("(+ (+ (+ 123 4) ( + 1 2)) (+ 2 (+ 3 4)))") == 139
    assert REP.rep("(- (- (- 1234 234) (- 1000 653)) 2)") == 651
    assert REP.rep("(* (* 120 30) (* 1 (* 34 23)))") == 2815200
    assert REP.rep("(/ (/ 10 2) (/ 9 (/ 9 3) ) )") == 1.6666666666666667
    assert REP.rep("(% (% 10 2) (% 13 (% 4 10)))") == 0

    # Boolean Logic
    assert REP.rep('(not (not (not true)))') == False
    assert REP.rep('(and (and true true) (and false false))') == False
    assert REP.rep('(or (or true false) (or true (or false false)))') == True

    # Comparison
    assert REP.rep('(< 2 3)') == True
    assert REP.rep('(> 2 3)') == False
    assert REP.rep('(= (= 12 12) (= 1 1))') == True


def test_do():
    # Basic Do
    assert REP.rep("(do 1 2 3 4)") == 4

    # Basic Do 2
    assert REP.rep("(do 1 2 3 (do 1 2 3 4 5))") == 5

    # Do fn
    assert REP.rep("(do (fn (a) (not a)) true)") == True

    # Nested Dos
    assert REP.rep("(do 1 (do 2 (do 3 (do 4 (do 5)))))") == 5


def test_fn():
    # Basic Fn
    assert REP.rep('((fn (a b) (+ a b)) 2 3)') == 5

    # Nested Fns
    assert REP.rep('((fn (a b) (+ a b)) 2 ((fn (a b) (+ a b)) 2 ((fn (a b) (+ a b)) 2 ((fn (a b) (+ a b)) 2 3))))') == 11

    # Lots of parameters
    assert REP.rep('((fn (a b c d e) (+ a (+ b (+ c (+ d e))))) 1 2 3 4 5)') == 15

    # Test recursion
    assert REP.rep('(do (set fib (fn (n) (if (> n 2) (+ (fib (- n 1)) (fib (- n 2))) 1))) (fib 10))') == 55

    # Test simpler recursion
    assert REP.rep("(do (set fact (fn (n) (if (> n 1)  (* n (fact (- n 1)))1))) (fact 10))") == 3628800

    # Test Big Recursion
    assert REP.rep("(do (set fib (fn (n) (if (> n 2) (+ (fib (- n 1)) (fib (- n 2))) 1))) (fib 25))") == 75025

    # Test boring recursion
    assert REP.rep("(do (set its_the_final_count_down (fn (n) (if (> n 0) (+ (its_the_final_count_down (- n 1)) 1) n) ) ) (its_the_final_count_down 50))") == 50

    # Test big but not too big recursion
    assert REP.rep("(do (set fib (fn (n) (if (> n 2) (+ (fib (- n 1)) (fib (- n 2))) 1))) (fib 20))") == 6765

    # Test Tail Recursion 1:(
    assert REP.rep("(do (set count (fn (a) (if (< a 10000) (do (print a) (count (+ 1 a) )) a) ) ) (count 1))") == 10000

    # Test Tail Recursion 2:
    assert REP.rep("(do (set fact (fn (a b) (if (> a 1) (fact (- a 1) (* a b))  b))) (fact 500 1))") == 1220136825991110068701238785423046926253574342803192842192413588385845373153881997605496447502203281863013616477148203584163378722078177200480785205159329285477907571939330603772960859086270429174547882424912726344305670173270769461062802310452644218878789465754777149863494367781037644274033827365397471386477878495438489595537537990423241061271326984327745715546309977202781014561081188373709531016356324432987029563896628911658974769572087926928871281780070265174507768410719624390394322536422605234945850129918571501248706961568141625359056693423813008856249246891564126775654481886506593847951775360894005745238940335798476363944905313062323749066445048824665075946735862074637925184200459369692981022263971952597190945217823331756934581508552332820762820023402626907898342451712006207714640979456116127629145951237229913340169552363850942885592018727433795173014586357570828355780158735432768888680120399882384702151467605445407663535984174430480128938313896881639487469658817504506926365338175055478128640000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def test_let():
    # Basic Let
    assert REP.rep("(let ((a 1) (b 2)) (+ a b))") == 3

    # Basic Let
    assert REP.rep("(let ((a 1) (b 2)) (+ a b))") == 3

    # Nested Let Parameter
    assert REP.rep("(let ( (a (let ((a 1)) (+ a 1))) ) a)") == 2

    # Lots of parameters
    assert REP.rep("(let ((a 1) (b 2) (c 3) (d 4) (e 5)) (do (print (+ a b)) (print (+ c d)) (print e) ))") == 5

    # Nested Let
    assert REP.rep("(let ((a 2) (b 1)) (+ a (let ((a 10) (b 20)) (+ a b) )) )") == 32


def test_set():
    # Basic Set
    assert REP.rep("(set a 10)\n (print a)") == 10

    # Basic Set 2
    assert REP.rep("(set a 100)") == 100

    # Basic Fn
    assert REP.rep("((set a (fn (a b) (+ a b))) 10 10)") == 20


def test_if():
    # Basic If
    assert REP.rep("(if true 1 2)") == 1

    # Nested If
    assert REP.rep("(if (if false false true) 1 2)") == 1


def test_quote():
    # Basic Quote
    assert REP.rep("(quote (1 2 3 4 5))") == [1, 2, 3, 4, 5]

    # Quote With Unquote
    assert REP.rep("(quote (unquote (1 2 3 4 5)))") == ['unquote', [1, 2, 3, 4, 5]]

    # Nested Quote 1
    assert REP.rep("(do (print (+ 1 2)) (quote (1 2 3 4)))") == [1, 2, 3, 4]


def test_quasiquote():
    # Basic Quasiquote
    assert REP.rep("(quasi-quote (1 2 3 4)") == [1, 2, 3, 4]

    # Quoted Quasiquote
    assert REP.rep("(quote (quasi-quote (1 2 3 4))") == ['quasi-quote', [1, 2, 3, 4]]

    # Basic Quasiquote With Unquote
    assert REP.rep("(quasi-quote (unquote (list 1 2 3 4)))") == [1, 2, 3, 4]

    # More advanced Quasiquote With Unquote
    assert REP.rep("(quasi-quote (unquote ((fn (x) (print x)) 2)))") == 2

    # Quasiquote with Spliceunquote
    assert REP.rep("(quasi-quote (1 2 3 4 5 (splice-unquote (list 6 7 8 9 10)) 11 12 13 14 15))") == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    # Quasiquote with Spliceunquote
    assert REP.rep("(quasi-quote (1 2 3 4 5 (splice-unquote (list 6 7 8 (quasi-quote (9 10 11 12 (splice-unquote (list 13 14 15 16)))))) 17 (splice-unquote (list 18 19 20 21)) 22)") == [1, 2, 3, 4, 5, 6, 7, 8, [9, 10, 11, 12, 13, 14, 15, 16], 17, 18, 19, 20, 21, 22]

    # add special syntax
    assert (REP.rep("'1")) == 1

    assert (REP.rep("'(1 2 3 4)")) == [1, 2, 3, 4]

    assert (REP.rep("''''1")) == ['quote', ['quote', ['quote', 1]]]

    assert (REP.rep("`~(+ 1 2)")) == 3

    assert REP.rep("`(1 2 3 ~(+ 1 3))") == [1, 2, 3, 4]


def test_macros():
    assert REP.rep("(def-macro unless2 (fn (pred a b) (list 'if (list 'not pred) a b))) (unless2 false 7 8)") == 7
    assert REP.rep("(def-macro unless (fn (pred a b) `(if ~pred ~b ~a))) (unless false 7 8)") == 7
    assert REP.rep("(def-macro one (fn () 1)) (+ 1 (one))") == 2
    assert REP.rep("(def-macro identity (fn (x) x)) (identity (quote (1 2 3 4))") == [1, 2, 3, 4]
