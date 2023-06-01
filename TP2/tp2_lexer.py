import ply.lex as plex


class Tp2Lexer:
    tokens = ("ESCREVER", "num", "str", "var")
    literals = [",", ";", "\"", "=", "+", "-", "*", "/"]
    t_ignore = " \n"

    def t_ESCREVER(self, t):
        r"(E|e)(S|s)(C|c)((R|r)(E|e)(V|v)(E|e)(R|r))?"
        print(t.value)
        return t

    def t_num(self, t):
        r"[0-9]+"
        t.value = int(t.value)
        return t

    def t_str(self, t):
        r"\"[^\"]+\""
        t.value = t.value.replace("\"", "")
        return t

    def t_var(self, t):
        r"[A-Za-z]+"
        return t
    def __init__(self):
        self.lexer = None

    def build(self, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)

    def input(self, string):
        self.lexer.input(string)

    def token(self):
        token = self.lexer.token()
        return token if token is None else token.type

    def t_error(self, t):
        print(f"Token inesperado: {t.value[:10]}")
        exit(1)
