import random


class TP2Eval:
    symbols = {}
    functions = {}
    comands = {
        "+": lambda args: args[0] + args[1],
        "-": lambda args: args[0] - args[1],
        "*": lambda args: args[0] * args[1],
        "/": lambda args: args[0] / args[1],
        "+=": lambda args: TP2Eval._comp_attrib(args[0], '+='),
        "-=": lambda args: TP2Eval._comp_attrib(args[0], '-='),
        "--": lambda args: TP2Eval._var_counter(args[0], '--'),
        "++": lambda args: TP2Eval._var_counter(args[0], '++'),
        "esc": lambda args: TP2Eval._escrever(args),
        "atr": lambda args: TP2Eval._attrib(args),
        "ent": lambda args: input('>>'),
        "aleatorio": lambda args: random.randrange(args[0]),
        "invk": lambda args: TP2Eval._invocar(args)
    }

    @staticmethod
    def _invocar(args):
        nome_func, func_args=args
        if nome_func in TP2Eval.functions:
            func = TP2Eval.functions[nome_func]
            if len(func['args']) != len(func_args):
                raise Exception(f"Argumentos insuficientes para a função {nome_func} foram dados {len(func_args)} necessários {len(func['args'])}")
            else:
                # definir as variaveis da função
                for i in range(0, len(func['args'])):
                    TP2Eval.symbols[func['args'][i]] = func_args[i]

                # execução do codigo da função
                TP2Eval.evaluate(func['codigo'])

                # apagar as variaveis da função
                for nome_arg in func['args']:
                    TP2Eval.symbols.pop(nome_arg)

        else:
            raise Exception("Função inexistente")

    @staticmethod
    def _escrever(args):
        for arg in args:
            print(arg, end="")
        print()

    @staticmethod
    def _var_counter(args, counter):
        var = args[0]
        var_nome = var['var']
        var_val = TP2Eval.evaluate(var)
        novo_valor = var_val + 1 if counter in '++' else var_val - 1
        TP2Eval.symbols[var_nome] = novo_valor

    @staticmethod
    def _comp_attrib(args, attrib):

        var, val = args
        var_nome = var['var']
        valor = TP2Eval.evaluate(val)
        var_valor = TP2Eval.evaluate(var)
        novo_valor = var_valor + valor if attrib in '+=' else var_valor - valor
        TP2Eval.symbols[var_nome] = novo_valor

        return None

    @staticmethod
    def _attrib(args):
        for arg in args:
            name, value = arg
            TP2Eval.symbols[name] = TP2Eval.evaluate(value)

        return None

    @staticmethod
    def evaluate(ast):
        if type(ast) is dict:
            return TP2Eval._eval_operator(ast)
        if type(ast) is list:
            answer = []
            for a in ast:
                answer.append(TP2Eval.evaluate(a))
            return answer
        if type(ast) is tuple:
            return ast
        if type(ast) is int:
            return ast
        if type(ast) is str:
            return ast

        raise Exception("Tipo da ast desconhecido")

    @staticmethod
    def _eval_operator(ast):
        if 'op' in ast:
            op = ast['op']
            args = [TP2Eval.evaluate(arg) for arg in ast['args']]
            if op in TP2Eval.comands:
                func = TP2Eval.comands[op]
                return func(args)
            else:
                raise Exception(f"Operador desconhecido: {op}")

        if 'var' in ast:
            nome_var = ast['var']
            if nome_var in TP2Eval.symbols:
                val = TP2Eval.symbols[nome_var]
                return val
            else:
                raise Exception(f"Variavel desconhecida: {nome_var}")

        if 'ciclo' in ast:
            intervalo = ast['interval']
            nome_counter = ast['counter']
            TP2Eval.symbols[nome_counter] = intervalo[0]

            codigo = ast['codigo']
            increment = ast['increment']
            for TP2Eval.symbols[nome_counter] in range(intervalo[0], intervalo[1] + 1, increment):
                TP2Eval.evaluate(codigo)
            return None

        if 'func' in ast:
            nome = ast['func']
            args = ast['args']
            codigo = ast['codigo']
            TP2Eval.functions[nome] = {'args': args, 'codigo': codigo}
            return None

        raise Exception("Ast desconhecida")
