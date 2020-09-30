import sys

argv = sys.argv[1:] #lista dos argumentos recebidos ao rodar o arquivo
class PrePro:
    def filter(entrada):
        parenteses = 0
        numero = ""
        saida = []
        comment = False
        skip = False
        for i in range(len(entrada)):
            char = entrada[i]
            if skip == True:
                skip = False
                continue
            if comment == True:
                if char == "=" and entrada[i+1] == "#":
                    comment = False #fim do comentario
                    skip = True
                    if not numero == "":
                        saida.append(numero)
                        numero = ""
                    continue
                else:
                    continue
            if char == "#" and entrada[i+1] == "=": #começo do comentario
                comment = True
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
        elif lido[0].isalpha():
            for i in lido:
                if i.isnumeric() or i.isalpha() or i == "_":
                    continue
                else:
                    raise Exception("Erro de gramática")
            prox = Token("IDEN",lido)
            self.atual = prox
            self.pos += 1
        elif lido == "\n":
            prox = Token("ENTER",lido)
            self.atual = prox
            self.pos += 1
        else:
            raise Exception("Erro de gramática")

class Parser:
    st = {}
    def parseBlock():
        while not Parser.tokenizer.atual.tipo == "EOF":
            Parser.parseCommand()
            Parser.tokenizer.selProx()
        return NoOp(0,0)
    def parseCommand():
        if Parser.tokenizer.atual.tipo == "IDEN":
            identifier = Parser.tokenizer.atual.valor
            Parser.tokenizer.selProx()
            if Parser.tokenizer.atual.tipo == "EQUAL":
                Parser.tokenizer.selProx()
                Parser.st[identifier] = Parser.parseExp().Evaluate()
            else:
                raise Exception("Erro de sintaxe")

        elif Parser.tokenizer.atual.tipo == "PRINT":
            Parser.tokenizer.selProx()
            if not Parser.tokenizer.atual.tipo == "OPEN":
                raise Exception("Erro de sintaxe")
            else:
                Parser.tokenizer.selProx()
            result = Parser.parseExp().Evaluate()
            print(result)
            Parser.tokenizer.selProx()
            if Parser.tokenizer.atual.tipo == "CLOSE":
                Parser.tokenizer.selProx()
        if Parser.tokenizer.atual.tipo in ["ENTER","EOF"]:
            return
        else:
            raise Exception("Erro de sintaxe")


    def parseExp():
        result = Parser.parseTerm()
        while Parser.tokenizer.atual.tipo in ["PLUS","MINUS"]:
            if Parser.tokenizer.atual.tipo == "PLUS":
                Parser.tokenizer.selProx()
                result = BinOp("+",[result,Parser.parseTerm()])
            elif Parser.tokenizer.atual.tipo == "MINUS":
                Parser.tokenizer.selProx()
                result = BinOp("-",[result,Parser.parseTerm()])
        return result

    def parseTerm():
        result = Parser.parseFactor()
        while Parser.tokenizer.atual.tipo in ["MULT","DIV"]:
            if Parser.tokenizer.atual.tipo == "MULT":
                Parser.tokenizer.selProx()
                result = BinOp("*",[result,Parser.parseFactor()])
            elif Parser.tokenizer.atual.tipo == "DIV":
                Parser.tokenizer.selProx()
                result = BinOp("/",[result,Parser.parseFactor()])
        return result
    
    def parseFactor():
        if Parser.tokenizer.atual.tipo == "INT":
            result = Parser.tokenizer.atual.valor
            Parser.tokenizer.selProx()
            return IntVal(result,[])
        elif Parser.tokenizer.atual.tipo == "PLUS":
            Parser.tokenizer.selProx()
            return UnOp("+",[Parser.parseFactor()])
        elif Parser.tokenizer.atual.tipo == "MINUS":
            Parser.tokenizer.selProx()
            return UnOp("-",[Parser.parseFactor()])
        elif Parser.tokenizer.atual.tipo == "OPEN":
            Parser.tokenizer.selProx()
            result = Parser.parseExp()
            if Parser.tokenizer.atual.tipo == "CLOSE":
                Parser.tokenizer.selProx()
                return result
            else:
                raise Exception("Erro de sintaxe")
        elif Parser.tokenizer.atual.tipo == "IDEN":
            identifier = Parser.tokenizer.atual.valor
            if not identifier in Parser.st:
                raise Exception("Erro de sintaxe")
            result = Parser.st[identifier]
            Parser.tokenizer.selProx()
            return IntVal(result,[])
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
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif self.value == "/":
            return self.children[0].Evaluate() // self.children[1].Evaluate()
        else:
            raise Exception("Erro de sintaxe")

class UnOp(Node):
    def Evaluate(self):
        if self.value == "-":
            return -(self.children[0].Evaluate())
        else:
            return self.children[0].Evaluate()


class IntVal(Node):
    def Evaluate(self):
        return self.value

class NoOp(Node):
    def Evaluate(self):
        pass

def main():
    Parser.run().Evaluate()
    return

if __name__ == "__main__":
    main()