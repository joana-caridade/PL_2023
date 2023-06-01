import sys

from tp2_grammar import Tp2Grammar
from tp2_eval import TP2Eval
from pprint import PrettyPrinter

pp = PrettyPrinter(sort_dicts=False)


lg = Tp2Grammar()
lg.build()

with open("entrada.ea", "r", encoding="utf8") as f:
    comandos = f.read()
    try:
        ast_tree=lg.parse(comandos)
        pp.pprint(ast_tree)
        TP2Eval.evaluate(ast_tree)
    except Exception as e:
        print(e, file=sys.stderr)
