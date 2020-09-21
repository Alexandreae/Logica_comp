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
        elif lido == "*":
            prox = Token("MULT",0)
            self.atual = prox
            self.pos += 1
            return
        elif lido == "/":
            prox = Token("DIV",0)
            self.atual = prox
            self.pos += 1
            return
        elif lido == "(":
            prox = Token("OPEN",0)
            self.atual = prox
            self.pos += 1
            return
        elif lido == ")":
            prox = Token("CLOSE",0)
            self.atual = prox
            self.pos += 1
            return
        else:
            raise Exception("Erro de gramática")

class Parser:
    tokenizerNum = []
    def __init__(self,tokenizerTerm):
        self.tokenizerTerm = tokenizerTerm

    def parseExp(entrada):
        parenteses = 0
        par = False
        lista = []
        listaPar = []

        for i in entrada:
            if i == "(":
                par = True
                parenteses += 1
                if parenteses == 1:
                    continue
                listaPar.append(i)

            if i == ")":
                parenteses += -1
                if parenteses == 0:
                    par = False
                    numero = Parser.parseExp(listaPar)
                    if numero < 0:
                        lista.append("-")
                        lista.append(str(numero))
                    else:
                        lista.append(str(numero))
                    listaPar = []
                    continue

            if par == True:
                listaPar.append(i)
            else:
                lista.append(i)

        tokenizer = Tokenizer(lista)
        parser = Parser(tokenizer)
        tokenizer2 = Tokenizer(parser.parseTerm())
        parser.tokenizerNum = tokenizer2
        return parser.parseNum()






    def parseTerm(self):
        self.tokenizerTerm.selProx()
        listaNum = []
        number = 0
        while self.tokenizerTerm.atual.tipo in ["PLUS","MINUS"]:
            if self.tokenizerTerm.atual.tipo == "PLUS":
                listaNum.append("+")
            else:
                listaNum.append("-")
            self.tokenizerTerm.selProx()

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
        negativo = False

        while self.tokenizerNum.atual.tipo in ["PLUS","MINUS"]:
            if self.tokenizerNum.atual.tipo == "MINUS":
                if negativo == True:
                    negativo = False
                else:
                    negativo = True
            self.tokenizerNum.selProx()

        if self.tokenizerNum.atual.tipo == "INT":
            if negativo == False:
                resultado = self.tokenizerNum.atual.valor
            else:
                resultado = -self.tokenizerNum.atual.valor
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
        print(Parser.parseExp(PrePro.filter(argv[0])))
        return 



def main():
    return Parser.run()

if __name__ == "__main__":
    main()
