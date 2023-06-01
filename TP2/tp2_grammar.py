from tp2_lexer import Tp2Lexer
import ply.yacc as pyacc


class Tp2Grammar:
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', '(', ')'),
    )

    def __init__(self):
        self.yacc = None
        self.lexer = None
        self.tokens = None

    def build(self, **kwargs):
        self.lexer = Tp2Lexer()
        self.lexer.build(**kwargs)
        self.tokens = self.lexer.tokens
        self.yacc = pyacc.yacc(module=self, **kwargs)

    def parse(self, string):
        self.lexer.input(string)
        return self.yacc.parse(lexer=self.lexer.lexer)

    def p_codigo0(self, p):
        """ codigo : S ';' """
        p[0] = [p[1]]
        print(f"P0- {p[0]}")

    def p_codigo1(self, p):
        """ codigo : codigo S ';' """
        p[0] = p[1]
        p[0].append(p[2])

    def p_s(self, p):
        """ S : comando """
        p[0] = p[1]

    def p_comando0(self, p):
        """ comando : ESCREVER args """
        p[0] = {'op': 'esc', 'args': p[2]}
        print(p[0])

    def p_comando1(self, p):
        """ comando : VAR var_args"""
        p[0] = {'op': 'atr', 'args': p[2]}

    def p_comando2(self, p):
        """ comando : var '=' arg
                    | var_operacoes """
        if len(p) > 2:
            p[0] = {'op': 'atr', 'args': [(p[1], p[3])]}
        else:
            p[0] = p[1]

    def p_var_args(self, p):
        """ var_args : var '=' arg
                    | var_args ',' var '=' arg """
        if len(p) > 4:
            p[0] = p[1]
            p[0].append((p[3], p[5]))
        else:
            p[0] = [(p[1], p[3])]

    def p_lista_args(self, p):
        """ args : arg
                 | args ',' arg  """
        """
            arg:
                ESCREVER a;
                arg = d
            args , arg:
                ESCREVER a,b,c,d;
                args = a,b,c
                arg = d
        """
        if len(p) > 2:
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0] = [p[1]]

    def p_arg(self, p):
        """ arg : str
                | arith
                | variavel
                | funcao """
        if len(p) > 2:
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_funcao(self, p):
        """ funcao : ENTRADA '(' ')'
                    | ALEATORIO '(' arith ')' """
        if len(p) > 4:
            p[0] = {'op': 'aleatorio', 'args': [p[3]]}
        else:
            p[0] = {'op': 'ent', 'args': []}

    def p_arith(self, p):
        """ arith : number
                | '(' number ')' """
        if len(p) > 2:
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_variavel(self, p):
        """ variavel : var"""
        p[0] = {'var': p[1]}

    def p_var(self, p):
        """ arith : variavel
                | '(' variavel ')' """
        if len(p) > 2:
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_var_operacoes(self, p):
        """ var_operacoes : variavel '+' '=' arg
                | variavel '-' '=' arg
                | variavel '+' '+'
                | variavel '-' '-' """

        if len(p) > 4:
            p[0] = {'op': p[2] + p[3], 'args': [(p[1], p[4])]}
        else:
            p[0] = {'op': p[2] + p[3], 'args': [(p[1],)]}
        print(f"VAR: {p[0]}")

    def p_arith_list(self, p):
        """ number : arith '+' arith
                | arith '-' arith
                | arith '/' arith
                | arith '*' arith
                | arith arith """

        if len(p) > 3:
            p[0] = {'op': p[2], 'args': [p[1], p[3]]}
        elif len(p) == 3:
            p[0] = {'op': '*', 'args': [p[1], p[2]]}
        else:
            p[0] = [p[1]]

    def p_number(self, p):
        """ number : num """
        p[0] = p[1]

    def p_error(self, p):
        if p:
            raise Exception(f"Erro de sintax: inesperado {p.type} -> {p}")
        else:
            raise Exception("Erro de sintax: end of file inesperado")
