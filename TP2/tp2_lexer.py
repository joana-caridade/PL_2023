import ply.lex as plex


class Tp2Lexer:
    tokens = ("ESCREVER", "VAR", "PARA", "FIM", "FAZER", "EM", "FUN","INVOCAR", "COMMENT", "num", "str", "var", "ENTRADA", "ALEATORIO")
    literals = [",", ";", "\"", "=", "+", "-", "*", "/", '(', ')', '[', ']', '.', '<', '>', '{', '}']
    t_ignore = " \n"

    def t_ESCREVER(self, t):
        r"((E|e)(S|s)(C|c)((R|r)(E|e)(V|v)(E|e)(R|r))?)\s"
        return t

    def t_COMMENT(self, t):
        r"(\/\*[^\*]*\*\/)|(\/\/[^(\r\n|\r|\n)]+)"
        pass

    def t_PARA(self, t):
        r"(PARA|para)\s"
        return t

    def t_FUN(self, t):
        r"(FUN|fun)\s"
        return t

    def t_FIM(self, t):
        r"(FIM|fim)\s"
        return t

    def t_EM(self, t):
        r"(EM|em)\s"
        return t

    def t_INVOCAR(self, t):
        r"(INV|inv)((k|K)|(ocar|OCAR))"
        return t
    def t_FAZER(self, t):
        r"(FAZER|fazer)\s"
        return t

    def t_VAR(self, t):
        r"((V|v)(A|a)(R|r))\s"
        return t

    def t_num(self, t):
        r"[0-9]+"
        t.value = int(t.value)
        return t

    def t_ALEATORIO(self, t):
        r"ALEATORIO|aleatorio"
        return t

    def t_ENTRADA(self, t):
        r"ENTRADA|entrada"
        return t

    def t_str(self, t):
        r"\"[^\"]+\""
        t.value = t.value.replace("\"", "")
        return t

    def t_var(self, t):
        r"([A-Za-z]|_)+[0-9]*([A-Za-z]|_)*"
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
