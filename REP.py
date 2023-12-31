import Lexing
import Environment
import copy
import os

# TODO

# none
# basic functions
# basic system functions
# test, test, test!
# possible fix cons, maybe?
# refactor?
# acctual working repl
# timing stuff?

def macro_expand():
    pass

def def_macro():
    pass

def rep(txt):
    repl = REP(txt)
    return repl.rep()


class REP:
    def __init__(self, txt):
        self.txt = txt
        lexer = Lexing.Tokenizer(txt)
        self.tokens = lexer.tokenize()
        self.current_token = self.tokens[0]
        self.token_index = 0
        self.tail_call = False

    def advance(self):
        if self.token_index + 1 < len(self.tokens):
            self.token_index += 1
            self.current_token = self.tokens[self.token_index]
            return True
        self.current_token = None
        return False

    def peek(self):
        if self.token_index + 1 < len(self.tokens):
            return self.tokens[self.token_index + 1]
        return None

    def is_macro(self, ast, env):
        special_forms = ("do", "if", "let", "set", "quote", "macro-expand", "quasi-quote",
         "splice-unquote", "fn", "print", "def-macro")
        return type(ast) is list and type(ast[0]) is str and ast[0] in env.macros

    def macro_expand(self, ast, env):
        while self.is_macro(ast, env):
            ast[0] = self.eval(ast[0], env)
            ast = ast[0](*ast[1:])
        return ast

    def handle_def_macro(self, ast, env):
        # set a function in the environment with (fn, True)
        # fn = FunctionType(params, ast[2])
        res = None
        def fn(*args):
            res = self.eval(ast[2], Environment.Environment(env))
            params = []
            if type(res) is tuple and len(res) == 2:
                # functions are weird because of tail recursion
                for param in res[0]:
                    params.append(param)
            return self.eval(res[1], Environment.Environment(env, params, [*args]))
        env.set(str(ast[1]), lambda *args: fn(*args))
        env.macros.append(str(ast[1]))
        return None

    def cons(self, a, b):
        if type(a) is list and type(b) is list:
            return a + b
        elif type(b) is list:
            return [a, *b[:]]
        elif b == None:
            return [a]
        else:
            # uh
            # undefined behavior is a feature
            return [a, ".", b]# [a, *b[:]]

    def print_sexpr(self, sexpr, inside_sexpr):
        if type(sexpr) is list:
            i = 0
            print("(", end="")
            for el in sexpr:
                self.print_sexpr(el, True)
                if i < len(sexpr)-1:
                    print(" ", end="")
                i += 1
            if inside_sexpr:
                print(")", end="")
            else:
                print(")")
        elif type(sexpr) is tuple:
            print("(fn (", end="")
            i = -1
            for i in range(0, len(sexpr[0])-1):
                param = sexpr[0][i]
                print(param + " ", end="")
            if len(sexpr[0]) > 0:
                print(sexpr[0][i], end="")
            print(") ", end="")
            self.print_sexpr(sexpr[1], True)
            print(")")
        else:
            if inside_sexpr:
                print(sexpr, end="")
            elif sexpr == "()" or sexpr == None:
                print("nil")
            else:
                print(sexpr)

    def rep(self):
        env = Environment.Environment()
        env.set('+', lambda a, b: a + b)
        env.set('-', lambda a, b: a - b)
        env.set('*', lambda a, b: a * b)
        env.set('/', lambda a, b: a / b)
        env.set('%', lambda a, b: a % b)

        env.set('=', lambda a, b: a == b)
        env.set('>', lambda a, b: a > b)
        env.set('<', lambda a, b: a < b)
        env.set('>=', lambda a, b: a >= b)
        env.set('<=', lambda a, b: a <= b)

        env.set('and', lambda a, b: a and b)
        env.set('or', lambda a, b: a or b)
        env.set('not', lambda a: not a)

        env.set('print', lambda a: (print(a), a)[1])
        env.set('car', lambda a: a[0])
        env.set('cdr', lambda a: a[1:])
        env.set('cons', lambda a, b: self.cons(a, b))
        env.set('list', lambda *a: [*a])

        env.set('nil?', lambda a: a==None)
        env.set('fn?', lambda a: env.contains(a) and type(env.get(a)) is tuple and len(env.get(a)) == 2)
        env.set('macro?', lambda a: a in env.macros)
        env.set('sym?', lambda a: not (env.find(a) == None))

        env.set("exec", lambda a: os.system(a))
        env.set("open", None)
        env.set("close", None)
        env.set("read", None)
        env.set("write", None)

        ast = []

        while self.current_token:
            ast.append(self.handle_sexpr())

        # ast = self.handle_sexpr()
        for el in ast:
            el = self.macro_expand(el, env)
            res = self.eval(el, env)

        # print(res)
        self.print_sexpr(res, False)
        return res

        # self.print_sexpr(self.eval(ast, env, 0))
        # while there are tokens to read

    def handle_sexpr(self):
        if self.current_token == '(':
            if self.peek() == ')':
                self.advance()
                self.advance()
                return None
            return self.handle_list()
        elif self.current_token in ("'", "`", "~", "~@"):
            return self.handle_special_quote()
        else:
            return self.handle_atom()

    def handle_special_quote(self):
        # 'true == (quote true)
        lst = []
        if self.current_token == "'":
            lst.append("quote")
        elif self.current_token == "`":
            lst.append("quasi-quote")
        elif self.current_token == "~":
            lst.append("unquote")
        elif self.current_token == "~@":
            lst.append("splice-unquote")
        self.advance()
        lst.append(self.handle_sexpr())
        return lst

    def handle_list(self):
        lst = []
        self.advance()
        while self.current_token and self.current_token != ')':
            lst.append(self.handle_sexpr())
        self.advance()
        return lst
        # return ListType(lst)

    def handle_atom(self):
        special_forms = ("do", "if", "let", "set", "quote", "macro-expand", "quasi-quote",
                         "splice-unquote", "fn", "print", "def-macro", "macro-expand")
        tok = self.current_token
        self.advance()

        if tok[0] in '0123456789':
            return int(tok)
        elif tok[0] =="\"":
            #modify this no "'str'" stuff
            return str(tok)
        elif tok == 'true':
            return True
        elif tok == 'false':
            return False
        # elif tok in special_forms:
        return tok
        # return SymbolType(tok)

    def handle_tail(self, tail_call, env):
        params = tail_call[0]
        expr = tail_call[1]
        args = tail_call[2]
        res = self.eval(expr, Environment.Environment(env, params, args))
        while type(res) is tuple and len(res) == 3:
            params = res[0]
            expr = res[1]
            args = res[2]
            res = self.eval(expr, Environment.Environment(env, params, args))
        assert (not (type(res) == tuple))
        return res

    @staticmethod
    def special_form(sexpr, form) -> bool:
        return type(sexpr) is list and sexpr[0] == form

    def handle_splice(self, lst, lst2, index, env):
        res = []
        for el in lst2:
            res.append(self.eval(el, env))
        lst[index] = lst[0:index-1] + [res] + lst[index+1:]

    def eval(self, sexpr, env):
        if type(sexpr) in (bool, int):
            return sexpr
        elif sexpr == None:
            return sexpr
        elif type(sexpr) is str:
            if len(sexpr) >= 1 and sexpr[0] == "\"":
                return sexpr
            else:
                return env.get(sexpr)
        else:
            # change this
            # change this
            # change this
            # change this
            ast = copy.deepcopy(sexpr)
            # why do lists suck so much
            # it is a list
            # elif it is do, let, set, fn, if, ', `, ,, quote, unquote, splice-unquote
            # else it is a list
            if self.special_form(sexpr, "if"):
                return self.handle_if(ast, env)
            elif self.special_form(sexpr, "do"):
                return self.handle_do(ast[1:], env)
            elif self.special_form(sexpr, "set"):
                return self.handle_set(ast, env)
            elif self.special_form(sexpr, "let"):
                return self.handle_let(ast, env)
            elif self.special_form(sexpr, "fn"):
                return self.handle_fn(ast, env)
            elif self.special_form(sexpr, "def-macro"):
                return self.handle_def_macro(ast, env)
            elif self.special_form(sexpr, "quote"):
                # ast should be length 2
                assert(len(ast) == 2)
                return ast[1]
            elif self.special_form(sexpr, "quasi-quote"):
                assert (len(ast) == 2)
                # 1.) (quasi-quote (unquote (+ 1 2))
                # 2.) (quasi-quote (+ 1 (unquote 2))
                # 3.) (quasi-quote (1 2 3 (splice-unquote (+ 2 2)) 5)
                if sexpr[1][0] == "unquote":
                    return self.eval(sexpr[1][1], env)
                i = 0
                res_ast = []
                while i < len(ast[1]):
                    res = ast[1][i]
                    if type(res) is list:
                        if res[0] == "unquote":
                            res = self.eval(res[1], env)
                        elif res[0] == "splice-unquote":
                            res = self.eval(res[1], env)
                    if type(res) is list:
                        for ele in res:
                            res_ast.append(ele)
                    else:
                        res_ast.append(res)
                    i += 1
                return res_ast
            else:
                for i in range(1, len(ast)):
                    ast[i] = self.eval(ast[i], env)
                # fn = env.get(ast[0])
                fn = self.eval(ast[0], env)
                if type(fn) is tuple:
                    if self.tail_call:
                        return fn[0], fn[1], ast[1:]
                    else:
                        expr = fn[1]
                        params = fn[0]
                        args = ast[1:]
                        while True:
                            self.tail_call = True
                            result = self.eval(expr, Environment.Environment(env, params, args))
                            if type(result) is tuple: #and len(result) == 3:
                                params = result[0]
                                expr = result[1]
                                args = result[2]
                            else:
                                self.tail_call = False
                                return result
                    # while
                    # return self.eval(fn[1], Environment.Environment(env, fn[0], ast[1:]), i)
                j = 1
                for thing in ast[1:]:
                    if type(thing) is tuple:
                        ast[j] = self.handle_tail(thing, env)
                    j += 1
                return fn(*ast[1:])

    def handle_if(self, ast, env):
        if self.eval(ast[1], env):
            res = self.eval(ast[2], env)
            return res
        else:
            return self.eval(ast[3], env)

    def handle_do(self, ast, env):
        for expr in ast:
            res = self.eval(expr, env)
        return res

    def handle_set(self, ast, env):
        res = self.eval(ast[2], env)
        env.set(ast[1], res)
        return res

    def handle_let(self, ast, env):
        new_env = Environment.Environment(env)
        for param in ast[1]:
            new_env.set(param[0], self.eval(param[1], env))
        return self.eval(ast[2], new_env)

    def handle_fn(self, ast, env):
        return ast[1], ast[2]
        params = []
        for param in ast[1]:
            params.append(param)
        # fn = FunctionType(params, ast[2])
        def fn(*args):
            res = self.eval(ast[2], Environment.Environment(env, params, *args))
            return res
        return lambda *args: fn(args)
        # return fn.evaluate(env, self, i)

    def handle_print(self, ast, env):
        print(val := self.eval(ast[1], env))
        return val
