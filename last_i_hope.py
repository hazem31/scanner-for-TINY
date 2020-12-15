

from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz 2.44.1/bin'

dot = Digraph()

reserved=['if','then','else','end','repeat','until',
		'read','write','break','for','while',
		'int','float','char','bool','void','main',
		'return', 'endl', 'cout']

operators = [':=' , '<' , '>' , '=' , '+' , '-' , '*' , '/' , '[' , ']' , '(' , ')']

#TODO what do we consider -50 is it an operator then an num or a full num -50

class token:
    def __init__(self,type,value = "None"):
        self.type = type
        self.value = value
    def Print(self):
        print("token type is " + self.type)
        print("token value is " + self.value)
        print('end#############end')


class Scanner :

    def __init__(self,file):
        self.file = file
        #self.file_text = file.read()
        self.lines = []
        self.lines_without_comments = []
        self.tokens = []
        self.comments = []
        self.in_comment = False
        for line in self.file:
            self.lines.append(line.strip())
        self.line_num = 0
        self.total_num_of_lines = len(self.lines)
    def get_all_tokens(self):
        for line in self.lines:
            first = line.split()
            self.remove_all_comments()
            i = 0
            flag_of_semicolon = 0
            if ";" in first:
                flag_of_semicolon = 1
            while i < len(first):
                word = first[i]
                if self.check_comment(word):
                    i += 1
                    continue
                if '}' in word:
                    i += 1
                    continue
                if self.check_reserved(word):
                    self.tokens.append(token('reserved', word))
                    i += 1
                    continue
                if self.check_operator(word):
                    self.tokens.append(token('operator', word))
                    i += 1
                    continue

                if len(word) == 1:
                    if word.isdigit():
                        self.tokens.append(token('NUM', word))
                    if word.isalpha():
                        self.tokens.append(token('ID', word))
                    i += 1
                    continue
                if len(word) > 1:
                    temp_list = self.check_all(word)
                    if temp_list is not None:
                        for te in temp_list:
                            self.tokens.append(te)



                i += 1

            if flag_of_semicolon == 1:
                self.tokens.append(token('operator',';'))


    #TODO improve this fuction
    def check_comment(self,word):
        if self.in_comment == False:
            if '{' in word:
                # 1 means start of a comment and in a comment
                self.in_comment = True
        else:
            if '}' in word:
                self.in_comment = False
        return self.in_comment

    def check_reserved(self,word):
        if word in reserved:
            return True
        else:
            return False
    def check_operator(self,word):
        if word in operators:
            return True
        else:
            return False
    def remove_all_comments(self):
        pass


    def check_all(self,word):
        temp_list = []
        if ';' in word:
            word = self.case0(word)
        type = ''
        new_word = word
        while (len(word) > 0):
            if len(word) == 1:
                if self.check_operator(word):
                    temp_list.append(token('operator', word))
                elif word.isdigit():
                    temp_list.append(token('NUM', word))
                elif word.isalpha():
                    temp_list.append(token('ID', word))
                return temp_list
            if word[0].isalpha():
                type = 'ID'
                ID = word[0]
                for i in range(1, len(word)):
                    if word[i].isalpha() or word[i].isdigit():
                        ID += word[i]
                        continue
                    elif word[i] in operators or word[i] == ':':
                        new_word = word[i:]
                        break
                    else:
                        print('ERORR#########################')
                        print('ERORR#########################')
                temp_list.append(token(type, ID))
                if word == new_word:
                    return temp_list
                else:
                    word = new_word
            if word[0:2] == ':=':
                temp_list.append(token('operator', word[0:2]))
                if len(word) > 2:
                    word = word[2:]
                else:
                    return temp_list
            if word[0].isdigit():
                type = 'NUM'
                ID = word[0]
                new_word = word
                for i in range(1, len(word)):
                    if word[i].isdigit():
                        ID += word[i]
                        continue
                    elif word[i] in operators:
                        new_word = word[i:]
                        break
                    else:
                        print('ERORR#########################')
                        print('ERORR#########################')
                temp_list.append(token(type, ID))
                if word == new_word:
                    return temp_list
                else:
                    word = new_word
            if word[0] in operators:
                temp_list.append(token('operator', word[0]))
                if len(word) == 1:
                    return temp_list
                else:
                    word = word[1:]


    # if there is a (;) in word
    def case0(self,word):
        loca = word.find(';')
        new_word = word[:loca]
        return new_word

class Node:
    def __init__(self,text):
        self.text = text
        self.childs = []
        self.next = None
        self.shape = None
        self.prev = None

    def set_childs(self,y):
        try:
            assert isinstance(y, list)
            for i in y:
                self.childs.append(i)
        except:
            self.childs.append(y)

    def set_next(self, y):
        self.next = y



class Parser:
    def __init__(self,tokens):
        self.token_list = tokens
        self.index = 0
        self.token = self.token_list[0]
        self.current_Node = Node('start')
        self.current_Node.shape = 'b'
        self.Parse_tree = self.current_Node
        self.prev1 = None
        self.node_counter = 0
        # 0 for child 1 for next
        self.child_or_next = 0
    def check_token_end(self):
        if self.index == len(self.token_list):
            return True
        else:
            return False

    def next(self):
        if not self.check_token_end():
            self.index += 1
            self.token = self.token_list[self.index]


    def read_stat(self):
        self.node_counter += 1
        t = Node('read' + '$' + str(self.node_counter))
        t.shape = 'b'
        self.next()
        if self.token.type == "ID":
            self.node_counter += 1
            n = Node('ID ' + self.token.value + '$' + str(self.node_counter))
            n.shape = 'c'
            t.set_childs(n)
            self.child_or_next = 1
            self.next()
            return t

    def if_stat(self):
        self.node_counter += 1
        t = Node('if' + '$' + str(self.node_counter))
        t.shape = 'b'
        self.next()
        t.set_childs(self.exp())
        if self.token.value == "then":
            self.next()
        #check later
        t.set_childs(self.start_fun())
        if self.token.value == "else":
            self.next()
            t.set_childs(self.start_fun())
        if self.token.value == "end":
            self.next()
        return t



    def write_stat(self):
        self.node_counter += 1
        t = Node('write' + '$' + str(self.node_counter))
        t.shape = 'b'
        self.child_or_next = 0
        self.next()
        e = self.exp()
        t.set_childs(e)
        return t


    def exp(self):
        t = self.simple_exp()
        if self.token.value == '>' or self.token.value == '<' or self.token.value == '=':
            self.node_counter += 1
            p = Node('op ' + self.token.value + '$' + str(self.node_counter))
            p.shape = 'c'
            p.set_childs(t)
            t = p
            self.next()
            t.set_childs(self.simple_exp())
        return t

    def simple_exp(self):
        t = self.term()
        while self.token.value == '+' or self.token.value == '-':
            self.node_counter += 1
            p = Node('op ' + self.token.value + '$' + str(self.node_counter))
            p.shape = 'c'
            p.set_childs(t)
            t = p
            self.next()
            t.set_childs(self.term())
        return t




    def term(self):
        t1 = self.factor()
        while self.token.value == '*' or self.token.value == '/':
            self.node_counter += 1
            p1 = Node('op ' + self.token.value + '$' + str(self.node_counter))
            p1.shape = 'c'
            p1.set_childs(t1)
            t1 = p1
            self.next()
            t1.set_childs(self.factor())
            self.child_or_next = 0
        return t1


    def factor(self):
        if self.token.type == "operator" and self.token.value == '(':
            self.next()
            t = self.exp()
            if self.token.type == "operator" and self.token.value == ')':
                self.next()
            return t
        elif self.token.type == "NUM":
            self.node_counter += 1
            t = Node('NUM ' + self.token.value + '$' + str(self.node_counter))
            t.shape = 'c'
            self.prev1 = self.current_Node
            self.next()
            return t

        elif self.token.type == "ID":
            self.node_counter += 1
            t = Node('ID ' + self.token.value +'$' + str(self.node_counter))
            t.shape = 'c'
            self.prev1 = self.current_Node
            self.next()
            return t


    def repeat_stat(self):
        self.node_counter += 1
        t = Node('repeat' + '$' + str(self.node_counter))
        t.shape = 'b'
        self.next()
        t.set_childs(self.start_fun())
        if self.token.value == "until":
            self.next()
        t.set_childs(self.exp())
        return t

    def assign_stat(self):
        self.node_counter += 1
        t = Node('assign ' + self.token.value + '$' + str(self.node_counter))
        t.shape = 'b'
        self.next()
        if self.token.value == ":=":
            self.next()
        t.set_childs(self.exp())

        return t

    def start_fun(self):
        t = self.statement()
        p = t
        while self.token.value == ';':
            self.next()
            q = self.statement()
            if q == None:
                break
            else:
                if t == None:
                    t = p = q
                else:
                    p.set_next(q)
                    p = q
        return t
    def statement(self):
        if not self.check_token_end():
            self.token = self.token_list[self.index]
        else:
            return

        if self.token.type == "reserved" and self.token.value == "if":
            t = self.if_stat()
            return t

        elif self.token.type == "reserved" and self.token.value == "read":
            t = self.read_stat()

            return t
        elif self.token.type == "reserved" and self.token.value == "write":
            t = self.write_stat()
            return t

        elif self.token.type == "reserved" and self.token.value == "repeat":
            t = self.repeat_stat()
            return t

        elif self.token.type == "ID":
            t = self.assign_stat()
            return t


        else:
            self.index += 1


    def consume_token(self):
        if not self.check_token_end():
            self.token = self.token_list[self.index]
        else:
            return
        if self.token.type == "reserved":
            if self.token.value == 'read':
                self.node_counter += 1
                t = Node('read' + '$' + str(self.node_counter))
                t.shape = 'b'
                self.prev1 = self.current_Node
                if self.child_or_next == 1:
                    self.current_Node.next = t
                else:
                    self.current_Node.childs.append(t)
                self.current_Node = t
                if not self.check_token_end():
                    if self.token_list[self.index+1].type == "ID":
                        self.node_counter += 1
                        n = Node('ID '+ self.token_list[self.index+1].value + '$' + str(self.node_counter))
                        n.shape = 'c'
                        n.prev = self.current_Node
                        self.current_Node.childs.append(n)
                        self.current_Node = t
                        self.child_or_next = 1
                        self.index += 2

            if self.token.value == 'if':
                self.node_counter += 1
                t = Node('if' + '$' + str(self.node_counter))
                t.shape = 'b'
                self.prev1 = self.current_Node
                if self.child_or_next == 1:
                    self.current_Node.next = t
                else:
                    self.current_Node.childs.append(t)
                self.current_Node = t
                self.child_or_next = 0
                self.exp1()

    def exp1(self):
        index_of_compa  = 0
        index_of_then = 0
        for i in range(self.index,len(self.token_list)):
            if self.token_list[i].type == "reserved":
                if self.token_list[i].value == "then":
                    index_of_then = i
                    break
        for i in range(self.index,len(self.token_list)):
            if self.token_list[i].type == "operator":
                if self.token_list[i].value == "<" or self.token_list[i].value == ">" or self.token_list[i].value == "=" :
                    index_of_compa = i
                    break

        self.token = self.token_list[index_of_compa]
        self.node_counter += 1
        t = Node('op  ' + self.token.value + '$' + str(self.node_counter))
        t.shape = 'c'
        self.prev1 = self.current_Node
        if self.child_or_next == 1:
            self.current_Node.next = t
        else:
            self.current_Node.childs.append(t)
        self.current_Node = t
        ##self.child_or_next = 0
        self.token = self.token_list[index_of_compa-1]
        left =self.token
        if left.type == 'ID':
            self.node_counter += 1
            t1 = Node('ID ' +  self.token.value + '$' + str(self.node_counter))
            t1.shape = 'c'
            self.current_Node.childs.append(t1)
        elif left.type == "NUM":
            self.node_counter += 1
            t1 = Node('NUM ' + self.token.value + '$' + str(self.node_counter))
            t1.shape = 'c'
            self.current_Node.childs.append(t1)
        self.token = self.token_list[index_of_compa + 1]
        right = self.token
        if right.type == 'ID':
            self.node_counter += 1
            t2 = Node('ID ' + self.token.value + '$' + str(self.node_counter))
            t2.shape = 'c'
            self.current_Node.childs.append(t2)
        elif right.type == "NUM":
            self.node_counter += 1
            t2 = Node('NUM ' + self.token.value + '$' + str(self.node_counter))
            t2.shape = 'c'
            self.current_Node.childs.append(t2)
        self.current_Node = self.prev1
        self.index = index_of_then+1




    def draw(self,node):
        if node.shape == 'b' :
            dot.attr('node', shape='box')
        else:
            dot.attr('node', shape='circle')
        if node.text == 'start':
            dot.node(node.text, node.text)
        else:
            dot.node(node.text,node.text[0:node.text.index('$')])
        for nd in node.childs:
            if nd:
                self.draw(nd)
                dot.edge(node.text,nd.text , label='child')

        if node.next:
            self.draw(node.next)
            dot.edge(node.text,node.next.text,constraint='false')


f = open("scan.txt", "r")

sc = Scanner(f)
sc.get_all_tokens()

# imp_list = []
# imp_list1 = []
# for toke in sc.tokens:
#     if toke.type == 'reserved':
#         imp_list.append(toke.value)
#         imp_list1.append(" ")
#     elif toke.type == 'ID':
#         imp_list.append('identifier')
#         imp_list1.append(toke.value)
#     elif toke.type == 'NUM':
#         imp_list.append('number')
#         imp_list1.append(toke.value)
#     else:
#         imp_list.append(toke.value)
#         imp_list1.append(toke.value)
#
#
# for i in range(len(imp_list)):
#     print(imp_list[i])
#     print(imp_list1[i])
#     print("#######################3")


p = Parser(sc.tokens)
v = p.start_fun()
p.draw(v)
dot.format = 'png'
dot.view()
