
class ADT:
    pass

class Any:
    pass

class Number(Any):
    pass

class _Int(Number):
    pass

class _Symbol(ADT):
    pass

class _Real(Number):
    pass

class _Cons:
    pass

class _Var:
    pass

class _LetVar:
    pass

class _Function:
    pass

class _Compiler:
    def errorRas(self, errMsg):
        pass

class _List:
    pass


class Memory:
    pass

class Root_Atom:
    pass

class Atom(Root_Atom):
    pass

class Atom_Builtin_Function(Atom):
    pass

class _StandardOut:
    pass

class _CompStandardOut(_StandardOut):
    pass

class _InterPreterStandardOut(_StandardOut):
    pass
