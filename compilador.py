import sys

argv = sys.argv[1:] #lista dos argumentos recebidos ao rodar o arquivo

def separador(entrada):
    numero = ""
    saida = []

    for char in entrada:
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
        else:
            raise Exception("Erro de gramática")

class Parser:
    def __init__(self,tokenizer):
        self.tokenizer = tokenizer
    
    def parseExp(self):
        self.tokenizer.selProx()
        resultado = 0
        if self.tokenizer.atual.tipo == "INT":
            resultado = self.tokenizer.atual.valor
            self.tokenizer.selProx()
            while self.tokenizer.atual.tipo in ["PLUS","MINUS"]:
                if self.tokenizer.atual.tipo == "PLUS":
                    self.tokenizer.selProx()
                    if self.tokenizer.atual.tipo == "INT":
                        resultado += self.tokenizer.atual.valor
                    else:
                        raise Exception("Erro de sintaxe")
                if self.tokenizer.atual.tipo == "MINUS":
                    self.tokenizer.selProx()
                    if self.tokenizer.atual.tipo == "INT":
                        resultado -= self.tokenizer.atual.valor
                    else:
                        raise Exception("Erro de sintaxe")
                self.tokenizer.selProx()
            if self.tokenizer.atual.tipo == "EOF":
                return resultado
            else:  
                raise Exception("EOF não encontrado")
        else:
            raise Exception("Erro de sintaxe")

    def run():
        #print("Operação: " + str(separador(argv[0])))
        tokenizer = Tokenizer(separador(argv[0]))
        parser = Parser(tokenizer)
        print(parser.parseExp())
        return 



def main():
    return Parser.run()

if __name__ == "__main__":
    main()
