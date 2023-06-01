class TP2Eval:
    symbols={}
    comands = {
        "+": lambda args: args[0] + args[1],
        "-": lambda args: args[0] - args[1],
        "*": lambda args: args[0] * args[1],
        "/": lambda args: args[0] / args[1],
        "esc": lambda args: print(args[0])
    }

    @staticmethod
    def evaluate(ast):
        if type(ast) is dict:
            return TP2Eval._eval_operator(ast)
        if type(ast) is list:
            answer = ''
            for a in ast:
                answer += str(TP2Eval.evaluate(a))
            return answer
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
        raise Exception("Ast desconhecida")