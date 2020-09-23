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

            if char == " ":
                if not numero == "":
                    saida.append(numero)
                    numero = ""
                continue
            elif char.isnumeric() == True:
                numero += char
            else:
                if not numero == "":
                    saida.append(numero)
                numero = ""
                saida.append(char)
            if char == "(":
                parenteses += 1
            if char == ")":
                if parenteses == 0:
                    raise Exception("Erro de gramática")
                parenteses -= 1
                
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
            prox = Token("EOF","eof")
            self.atual = prox
            return

        lido = self.origem[self.pos]

        if lido.isnumeric() == True:
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
        else:
            raise Exception("Erro de gramática")

class Parser:

    def parseExp():
        result = Parser.parseTerm()
        while Parser.tokenizer.atual.tipo in ["PLUS","MINUS"]:
            if Parser.tokenizer.atual.tipo == "PLUS":
                Parser.tokenizer.selProx()
                result += Parser.parseTerm()
            elif Parser.tokenizer.atual.tipo == "MINUS":
                Parser.tokenizer.selProx()
                result -= Parser.parseTerm()
        return result

    def parseTerm():
        result = Parser.parseFactor()
        while Parser.tokenizer.atual.tipo in ["MULT","DIV"]:
            if Parser.tokenizer.atual.tipo == "MULT":
                Parser.tokenizer.selProx()
                result = result * Parser.parseFactor()
            elif Parser.tokenizer.atual.tipo == "DIV":
                Parser.tokenizer.selProx()
                result = result // Parser.parseFactor()
        return result
    
    def parseFactor():
        if Parser.tokenizer.atual.tipo == "INT":
            result = Parser.tokenizer.atual.valor
            Parser.tokenizer.selProx()
            return result
        elif Parser.tokenizer.atual.tipo == "PLUS":
            Parser.tokenizer.selProx()
            return Parser.parseFactor()
        elif Parser.tokenizer.atual.tipo == "MINUS":
            Parser.tokenizer.selProx()
            return -(Parser.parseFactor())
        elif Parser.tokenizer.atual.tipo == "OPEN":
            Parser.tokenizer.selProx()
            result = Parser.parseExp()
            if Parser.tokenizer.atual.tipo == "CLOSE":
                Parser.tokenizer.selProx()
                return result
            else:
                raise Exception("Erro de sintaxe")
        else:
            raise Exception("Erro de sintaxe")

    def run():
        Parser.tokenizer = Tokenizer(PrePro.filter(argv[0]))
        Parser.tokenizer.selProx()
        result = Parser.parseExp()
        if Parser.tokenizer.atual.tipo == "EOF":
            return result
        else:
            raise Exception("Erro de sintaxe")
                 

def main():
    print(Parser.run())
    return

if __name__ == "__main__":
    main()