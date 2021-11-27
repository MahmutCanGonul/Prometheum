# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 13:12:09 2021

@author: Mahmut Can Gonol
"""
########################################
            #CONSTANTS
DIGITS = '0123456789'
####################################

########################################
            #ERRORS

class Error:
    def __init__(self,pos_start,pos_end,error_name,detail):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.detail = detail
        
    def error_message(self):
        result = f'{self.error_name}:{self.detail}'
        result += f'File: {self.pos_start.fn}, line: {self.pos_start.ln + 1}'
        return result



class IllegalCharError(Error):
    def __init__(self,pos_start,pos_end,detail):
        super().__init__(pos_start, pos_end ,' Illegal Character',detail)
        
class InvalidSyntaxError(Error):
    def __init__(self,pos_start,pos_end,detail= ''):
        super().__init__(pos_start, pos_end ,' Invalid Syntax',detail)
        

        
########################################

###############################
        #POSITION
        
class Position:
    def __init__(self,idx,ln,col,fn,ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    def advance(self,current_char=None):
        self.idx+=1
        self.col+=1
        
        if current_char == '\n':
            self.ln+=1
            self.col=0
            
        return self
    
    def copy(self):
        return Position(self.idx,self.ln,self.col,self.fn,self.ftxt)
        
     
###############################


TT_INT = "INT" #integer value
TT_FLOAT = "FLOAT" #float value
TT_MINUS = "MINUS" #minus
TT_PLUS = "PLUS" #plus
TT_MUL = "MUL" #multiple
TT_DIV = "DIV" #divide
TT_LPAREN = "LPAREN" #lparen (
TT_RPAREN = "RPAREN" #rparen )
TT_EOF = "EOF" # EOF mean is input

############## TOKEN PART ###############

class Token:
    def __init__(self,type_,value=None,pos_start = None, pos_end = None):
        self.type = type_
        self.value = value
        
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        
        if pos_end:
            self.pos_end = pos_end
        
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    



############## LEXER PART ##############
        
class Lexer:
    def __init__(self,fn,text):
        self.text = text
        self.fn = fn
        self.pos = Position(-1,0,-1,fn,text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]
        else:
            self.current_char = None
        
        
    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            if self.current_char in ' \t': #This part help to make a break
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS,pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS,pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL,pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV,pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN,pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN,pos_start=self.pos))
                self.advance()
            else:
                ## Error Part
                pos_start = self.pos.copy()
                char = self.current_char
                """
                take_error_word = []
                is_error=False
                for  i in range(len(self.text)):
                    if self.text[i] == char and is_error!=True:
                        take_error_word.append(self.text[i])
                        is_error = True
                    if is_error == True and self.text[i] != ' ':
                        take_error_word.append(self.text[i])
                    if is_error == True and self.text[i] == ' ':
                        is_error=False
                result_error =""
                if len(take_error_word) > 1:
                    for i in range(len(take_error_word)):
                        result_error += take_error_word[i]
                else:
                    result_error = take_error_word[0]
                """
                self.advance()
                return [],IllegalCharError(pos_start,self.pos,"'" + char + "'")
        # I added this part for some easy mathematic calculations
        take_numbers = []
        take_operator = []
        for i in range(len(tokens)):
             
            number = []
            ex = str(tokens[i])
            if 'PLUS' or 'MINUS' in ex:
                if i == 0:
                    take_numbers.append(int(0))
            if ':' in ex:
                number = ex.split(':')
            if len(number) > 0:
                if number[0] == 'INT':
                    take_numbers.append(int(number[1]))
                elif number[0] == 'FLOAT':
                    take_numbers.append(float(number[1]))
            else:
                take_operator.append(str(tokens[i]))
        result = 0
        first_result=0
        is_has_plus_minus=False
        #This function make mathematic calculations 
        for i in range(len(take_operator)):
            if take_operator[i] == 'MUL' and len(take_numbers) > 1:
                first_result = take_numbers[i] * take_numbers[i+1]
                take_numbers[i+1] = first_result
                take_numbers[i] = first_result
                
            elif take_operator[i] == 'DIV'  and len(take_numbers) > 1:
                first_result = take_numbers[i] / take_numbers[i+1]
                take_numbers[i+1] = first_result
                take_numbers[i] = first_result
            
            elif take_operator[i] == 'PLUS' or take_operator[i] == 'MINUS':
                is_has_plus_minus=True
        
        if is_has_plus_minus == False:
            result = first_result
            if result != 0:
              print(result)
            tokens.append(Token(TT_EOF,pos_start=self.pos))     
            return tokens,None
      
        
        for i in range(len(take_operator)):
                if take_operator[i] == 'PLUS'  and len(take_numbers) > 1:
                    result = take_numbers[i] + take_numbers[i+1]
                    take_numbers[i+1] = result
                if take_operator[i] == 'MINUS'  and len(take_numbers) > 1:
                    result = take_numbers[i] - take_numbers[i+1]
                    take_numbers[i+1] = result
                
            
        if result != 0:     
           print(result)
                
            
                   
                
                
                    
        tokens.append(Token(TT_EOF,pos_start=self.pos))        
        return tokens,None
                
                
                
            
    def make_number(self):
        num_str = ''
        dot_count = 0
        take_firt_float_char = []
        pos_start = self.pos.copy()
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count +=1
                num_str = '.'
            else:
                take_firt_float_char.append(self.current_char)
                num_str += self.current_char
            
            self.advance()
                
        if dot_count == 0:
            return Token(TT_INT, int(num_str),pos_start,self.pos)
        else:
            return Token(TT_FLOAT,float(num_str) + float(take_firt_float_char[0]),pos_start,self.pos)
        

####################################
        #NODES
 

class NumberNode:
    def __init__(self,tok):
        self.tok = tok
    def __repr__(self):
        return f'{self.tok}'


class BinOpNode:
    def __init__(self,left_node,op_tok,right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
    def __init__(self,op_tok,node):
        self.op_tok = op_tok
        self.node = node
    def __repr__(self):
        return f'({self.op_tok}, {self.node})'
        
        
####################################
   

#PARSE RESULT


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        
    def register(self,res):
        if isinstance(res,ParseResult):
            if res.error:
                self.error = res.error
            return res.node
        return res
        
    def success(self,node):
        self.node = node
        return self
        
    def failure(self,error):
        self.error = error
        return self
    


####################################

     
####################################
        #PARSER
        

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
    
    def advance(self):
        self.tok_idx +=1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    
    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected '+' or '-' or '*' or '/'"))
            
        return res
        
    
    def factor(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type in (TT_PLUS,TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok,factor))
            
        
        
        elif tok.type in (TT_INT,TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.type in TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected ')'"))
               
            
        
        
        return res.failure(InvalidSyntaxError(tok.pos_start,tok.pos_end,"Expected int or float! After the '+' or '-' or '*' or '/': "))
        
        
    def term(self): # Multiple and Divide Operation Control
        return self.bin_op(self.factor,(TT_MUL,TT_DIV))
     
        
    def expr(self): #Plus and Minus Operation Control
        return self.bin_op(self.term,(TT_PLUS,TT_MINUS))
     
        
    
    
    def bin_op(self,func,ops):
        res = ParseResult()
        left = res.register(func())
        
        if res.error:
            return res
        
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = BinOpNode(left,op_tok,right)
            
        return res.success(left)

####################################

  
###################################
       #RUN
###################################

def run(fn,text):
    #Generate tokens
    lexer = Lexer(fn,text)
    tokens,error = lexer.make_tokens()
    if error:
        return None,error
        
    #Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node,ast.error
       
       
       
       





