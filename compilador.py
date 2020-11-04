import sys

argv = sys.argv[1:] #lista dos argumentos recebidos ao rodar o arquivo
class PrePro:
    def filter(entrada):
        parenteses = 0
        numero = ""
        numero2 = ""
        saida = []
        comment = False
        string = False
        skip = False
        for i in range(len(entrada)):
            char = entrada[i]
            if skip == True:
                skip = False
                continue
            if char == "=" and entrada[i+1] == "#":
                if comment:
                    comment = False #fim do comentario
                    skip = True
                    if not numero == "":
                        saida.append(numero)
                        numero = ""
                    continue
                elif string:
                    pass
                else:
                    raise Exception("Erro de gramática")

            if string and (not char == '"'):
                numero += char
                continue

            if char == "#" and entrada[i+1] == "=": #começo do comentario
                comment = True
                continue
            
            if char == '"':
                if not string:
                    string = True
                    numero += char
                    continue
                else:
                    string = False
                    saida.append(numero)
                    numero = ""
                    continue

            if char == "(":
                parenteses += 1
            if char == ")":
                if parenteses == 0:
                    raise Exception("Erro de gramática")
                parenteses -= 1

            if char == " ":
                if not numero == "":
                    saida.append(numero)
                    numero = ""
                continue
            elif char.isnumeric() or char.isalpha() or char == "_":
                numero += char    
            else:
                if not numero == "":
                    saida.append(numero)
                numero = ""
                if char == "&" or char == "|" or char == "=" or char == ":":
                    numero2 += char
                    if entrada[i+1] == "&" or entrada[i+1] == "|" or entrada[i+1] == "=" or entrada[i+1] == ":":
                        continue
                    saida.append(numero2)
                    numero2 = ""
                else:
                    saida.append(char)

                
        if not numero == "":
            saida.append(numero)
        if comment == True or (not parenteses == 0):
            raise Exception("Erro de gramática")
        return saida

class Token:
    def __init__(self,tipo,valor):
        self.tipo = tipo     #string
        self.valor = valor   #int

class Tokenizer:
    pos = 0                 #inteiro que marca o próximo token
    atual = Token("0",0)    #token

    def __init__(self,origem):
        self.origem = origem #lista de origem
    
    def selProx(self):
        if len(self.origem) == (self.pos):
            prox = Token("EOF",0)
            self.atual = prox
            return

        lido = self.origem[self.pos]

        if lido.isnumeric():
            prox = Token("INT",int(lido))
            self.atual = prox
            self.pos += 1
            return
        elif lido == "+":
            prox = Token("PLUS","+")
            self.atual = prox
            self.pos += 1
            return
        elif lido == "-":
            prox = Token("MINUS","-")
            self.atual = prox
            self.pos += 1
            return
        elif lido == "*":
            prox = Token("MULT","*")
            self.atual = prox
            self.pos += 1
            return
        elif lido == "/":
            prox = Token("DIV","/")
            self.atual = prox
            self.pos += 1
            return
        elif lido == "(":
            prox = Token("OPEN","(")
            self.atual = prox
            self.pos += 1
            return
        elif lido == ")":
            prox = Token("CLOSE",")")
            self.atual = prox
            self.pos += 1
            return
        elif lido == "=":
            prox = Token("EQUAL","=")
            self.atual = prox
            self.pos +=1
        elif lido == "println":
            prox = Token("PRINT",lido)
            self.atual = prox
            self.pos +=1
        elif lido == "readline":
            prox = Token("READ",lido)
            self.atual = prox
            self.pos +=1
        elif lido == "while":
            prox = Token("WHILE",lido)
            self.atual = prox
            self.pos +=1
        elif lido == "if":
            prox = Token("IF",lido)
            self.atual = prox
            self.pos +=1
        elif lido == "elseif":
            prox = Token("ELSEIF",lido)
            self.atual = prox
            self.pos +=1
        elif lido == "else":
            prox = Token("ELSE",lido)
            self.atual = prox
            self.pos +=1
        elif lido == "end":
            prox = Token("END",lido)
            self.atual = prox
            self.pos +=1
        elif lido == "local":
            prox = Token("LOCAL",lido)
            self.atual = prox
            self.pos +=1
        elif lido == "Int":
            prox = Token("INTVAR",lido)
            self.atual = prox
            self.pos += 1
        elif lido == "Bool":
            prox = Token("BOOLVAR",lido)
            self.atual = prox
            self.pos += 1
        elif lido == "String":
            prox = Token("STRINGVAR",lido)
            self.atual = prox
            self.pos += 1
        elif lido == "true":
            prox = Token("TRUE",lido)
            self.atual = prox
            self.pos += 1
        elif lido == "false":
            prox = Token("FALSE",lido)
            self.atual = prox
            self.pos += 1
        elif lido[0].isalpha():
            for i in lido:
                if i.isnumeric() or i.isalpha() or i == "_":
                    continue
                else:
                    raise Exception("Erro de gramática")
            prox = Token("IDEN",lido)
            self.atual = prox
            self.pos += 1

        elif lido[0] == '"':
            lido = lido.replace('"','')
            prox = Token("STR",lido)
            self.atual = prox
            self.pos +=1
        elif lido == "\n":
            prox = Token("ENTER",lido)
            self.atual = prox
            self.pos += 1
        elif lido == "&&":
            prox = Token("AND",lido)
            self.atual = prox
            self.pos += 1
        elif lido == "||":
            prox = Token("OR",lido)
            self.atual = prox
            self.pos += 1
        elif lido == "::":
            prox = Token("EQUALVAR",lido)
            self.atual = prox
            self.pos += 1
        elif lido == "!":
            prox = Token("NOT",lido)
            self.atual = prox
            self.pos += 1
        elif lido == "==":
            prox = Token("COMPARE",lido)
            self.atual = prox
            self.pos += 1
        elif lido == ">":
            prox = Token("BIGGER",lido)
            self.atual = prox
            self.pos += 1
        elif lido == "<":
            prox = Token("SMALLER",lido)
            self.atual = prox
            self.pos += 1
        else:
            raise Exception("Erro de gramática")

class Parser:
    st = {}

    def loopif():
        Parser.tokenizer.selProx()
        condition = Parser.parseRelExp()
        block = Parser.parseBlock()
        block2 = NoOp(0,0)
        if Parser.tokenizer.atual.tipo == "ELSEIF":
            block2 = Parser.loopif()
        if Parser.tokenizer.atual.tipo == "ELSE":
            Parser.tokenizer.selProx()
            block2 = Parser.parseBlock()
        result = IfOp("if",[condition,block,block2])
        return result

    def parseBlock():
        filhos = []
        while not Parser.tokenizer.atual.tipo in ["EOF","END","ELSE","ELSEIF"]:
            filhos.append(Parser.parseCommand())
            Parser.tokenizer.selProx()
        return Statements(0,filhos)
    def parseCommand():
        result = ""
        if Parser.tokenizer.atual.tipo == "IDEN":
            identifier = Parser.tokenizer.atual.valor
            Parser.tokenizer.selProx()
            if Parser.tokenizer.atual.tipo == "EQUAL":
                Parser.tokenizer.selProx()
                if Parser.tokenizer.atual.tipo == "READ":
                    Parser.tokenizer.selProx()
                    if Parser.tokenizer.atual.tipo == "OPEN":
                        Parser.tokenizer.selProx()
                    if Parser.tokenizer.atual.tipo == "CLOSE":
                        readline = NoOp("readline",[])
                        result = BinOp("=",[identifier,readline])
                        Parser.tokenizer.selProx()
                else:
                    result = BinOp("=",[identifier,Parser.parseRelExp()])
            else:
                raise Exception("Erro de sintaxe")

        elif Parser.tokenizer.atual.tipo == "PRINT":
            Parser.tokenizer.selProx()
            if not Parser.tokenizer.atual.tipo == "OPEN":
                raise Exception("Erro de sintaxe")
            else:
                Parser.tokenizer.selProx()
            
            valor = Parser.parseRelExp()
            result = UnOp("println",[valor])
            Parser.tokenizer.selProx()
            if Parser.tokenizer.atual.tipo == "CLOSE":
                Parser.tokenizer.selProx()
        
        elif Parser.tokenizer.atual.tipo == "WHILE":
            Parser.tokenizer.selProx()
            condition = Parser.parseRelExp()
            block = Parser.parseBlock()
            result = BinOp("while",[condition,block])
            if not Parser.tokenizer.atual.tipo == "END":
                raise Exception("Erro de sintaxe")
            Parser.tokenizer.selProx()

        elif Parser.tokenizer.atual.tipo == "IF":
            result = Parser.loopif()
            if not Parser.tokenizer.atual.tipo == "END":
                raise Exception("Erro de sintaxe")
            Parser.tokenizer.selProx()

        elif Parser.tokenizer.atual.tipo == "LOCAL":
            Parser.tokenizer.selProx()
            if Parser.tokenizer.atual.tipo == "IDEN":
                identifier = Parser.tokenizer.atual.valor
                Parser.tokenizer.selProx()
                if Parser.tokenizer.atual.tipo == "EQUALVAR":
                    Parser.tokenizer.selProx()
                    if Parser.tokenizer.atual.tipo in ["INTVAR","BOOLVAR","STRINGVAR"]:
                        valor = Parser.tokenizer.atual.valor
                        result = BinOp("::",[identifier,valor])
                        Parser.tokenizer.selProx()

        if Parser.tokenizer.atual.tipo in ["ENTER","EOF"]:
            if result == "":
                result = NoOp(0,0)
            return result
        else:
            raise Exception("Erro de sintaxe")

    def parseRelExp():
        result = Parser.parseExp()
        while Parser.tokenizer.atual.tipo in ["COMPARE","BIGGER","SMALLER"]:
            if Parser.tokenizer.atual.tipo == "COMPARE":
                Parser.tokenizer.selProx()
                result = BinOp("==",[result,Parser.parseExp()])
            elif Parser.tokenizer.atual.tipo == "BIGGER":
                Parser.tokenizer.selProx()
                result = BinOp(">",[result,Parser.parseExp()])
            elif Parser.tokenizer.atual.tipo == "SMALLER":
                Parser.tokenizer.selProx()
                result = BinOp("<",[result,Parser.parseExp()])
        return result

    def parseExp():
        result = Parser.parseTerm()
        while Parser.tokenizer.atual.tipo in ["PLUS","MINUS","OR"]:
            if Parser.tokenizer.atual.tipo == "PLUS":
                Parser.tokenizer.selProx()
                result = BinOp("+",[result,Parser.parseTerm()])
            elif Parser.tokenizer.atual.tipo == "MINUS":
                Parser.tokenizer.selProx()
                result = BinOp("-",[result,Parser.parseTerm()])
            elif Parser.tokenizer.atual.tipo == "OR":
                Parser.tokenizer.selProx()
                result = BinOp("||",[result,Parser.parseTerm()])
        return result

    def parseTerm():
        result = Parser.parseFactor()
        while Parser.tokenizer.atual.tipo in ["MULT","DIV","AND"]:
            if Parser.tokenizer.atual.tipo == "MULT":
                Parser.tokenizer.selProx()
                result = BinOp("*",[result,Parser.parseFactor()])
            elif Parser.tokenizer.atual.tipo == "DIV":
                Parser.tokenizer.selProx()
                result = BinOp("/",[result,Parser.parseFactor()])
            elif Parser.tokenizer.atual.tipo == "AND":
                Parser.tokenizer.selProx()
                result = BinOp("&&",[result,Parser.parseFactor()])
        return result
    
    def parseFactor():
        if Parser.tokenizer.atual.tipo == "INT":
            result = Parser.tokenizer.atual.valor
            Parser.tokenizer.selProx()
            return IntVal(result,[])
        elif Parser.tokenizer.atual.tipo == "STR":
            result = Parser.tokenizer.atual.valor
            Parser.tokenizer.selProx()
            return StrVal(result,[])
        elif Parser.tokenizer.atual.tipo == "TRUE":
            result = Parser.tokenizer.atual.valor
            Parser.tokenizer.selProx()
            return BoolVal(True,[])
        elif Parser.tokenizer.atual.tipo == "FALSE":
            result = Parser.tokenizer.atual.valor
            Parser.tokenizer.selProx()
            return BoolVal(False,[])
        elif Parser.tokenizer.atual.tipo == "PLUS":
            Parser.tokenizer.selProx()
            return UnOp("+",[Parser.parseFactor()])
        elif Parser.tokenizer.atual.tipo == "MINUS":
            Parser.tokenizer.selProx()
            return UnOp("-",[Parser.parseFactor()])
        elif Parser.tokenizer.atual.tipo == "NOT":
            Parser.tokenizer.selProx()
            return UnOp("!",[Parser.parseFactor()])
        elif Parser.tokenizer.atual.tipo == "OPEN":
            Parser.tokenizer.selProx()
            result = Parser.parseRelExp()
            if Parser.tokenizer.atual.tipo == "CLOSE":
                Parser.tokenizer.selProx()
                return result
            else:
                raise Exception("Erro de sintaxe")
        elif Parser.tokenizer.atual.tipo == "IDEN":
            identifier = Parser.tokenizer.atual.valor
            result = Identifier(identifier,[])
            Parser.tokenizer.selProx()
            return result
        else:
            raise Exception("Erro de sintaxe")

    def run():
        arquivo = open(argv[0],"r")
        lista = []
        for linha in arquivo:
            lista += PrePro.filter(linha)
        Parser.tokenizer = Tokenizer(lista)
        Parser.tokenizer.selProx()
        result = Parser.parseBlock()
        if Parser.tokenizer.atual.tipo == "EOF":
            return result
        else:
            raise Exception("Erro de sintaxe")
                 

class Node:
    def __init__(self,value,children):
        self.value = value #variant
        self.children = children # lista de nodes filhos
    def Evaluate(self):
        pass

class BinOp(Node):
    def Evaluate(self):
        if self.value == "+":
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == "-":
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif self.value == "*":
            eval0 = self.children[0].Evaluate()
            eval1 = self.children[1].Evaluate()
            if type(eval0) == type("string") or type(eval1) == type("string"):
                if eval0 == True:
                    eval0 = "true"
                elif eval0 == False:
                    eval0 = "false"
                if eval1 == True:
                    eval1 = "true"
                elif eval1 == False:
                    eval1 = "false"
                return str(eval0) + str(eval1)
            return eval0 * eval1
        elif self.value == "/":
            return self.children[0].Evaluate() // self.children[1].Evaluate()
        elif self.value == "=":
            valor = self.children[1].Evaluate()
            if not (type(Parser.st[self.children[0]][1]) == type(valor)):
                raise Exception("Variável não é do tipo especificado")
            Parser.st[self.children[0]][0] = valor
            return
        elif self.value == "::":
            valor = None
            if self.children[1] == "Int":
                valor = 1
            elif self.children[1] == "Bool":
                valor = True
            elif self.children[1] == "String":
                valor = "string"
            else:
                raise Exception("Tipo de variável desconhecido")
            Parser.st[self.children[0]] = [None,valor]
            return
        elif self.value == "&&":
            return self.children[0].Evaluate() and self.children[1].Evaluate()
        elif self.value == "||":
            return self.children[0].Evaluate() or self.children[1].Evaluate()
        elif self.value == "==":
            return self.children[0].Evaluate() == self.children[1].Evaluate()
        elif self.value == ">":
            return self.children[0].Evaluate() > self.children[1].Evaluate()
        elif self.value == "<":
            return self.children[0].Evaluate() < self.children[1].Evaluate()
        elif self.value == "while":
            while self.children[0].Evaluate():
                self.children[1].Evaluate()
            return
        else:
            raise Exception("Erro de sintaxe")

class UnOp(Node):
    def Evaluate(self):
        if self.value == "-":
            return -(self.children[0].Evaluate())
        elif self.value == "+":
            return self.children[0].Evaluate()
        elif self.value == "println":
            print(self.children[0].Evaluate())
            return
        elif self.value == "!":
            return not self.children[0].Evaluate()
        else:
            raise Exception("Erro de sintaxe")


class IntVal(Node):
    def Evaluate(self):
        return self.value

class StrVal(Node):
    def Evaluate(self):
        return self.value

class BoolVal(Node):
    def Evaluate(self):
        return self.value

class NoOp(Node):
    def Evaluate(self):
        if self.value == "readline":
            return int(input())
        pass

class Statements(Node):
    def Evaluate(self):
        for filho in self.children:
            filho.Evaluate()
        return

class Identifier(Node):
    def Evaluate(self):
        return Parser.st[self.value][0]

class IfOp(Node):
    def Evaluate(self):
        if self.children[0].Evaluate():
            self.children[1].Evaluate()
        else:
            self.children[2].Evaluate()
        return

def main():
    Parser.run().Evaluate()
    return

if __name__ == "__main__":
    main()