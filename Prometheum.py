# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 13:12:09 2021

@author: Mahmut Can Gonol
"""
#####IMPORTS
import string 



########################################
            #CONSTANTS
DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
####################################


####################################
        #SYMBOLTABLE


class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None
        
    def get(self,name):
        value = self.symbols.get(name,None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value
    def set(self,name,value):
        self.symbols[name] = value
    
    def remove(self,name):
        del self.symbols[name]
        
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



class ExpectedCharError:
    def __init__(self,pos_start,pos_end,detail):
        super().__init__(pos_start,pos_end,'Expected character error',detail)

class IllegalCharError(Error):
    def __init__(self,pos_start,pos_end,detail):
        super().__init__(pos_start, pos_end ,' Illegal Character',detail)
        
class InvalidSyntaxError(Error):
    def __init__(self,pos_start,pos_end,detail= ''):
        super().__init__(pos_start, pos_end ,' Invalid Syntax',detail)

class RunTimeError(Error):
    def __init__(self,pos_start,pos_end,detail,context):
        super().__init__(pos_start, pos_end ,' Runtime Error',detail)
        self.context = context
    def error_message(self):
        result = self.generate_traceback()
        result += f'{self.error_name}:{self.detail}'
        return result
    
    def generate_traceback(self):
        result =''
        pos = self.pos_start
        ctx = self.context
        
        while ctx:
            result = f' File: {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
            
        return 'Traceback (most recent call last):\n' + result
    
            
            
            
        
        

        
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
TT_POW = "POW"
TT_EQ = "EQ"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_EE = "EE"
TT_NE = "NE"
TT_LT = "LT"
TT_GT = "GT"
TT_GTE = "GTE"
TT_LTE = "LTE"


KEYWORDS = ['var','and','or','not','if','THEN','elif','else','for','TO','STEP','while']


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
        
    def matches(self,type_,value):
        return self.type == type_ and self.value == value
    
    
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
            elif self.current_char == '^':
                tokens.append(Token(TT_POW,pos_start=self.pos))
                self.advance()
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            
            elif self.current_char == '!':
                tok,error = self.make_not_equals()
                if error:
                    return [],error
                tokens.append(tok)
            
            
            
                
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())

            
            
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
        """
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
        """       
         
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


    def make_identifier(self):
        idx_str = ''
        pos_start = self.pos.copy()
        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            idx_str += self.current_char
            self.advance()
        tok_type = TT_KEYWORD if idx_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, idx_str,pos_start,self.pos)
        
        
    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start = pos_start,pos_end=self.pos),None
        self.advance()
        return None,ExpectedCharError(pos_start,self.pos,"'=' (after '!')")
         
    def make_equals(self):
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=': # if you have == change the tok_type to TT_EE 
            self.advance()
            tok_type = TT_EE
           
        return Token(tok_type, pos_start = pos_start,pos_end=self.pos)
     
    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=': 
            self.advance()
            tok_type = TT_GTE
           
        return Token(tok_type, pos_start = pos_start,pos_end=self.pos)
        
    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':  
            self.advance()
            tok_type = TT_LTE
           
        return Token(tok_type, pos_start = pos_start,pos_end=self.pos)
        
        

####################################
        #NODES


class NumberNode:
    def __init__(self,tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    def __repr__(self):
        return f'{self.tok}'

class VarAccessNode:
    def __init__(self,var_name_tok):
        self.var_name_tok = var_name_tok
    
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
    def __init__(self,var_name_tok,value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end
        
        
        
        
    


class BinOpNode:
    def __init__(self,left_node,op_tok,right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end
        
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
    def __init__(self,op_tok,node):
        self.op_tok = op_tok
        self.node = node
        
        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end
        
        
    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

class IfNode:
    def __init__(self,cases,else_cases):
        self.cases = cases
        self.else_cases = else_cases
        
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_cases or self.cases[len(self.cases)-1][0]).pos_end
        
        
        
class ForNode: 
    def __init__(self,var_name_tok,start_value_node,end_value_node,step_value_node,body_node):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end
        
        
        
class WhileNode:  
    def __init__(self,condition_node,body_node):
        self.condition_node = condition_node
        self.body_node = body_node
        
        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end
       
        
    


        
        
####################################
   

#PARSE RESULT


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count=0
        
    def register(self,res):
        self.advance_count += res.advance_count
        if res.error:
          self.error = res.error
        return res.node
       
    def register_advacement(self):
        self.advance_count+=1
        pass
    
    def success(self,node):
        self.node = node
        return self
        
    def failure(self,error):
        if not self.error or self.advance_count ==0: #Haven not advance since
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
        
    def atom(self):
        res = ParseResult()
        tok = self.current_tok
        if tok.type in (TT_INT,TT_FLOAT):
            """
            res.register(self.advance())   # Remove this code from the under the line of code
            """
            res.register_advacement()
            self.advance()
            
            
            return res.success(NumberNode(tok))
        
        elif  tok.type == TT_IDENTIFIER:
            res.register_advacement()
            self.advance()
            return res.success(VarAccessNode(tok))
        
        
        elif tok.type == TT_LPAREN:
            res.register_advacement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advacement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected ')'"))
        
        elif tok.matches(TT_KEYWORD,'if'):
            if_expr = res.register(self.if_expr())
            if res.error: 
                return res
            return res.success(if_expr)
            
        elif tok.matches(TT_KEYWORD,'for'):
            for_expr = res.register(self.for_expr())
            if res.error: 
                return res
            return res.success(for_expr)
         
        elif tok.matches(TT_KEYWORD,'while'):
            while_expr = res.register(self.while_expr())
            if res.error: 
                return res
            return res.success(while_expr)    
                
        
        return res.failure(InvalidSyntaxError(tok.pos_start,tok.pos_end,"Expected int, float, identifier! After the '+' or '-' or '*' or '/': "))
    
    
    
    def for_expr(self):
        res = ParseResult()
        
        if not self.current_tok.matches(TT_KEYWORD,'for'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected 'if'"))
        
        res.register_advacement()
        self.advance()
    
        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected identifier!"))
           
        var_name = self.current_tok
        res.register_advacement()
        self.advance()
        
        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected '='"))
        
        
        res.register_advacement()
        self.advance()
        
        start_value = res.register(self.expr()) 
        if res.error:
            return res
        
        if not self.current_tok.matches(TT_KEYWORD,'TO'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected 'TO'"))
        
        
        res.register_advacement()
        self.advance()
       
        end_value = res.register(self.expr())
        if res.error:
            return res
        
        
        
        
        if self.current_tok.matches(TT_KEYWORD,'STEP'):
           res.register_advacement()
           self.advance()
           
           step_value = res.register(self.expr())
           if res.error:
               return res
        else:
           step_value = None
         
        if not self.current_tok.matches(TT_KEYWORD,'THEN'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected 'THEN'"))
        
        res.register_advacement()
        self.advance()
       
        body = res.register(self.expr())
        if res.error:
            return res
        
        
        return res.success(ForNode(var_name,start_value,end_value,step_value,body))
        
        
               
    def while_expr(self):
        res = ParseResult()
        
        if not self.current_tok.matches(TT_KEYWORD,'while'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected 'while'"))
        
        res.register_advacement()
        self.advance()
        
        condition = res.register(self.expr())
        
        if res.error:
            return res
        
        if not self.current_tok.matches(TT_KEYWORD,'THEN'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected 'THEN'"))
        
        res.register_advacement()
        self.advance()
        
        body_node = res.register(self.expr())
        
        if res.error:
            return res
        
        return res.success(WhileNode(condition,body_node))
        
        
        
       
    
    
    def if_expr(self):
        res = ParseResult()
        cases = []
        else_cases = None
        if not self.current_tok.matches(TT_KEYWORD,'if'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected 'if'"))
        
        res.register_advacement()
        self.advance()
        
        condition = res.register(self.expr())
        if res.error:
            return res
        
        if not self.current_tok.matches(TT_KEYWORD,'THEN'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected 'THEN'"))
        
        
        res.register_advacement()
        self.advance()
        
        expr = res.register(self.expr())
        if res.error:
            return res
        cases.append((condition,expr))
        
        while self.current_tok.matches(TT_KEYWORD,'elif'):
            res.register_advacement()
            self.advance()
            condition = res.register(self.expr())
            if res.error:
               return res
        
            if not self.current_tok.matches(TT_KEYWORD,'THEN'):
               return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected 'THEN'"))
            
            res.register_advacement()
            self.advance()
        
            expr = res.register(self.expr())
            if res.error:
               return res
            cases.append((condition,expr))
        
        if self.current_tok.matches(TT_KEYWORD,'else'):
            res.register_advacement()
            self.advance()
            else_cases = res.register(self.expr())
            if res.error:
               return res
        return res.success(IfNode(cases,else_cases))
        
        
            
        

            
            
            
        
        
        
        
        
            
            
            
            
        
        
        
        
        
        
        
        
    
    
    def power(self):
        return self.bin_op(self.atom,(TT_POW, ),self.factor)
        
    
    def factor(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type in (TT_PLUS,TT_MINUS):
            res.register_advacement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok,factor))
        
        return self.power()
        
               
    def term(self): # Multiple and Divide Operation Control
        return self.bin_op(self.factor,(TT_MUL,TT_DIV))
     
     
    def comp_expr(self):
        res = ParseResult()
        
        if self.current_tok.matches(TT_KEYWORD,'not'):
            op_tok = self.current_tok
            res.register_advacement()
            self.advance()
            
            
            node = res.register(self.comp_expr())
            if res.error:
               return res
            return res.success(UnaryOpNode(op_tok,node))
      
        node = res.register(self.bin_op(self.arith_expr, (TT_EE,TT_NE,TT_GT,TT_LT,TT_GTE,TT_LTE)))
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected int, float, identifier! After the '+' or '-' or '*' or '/' or 'not': "))
        
        return res.success(node)
    
        
        
    def arith_expr(self):
        return self.bin_op(self.term,(TT_PLUS,TT_MINUS))
        
    
    
    def expr(self): #Plus and Minus Operation Control
        res = ParseResult()
        if self.current_tok.matches(TT_KEYWORD,'var'):
            res.register_advacement()
            self.advance()
            
            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end," Expected identifier!"))
            
            var_name = self.current_tok
            res.register_advacement()
            self.advance()
            
            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end," Expected '=' "))
            
            res.register_advacement()
            self.advance()
            var_expr =  res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name,var_expr))
        """        
        elif self.current_tok.matches(TT_KEYWORD,'int'):
            res.register_advacement()
            self.advance()
            
            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end," Expected identifier!"))
            
            var_name = self.current_tok
            res.register_advacement()
            self.advance()
            
            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end," Expected '=' "))
            
            res.register_advacement()
            self.advance()
            var_expr =  res.register(self.expr())
            result = Number(var_expr)
            take_value = str(result).split(':')
            if len(take_value) != 0:
                if take_value[len(take_value)-1].isdigit() == False:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end," Expected integer value! "))
            if res.error:
                return res
            take_value = []
            return res.success(VarAssignNode(var_name,var_expr))
            
          """  
        
        
        node = res.register(self.bin_op(self.comp_expr,((TT_KEYWORD,"and"),(TT_KEYWORD,"or"))))
        
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected 'var',int,float, identifier,'+' or '-' or '*' or '/' "))
        
        return res.success(node)
    
    
    
    def bin_op(self,func_a,ops,func_b=None):
        if func_b == None: # if func_b is empty
            func_b = func_a # equal to func_a
            
        res = ParseResult()
        left = res.register(func_a()) #For left  use a different func
        
        if res.error:
            return res
        
        while self.current_tok.type in ops or (self.current_tok.type,self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advacement()
            self.advance()
            right = res.register(func_b()) #For right  use a different func
            if res.error:
                return res
            left = BinOpNode(left,op_tok,right)
            
        return res.success(left)

####################################

####################################
        #RUNTIME RESULT



class RuntimeResult:
    def __init__(self):
        self.error = None
        self.value=None
        
    def register(self,res):
        if res.error:
            self.error = res.error
        return res.value
    def success(self,value):
        self.value = value
        return self
    
    def failure(self,error):
        self.error = error
        return self
    
    
####################################



#################################
        #VALUES
        

class Number:
    def __init__(self,value):
        self.value = value
        self.set_pos()
        self.set_context()
    def set_pos(self,pos_start=None,pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def set_context(self,context=None):
        self.context = context
        return self
    
    def add_method(self,other):
        if isinstance(other,Number):
            return Number(self.value + other.value).set_context(self.context),None
    def minus_method(self,other):
        if isinstance(other,Number):
            return Number(self.value - other.value).set_context(self.context),None
    def multiple_method(self,other):
        if isinstance(other,Number):
            return Number(self.value * other.value).set_context(self.context),None
    def divide_method(self,other):
        if isinstance(other,Number):
            if other.value == 0:
                return None,RunTimeError(other.pos_start,other.pos_end,"Division by zero issue!",self.context)

            return Number(self.value / other.value).set_context(self.context),None
    def power_method(self,other):
        if isinstance(other,Number):
            return Number(self.value ** other.value).set_context(self.context),None
    
    def get_comparison_eq(self,other):
        if isinstance(other,Number):
            return Number(int(self.value == other.value)).set_context(self.context),None
    
    def get_comparison_ne(self,other):
        if isinstance(other,Number):
            return Number(int(self.value != other.value)).set_context(self.context),None
    def get_comparison_lt(self,other):
        if isinstance(other,Number):
            return Number(int(self.value < other.value)).set_context(self.context),None
    def get_comparison_gt(self,other):
        if isinstance(other,Number):
            return Number(int(self.value > other.value)).set_context(self.context),None
    def get_comparison_gte(self,other):
        if isinstance(other,Number):
            return Number(int(self.value >= other.value)).set_context(self.context),None
    def get_comparison_lte(self,other):
        if isinstance(other,Number):
            return Number(int(self.value <= other.value)).set_context(self.context),None
    def anded_by(self,other):
        if isinstance(other,Number):
            return Number(int(self.value and other.value)).set_context(self.context),None
    def ored_by(self,other):
        if isinstance(other,Number):
            return Number(int(self.value or other.value)).set_context(self.context),None
    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context),None
        
    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start,self.pos_end)
        copy.set_context(self.context)
        return copy
    
    
    
    def __repr__(self):
        return str(self.value)
    
    def is_true(self):
        return self.value!=0
    

#################################

################################
        #CONTEXT
        
class Context:
    def __init__(self,display_name,parent=None,parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None
        
################################




####################################
        #INTERPRETER

class Interpreter:
    def visit(self,node,context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method) #Issue is here beacuse return None
        return method(node,context)
    
    def no_visit_method(self,node,context):
        raise Exception(f'No visit_{type(node).__name__} method defined!')
    
    def visit_NumberNode(self,node,context):
        return RuntimeResult().success(Number(node.tok.value).set_context(context).set_pos(node.pos_start,node.pos_end)) #Don't forget when you call class put ()
    
    def visit_VarAccessNode(self,node,context):
        res = RuntimeResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)
        
        
        if not value:
            return res.failure(RunTimeError(node.pos_start,node.pos_end,f'{var_name} is not defined',context))
        
        value = value.copy().set_pos(node.pos_start,node.pos_end)
        return res.success(value)
    
    def visit_VarAssignNode(self,node,context):
        res = RuntimeResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node,context))
        
        if res.error:
            return res
        
        context.symbol_table.set(var_name,value)
        return res.success(value)
    
        
        
            
    
        
    
    def visit_BinOpNode(self,node,context):
        res = RuntimeResult()
        left = res.register(self.visit(node.left_node,context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node,context)) 
        if res.error:
            return res
        
        result=None
        if left != None and right != None:
            if node.op_tok.type == TT_PLUS:
                result,error = left.add_method(right)
            elif node.op_tok.type == TT_MINUS:
                result,error = left.minus_method(right)
            elif node.op_tok.type == TT_MUL:
                result,error = left.multiple_method(right)
            elif node.op_tok.type == TT_DIV:
                result,error = left.divide_method(right)
            elif node.op_tok.type == TT_POW:
                result,error = left.power_method(right)
            elif node.op_tok.type == TT_EE:
                result,error = left.get_comparison_eq(right)
            elif node.op_tok.type == TT_NE:
                result,error = left.get_comparison_ne(right)
            elif node.op_tok.type == TT_LT:
                result,error = left.get_comparison_lt(right)
            elif node.op_tok.type == TT_GT:
                result,error = left.get_comparison_gt(right)
            elif node.op_tok.type == TT_LTE:
                result,error = left.get_comparison_lte(right)
            elif node.op_tok.type == TT_GTE:
                result,error = left.get_comparison_gte(right)
            elif node.op_tok.matches(TT_KEYWORD,'and'):
                result,error = left.anded_by(right)
            elif node.op_tok.matches(TT_KEYWORD,'or'):
                result,error = left.ored_by(right)
               
            
                
                
                
            
            if error:
                return res.failure(error)
            else:
                result = res.success(result.set_pos(node.pos_start,node.pos_end))
                return result
        
    def visit_UnaryOpNode(self,node,context):
        res = RuntimeResult()
        number = res.register(self.visit(node.node,context))
        if res.error:
            return res
        error = None
        if node.op_tok.type == TT_MINUS:
            number,error = number.multiple_method(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD,'not'):
            number,error = number.notted()
        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start,node.pos_end))
    
    def visit_IfNode(self,node,context):
        res = RuntimeResult()
        
        for condition,expr in node.cases:
            condition_value = res.register(self.visit(condition,context))
            if res.error:
                return res
            if condition_value.is_true():
                expr_value = res.register(self.visit(expr,context))
                if res.error:
                   return res
                return res.success(expr_value)
            
        if node.else_cases:
             else_value = res.register(self.visit(node.else_cases,context))
             if res.error:
                 return res
             res.success(else_value)
        
        return res.success(None)
        
    def visit_ForNode(self,node,context):
        res = RuntimeResult()
        start_value = res.register(self.visit(node.start_value_node,context))
        if res.error:
            return res
        end_value = res.register(self.visit(node.end_value_node,context))
        if res.error:
           return res
        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node,context))
            if res.error:
                return res
        else:
            step_value = Number(1) #Return 1 
        
        x = start_value.value
        if step_value.value >=0:
            condition = lambda: x < end_value.value
        else:
            condition = lambda: x > end_value.value
       
        while condition():
            context.symbol_table.set(node.var_name_tok.value,Number(x))
            x+= step_value.value
            
            res.register(self.visit(node.body_node,context))
            if res.error:
                return res
            
        return res.success(None)
            
    def visit_WhileNode(self,node,context):
         res = RuntimeResult()
         while True:
             condition = res.register(self.visit(node.condition_node,context))
             if res.error:
                return res
             if not condition.is_true():
                break
         
             res.register(self.visit(node.body_node,context))
             if res.error:
                return res
         return res.success(None)
        
         
           
        
            
            
            
    

####################################

  
###################################
       #RUN
###################################

global_symbol_table = SymbolTable()
global_symbol_table.set("null",Number(0)) #if you write a null program return a '0'
global_symbol_table.set("true",Number(1)) #if you write a true program return a '1'
global_symbol_table.set("false",Number(0)) #if you write a false program return a '0'




def run(fn,text):
    #Generate tokens
    lexer = Lexer(fn,text)
    tokens,error = lexer.make_tokens()
    if error:
        return None,error
        
    #Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    context = Context("<Program>")
    context.symbol_table = global_symbol_table
    if ast.error:
        return None,ast.error
    interpreter = Interpreter()
    result = interpreter.visit(ast.node,context)
    
    return result.value,result.error
       
       
       
       





