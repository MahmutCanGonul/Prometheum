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


KEYWORDS = ['var']

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
                tokens.append(Token(TT_EQ,pos_start=self.pos))
                self.advance()     
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
        
        
        elif tok.type in TT_LPAREN:
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
        
                
        return res.failure(InvalidSyntaxError(tok.pos_start,tok.pos_end,"Expected int, float, identifier! After the '+' or '-' or '*' or '/': "))
    
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
                
        
        node = res.register(self.bin_op(self.term,(TT_PLUS,TT_MINUS)))
        
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
        
        while self.current_tok.type in ops:
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
            
    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start,self.pos_end)
        copy.set_context(self.context)
        return copy
    
    
    
    def __repr__(self):
        return str(self.value)


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
        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start,node.pos_end))
   
    

####################################

  
###################################
       #RUN
###################################

global_symbol_table = SymbolTable()
global_symbol_table.set("null",Number(0))



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
       
       
       
       





