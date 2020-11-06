from lang_types import Types
from distlib.compat import raw_input
from parse import tokenizer, tokenize
from env import std, Env

global_env = std()


def parser(expression: str):
    return tokenizer(tokenize(expression))


def schemize(exp):
    if isinstance(exp, Types.List):
        return '(' + ' '.join(map(schemize, exp)) + ')'
    else:
        return str(exp)


class Procedure(object):

    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))


def eval(token, env=None):
    if env is None:
        env = global_env
    if isinstance(token, Types.Symbol):
        return env.find(token)[token]
    if not isinstance(token, Types.List):
        return token
    if token[0] == 'quote':
        (_, exp) = token
        return exp
    if token[0] == 'if':
        (_, test, conseq, alt) = token
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    if token[0] == 'define':
        (_, var, exp) = token
        env[var] = eval(exp, env)
    if token[0] == 'set!':
        (_, var, exp) = token
        env.find(var)[var] = eval(exp, env)
    if token[0] == 'lambda':
        (_, parms, body) = token
        return Procedure(parms, body, env)
    else:
        proc = eval(token[0], env)
        args = [eval(exp, env) for exp in token[1:]]
        return proc(*args)


def repl(prompt='tls.py> '):
    while True:
        val = eval(parser(raw_input(prompt)))
        if val is not None:
            print(schemize(val))


repl()
