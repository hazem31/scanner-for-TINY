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
        for toke in self.tokens:
            toke.Print()

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




f = open("scan.txt", "r")

sc = Scanner(f)
sc.get_all_tokens()