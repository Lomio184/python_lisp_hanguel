from src.backsrc.coreSrc.core.envFunction import cleanLocalEnv
from src.backsrc.coreSrc.parseComp import Compiler, localEnvi, nodeVal
from src.backsrc.object.type import AtomType_Token

class MakeOut:
    def __init__(self, exec_stack_area):
        self.exec_stack_area = exec_stack_area
        self.result = []
        self.compiler = Compiler()

    def out(self):
        for exev in self.exec_stack_area:
            if len(exev.tokens) is 0:
                return
            exev.tokens.append(AtomType_Token('EOF', 'EOF'))
            self.compiler.__init__(exev.tokens)
            node_result = self.compiler.scope_eval1()
            cleanLocalEnv(localEnvi, nodeVal)
            if node_result is None:
                pass
            else:
                self.result.append(node_result)

    def result_out(self):
        return self.result[0]

