

from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz 2.44.1/bin'

dot = Digraph()

reserved=['if','then','else','end','repeat','until',
		'read','write','break','for','while',
		'int','float','char','bool','void','main',
		'return', 'endl', 'cout']

operators = [':=' , '<' , '>' , '=' , '+' , '-' , '*' , '/' , '[' , ']']

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
        # for toke in self.tokens:
        #     toke.Print()

        # first = self.lines[3]
        # first = first.split()
        # self.remove_all_comments()
        # i = 0
        # while i < len(first):
        #     word = first[i]
        #     if self.check_comment(word):
        #         i += 1
        #         continue
        #     if '}' in word:
        #         i += 1
        #         continue
        #     if self.check_reserved(word):
        #         self.tokens.append(token('reserved',word))
        #         i += 1
        #         continue
        #     if self.check_operator(word):
        #         self.tokens.append(token('operator' , word))
        #         i += 1
        #         continue
        #
        #     if len(word) == 1:
        #         if word.isdigit():
        #             self.tokens.append(token('NUM', word))
        #         if word.isalpha():
        #             self.tokens.append(token('ID', word))
        #         i += 1
        #         continue
        #     if len(word) > 1:
        #         temp_list = self.check_all(word)
        #         print(temp_list)
        #         if temp_list is not None:
        #             for te in temp_list:
        #                 self.tokens.append(te)
        #
        #
        #     i += 1
        # for toke in self.tokens:
        #     toke.Print()


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
                    # if len(word) == 1:
                    #     if self.check_operator(word):
                    #         temp_list.append(token('operator', word))
                    #         return temp_list
                    # else:
                    #     if word[0] in operators or word[0:2] == ':=':
                    #         if word[0:2] == ":=":
                    #             temp_list.
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
                    # if len(word) == 1:
                    #     if self.check_operator(word):
                    #         temp_list.append(token('operator', word))
                    #         return temp_list
                    # else:
                    #     if word[0] in operators or word[0:2] == ':=':
                    #         if word[0:2] == ":=":
                    #             temp_list.
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
                if self.child_or_next == 0:
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
                self.exp()
    def exp(self):
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
            self.draw(nd)
            dot.edge(node.text,nd.text)

        if node.next:
            self.draw(node.next)
            dot.edge(node.text,node.next.text,constraint='false')





#
# class Node:
#     def __init__(self, t, c, s):
#         self.token_value = t
#         self.code_value = c
#         self.shape = s
#         self.children = []
#         self.sibling = None
#         self.index = None
#
#     def set_children(self, y):
#         try:
#             assert isinstance(y, list)
#             for i in y:
#                 self.children.append(i)
#         except:
#             self.children.append(y)
#
#     def set_sibling(self, y):
#         self.sibling = y

#
# class Parser:
#     nodes_table = {}
#     tmp_index = 0
#     edges_table = []
#
#     def __init__(self):
#         self.token = str
#         self.tokens_list = ['identifier', ':=',
#                             'identifier', '+', 'number']
#         self.code_list = ['x', ':=', 'x', '+', '5']
#         self.tmp_index = 0
#         self.token = self.tokens_list[self.tmp_index]
#         self.parse_tree = None
#         self.nodes_table = None
#         self.edges_table = None
#         self.same_rank_nodes = []
#
#     def set_tokens_list_and_code_list(self, x, y):
#         self.code_list = y
#         self.tokens_list = x
#         self.tmp_index = 0
#         self.token = self.tokens_list[self.tmp_index]
#
#     def next_token(self):
#         if(self.tmp_index == len(self.tokens_list)-1):
#             return False  # we have reachd the end of the list
#         self.tmp_index = self.tmp_index + 1
#         self.token = self.tokens_list[self.tmp_index]
#         return True
#
#     def match(self, x):
#         if self.token == x:
#             self.next_token()
#             return True
#         else:
#             raise ValueError('Token Mismatch', self.token)
#
#     def statement(self):
#         if self.token == 'if':
#             t = self.if_stmt()
#             return t
#         elif self.token == 'repeat':
#             t = self.repeat_stmt()
#             return t
#         elif self.token == 'identifier':
#             t = self.assign_stmt()
#             return t
#         elif self.token == 'read':
#             t = self.read_stmt()
#             return t
#         elif self.token == 'write':
#             t = self.write_stmt()
#             return t
#         else:
#             raise ValueError('SyntaxError', self.token)
#
#     def stmt_sequence(self):
#         t = self.statement()
#         p = t
#         while self.token == ';':
#             q = Node(None, None, None)
#             self.match(';')
#             q = self.statement()
#             if q == None:
#                 break
#             else:
#                 if t == None:
#                     t = p = q
#                 else:
#                     p.set_sibling(q)
#                     p = q
#         return t
#
#     def factor(self):
#         if self.token == '(':
#             self.match('(')
#             t = self.exp()
#             self.match(')')
#         elif self.token == 'number':
#             t = Node(
#                 'CONSTANT', '(' + self.code_list[self.tmp_index] + ')', 'o')
#             self.match('number')
#         elif self.token == 'identifier':
#             t = Node('IDENTIFIER',
#                      '(' + self.code_list[self.tmp_index] + ')', 'o')
#             self.match('identifier')
#         else:
#             raise ValueError('SyntaxError', self.token)
#             return False
#         return t
#
#     def term(self):
#         t = self.factor()
#         while self.token == '*' or self.token == '/':
#             p = Node(
#                 'OPERATOR', '(' + self.code_list[self.tmp_index] + ')', 'o')
#             p.set_children(t)
#             t = p
#             self.mulop()
#             p.set_children(self.factor())
#         return t
#
#     def simple_exp(self):
#         t = self.term()
#         while self.token == '+' or self.token == '-':
#             p = Node(
#                 'OPERATOR', '(' + self.code_list[self.tmp_index] + ')', 'o')
#             p.set_children(t)
#             t = p
#             self.addop()
#             t.set_children(self.term())
#         return t
#
#     def exp(self):
#         t = self.simple_exp()
#         if self.token == '<' or self.token == '=' or self.token == '>':
#             p = Node(
#                 'OPERATOR', '(' + self.code_list[self.tmp_index] + ')', 'o')
#             p.set_children(t)
#             t = p
#             self.comparison_op()
#             t.set_children(self.simple_exp())
#         return t
#
#     def if_stmt(self):
#         t = Node('IF', '', 's')
#         if self.token == 'if':
#             self.match('if')
#             t.set_children(self.exp())
#             self.match('then')
#             t.set_children(self.stmt_sequence())
#             if self.token == 'else':
#                 self.match('else')
#                 t.set_children(self.stmt_sequence())
#             self.match('end')
#         return t
#
#     def comparison_op(self):
#         if self.token == '<':
#             self.match('<')
#         elif self.token == '=':
#             self.match('=')
#         elif self.token == '>':
#             self.match('>')
#
#     def addop(self):
#         if self.token == '+':
#             self.match('+')
#         elif self.token == '-':
#             self.match('-')
#
#     def mulop(self):
#         if self.token == '*':
#             self.match('*')
#         elif self.token == '/':
#             self.match('/')
#
#     def repeat_stmt(self):
#         t = Node('REPEAT', '', 's')
#         if self.token == 'repeat':
#             self.match('repeat')
#             t.set_children(self.stmt_sequence())
#             self.match('until')
#             t.set_children(self.exp())
#         return t
#
#
#     def assign_stmt(self):
#         t = Node('ASSIGN', '(' + self.code_list[self.tmp_index] + ')', 's')
#         self.match('identifier')
#         self.match(':=')
#         t.set_children(self.exp())
#         return t
#
#     def read_stmt(self):
#         t = Node('READ', '(' + self.code_list[self.tmp_index+1] + ')', 's')
#         self.match('read')
#         self.match('identifier')
#         return t
#
#     def write_stmt(self):
#         t = Node('WRITE', '', 's')
#         self.match('write')
#         t.set_children(self.exp())
#         return t
#
#
#     def create_nodes_table(self, args=None):
#         if args == None:
#             self.parse_tree.index = Parser.tmp_index
#             Parser.nodes_table.update(
#                 {Parser.tmp_index: [self.parse_tree.token_value, self.parse_tree.code_value, self.parse_tree.shape]})
#             Parser.tmp_index = Parser.tmp_index+1
#             if len(self.parse_tree.children) != 0:
#                 for i in self.parse_tree.children:
#                     self.create_nodes_table(i)
#             if self.parse_tree.sibling != None:
#                 self.create_nodes_table(self.parse_tree.sibling)
#         else:
#             args.index = Parser.tmp_index
#             Parser.nodes_table.update(
#                 {Parser.tmp_index: [args.token_value, args.code_value, args.shape]})
#             Parser.tmp_index = Parser.tmp_index+1
#             if len(args.children) != 0:
#                 for i in args.children:
#                     self.create_nodes_table(i)
#             if args.sibling != None:
#                 self.create_nodes_table(args.sibling)
#
#     def create_edges_table(self, args=None):
#         if args == None:
#             if len(self.parse_tree.children) != 0:
#                 for i in self.parse_tree.children:
#                     Parser.edges_table.append((self.parse_tree.index, i.index))
#                 for j in self.parse_tree.children:
#                     self.create_edges_table(j)
#             if self.parse_tree.sibling != None:
#                 Parser.edges_table.append(
#                     (self.parse_tree.index, self.parse_tree.sibling.index))
#                 self.same_rank_nodes.append(
#                     [self.parse_tree.index, self.parse_tree.sibling.index])
#                 self.create_edges_table(self.parse_tree.sibling)
#         else:
#             if len(args.children) != 0:
#                 for i in args.children:
#                     Parser.edges_table.append((args.index, i.index))
#                 for j in args.children:
#                     self.create_edges_table(j)
#             if args.sibling != None:
#                 Parser.edges_table.append((args.index, args.sibling.index))
#                 self.same_rank_nodes.append([args.index, args.sibling.index])
#                 self.create_edges_table(args.sibling)
#
#     def run(self):
#         self.parse_tree = self.stmt_sequence()  # create parse tree
#         self.create_nodes_table()  # create nodes_table
#         self.create_edges_table()  # create edges_table
#         self.edges_table = Parser.edges_table  # save edges_table
#         self.nodes_table = Parser.nodes_table  # save nodes_table
#         if self.tmp_index == len(self.tokens_list)-1:
#             print('success')
#         elif self.tmp_index < len(self.tokens_list):
#             raise ValueError('SyntaxError', self.token)
#
#     def clear_tables(self):
#         self.nodes_table.clear()
#         self.edges_table.clear()

# p = Parser()
# p.run()


f = open("scan.txt", "r")

sc = Scanner(f)
sc.get_all_tokens()

imp_list = []
imp_list1 = []
for toke in sc.tokens:
    if toke.type == 'reserved':
        imp_list.append(toke.value)
        imp_list1.append(" ")
    elif toke.type == 'ID':
        imp_list.append('identifier')
        imp_list1.append(toke.value)
    elif toke.type == 'NUM':
        imp_list.append('number')
        imp_list1.append(toke.value)
    else:
        imp_list.append(toke.value)
        imp_list1.append(toke.value)


for i in range(len(imp_list)):
    print(imp_list[i])
    print(imp_list1[i])
    print("#######################3")
#
# p1 = Parser()
# p1.set_tokens_list_and_code_list(imp_list,imp_list1)
# p1.run()
#

p = Parser(sc.tokens)
p.consume_token()
p.consume_token()
p.draw(p.Parse_tree)


# for imp in imp_list:
#     print(imp)

# ps = Parser(sc.tokens)
# ps.consume_token()
# ps.draw(ps.Parse_tree)
dot.format = 'png'
dot.view()
# dot = Digraph()
# # Add nodes 1 and 2
#
#
#
# dot.node('1','a7a\n hello')
# dot.node('2')
#
#
# # Add edge between 1 and 2
# dot.edge('1','2')
#
# # Visualize the graph
#
# dot.format = 'png'
#
# dot.render('test-output/round-table.gv' , view=True)
#
# print('working')
