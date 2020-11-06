from lang_types import Types


def tokenize(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').split()


def _atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Types.Symbol(token)


def tokenizer(tokens):
    if not tokens:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        tokens_list = list()
        while tokens[0] != ')':
            tokens_list.append(tokenizer(tokens))
        tokens.pop(0)
        return tokens_list
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return _atom(token)
