import sys

argv = sys.argv[1:] #lista dos argumentos recebidos ao rodar o arquivo


class PrePro:
    def filter(entrada):
        numero = ""
        saida = []
        comment = False
        for char in entrada:
            if comment == True:
                if char == "#":
                    comment = False #fim do comentario
                    if not numero == "":
                        saida.append(numero)
                        numero = ""
                    continue
                else:
                    continue
            if char == "#": #começo do comentario
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
                
        if not numero == "":
            saida.append(numero)
        if comment == True:
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

        if lido.isnumeric() == True:
            prox = Token("INT",int(lido))
            self.atual = prox
            self.pos += 1
            return
        elif lido == "+":
            prox = Token("PLUS",0)
            self.atual = prox
            self.pos += 1
            return
        elif lido == "-":
            prox = Token("MINUS",0)
            self.atual = prox
            self.pos += 1
            return
        elif lido == "x":
            prox = Token("MULT",0)
            self.atual = prox
            self.pos += 1
            return
        elif lido == "/":
            prox = Token("DIV",0)
            self.atual = prox
            self.pos += 1
            return
        else:
            raise Exception("Erro de gramática")

class Parser:
    tokenizerNum = []
    def __init__(self,tokenizerTerm):
        self.tokenizerTerm = tokenizerTerm

    def parseTerm(self):
        self.tokenizerTerm.selProx()
        listaNum = []
        number = 0
        if self.tokenizerTerm.atual.tipo == "INT":
            number = self.tokenizerTerm.atual.valor
            self.tokenizerTerm.selProx()
        else:
            raise Exception("Erro de sintaxe")
        while self.tokenizerTerm.atual.tipo in ["PLUS","MINUS","MULT","DIV"]:
            if self.tokenizerTerm.atual.tipo == "MULT":
                self.tokenizerTerm.selProx()
                if self.tokenizerTerm.atual.tipo == "INT":
                    number = number * self.tokenizerTerm.atual.valor
                else:
                    raise Exception("Erro de sintaxe")

            if self.tokenizerTerm.atual.tipo == "DIV":
                self.tokenizerTerm.selProx()
                if self.tokenizerTerm.atual.tipo == "INT":
                    number = int(number / self.tokenizerTerm.atual.valor)
                else:
                    raise Exception("Erro de sintaxe")                

            if self.tokenizerTerm.atual.tipo == "PLUS":
                listaNum.append(str(number))
                listaNum.append("+")
                self.tokenizerTerm.selProx()
                if self.tokenizerTerm.atual.tipo == "INT":
                    number = self.tokenizerTerm.atual.valor
                else:
                    raise Exception("Erro de sintaxe")

            if self.tokenizerTerm.atual.tipo == "MINUS":
                listaNum.append(str(number))
                listaNum.append("-")
                self.tokenizerTerm.selProx()
                if self.tokenizerTerm.atual.tipo == "INT":
                    number = self.tokenizerTerm.atual.valor
                else:
                    raise Exception("Erro de sintaxe")
            self.tokenizerTerm.selProx()
        listaNum.append(str(number))
        if self.tokenizerTerm.atual.tipo == "EOF":
            return listaNum
        else:
            raise Exception("EOF não encontrado")

        
    def parseNum(self):
        self.tokenizerNum.selProx()
        resultado = 0
        if self.tokenizerNum.atual.tipo == "INT":
            resultado = self.tokenizerNum.atual.valor
            self.tokenizerNum.selProx()
            while self.tokenizerNum.atual.tipo in ["PLUS","MINUS"]:
                if self.tokenizerNum.atual.tipo == "PLUS":
                    self.tokenizerNum.selProx()
                    if self.tokenizerNum.atual.tipo == "INT":
                        resultado += self.tokenizerNum.atual.valor
                    else:
                        raise Exception("Erro de sintaxe")
                if self.tokenizerNum.atual.tipo == "MINUS":
                    self.tokenizerNum.selProx()
                    if self.tokenizerNum.atual.tipo == "INT":
                        resultado -= self.tokenizerNum.atual.valor
                    else:
                        raise Exception("Erro de sintaxe")
                self.tokenizerNum.selProx()
            if self.tokenizerNum.atual.tipo == "EOF":
                return resultado
            else:  
                raise Exception("EOF não encontrado")
        else:
            raise Exception("Erro de sintaxe")

    def run():
        tokenizerTerm = Tokenizer(PrePro.filter(argv[0]))
        parser = Parser(tokenizerTerm)
        tokenizerNum = Tokenizer(parser.parseTerm())
        parser.tokenizerNum = tokenizerNum

        print(parser.parseNum())
        return 



def main():
    return Parser.run()

if __name__ == "__main__":
    main()
