class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def peek(self, char):
        if self.pos+1 < len(self.text):
            if self.text[self.pos+1] == char:
                return True
        return False

    def peek_back(self, char):
        if self.pos-1 > -1:
            if self.text[self.pos-1] == char:
                return True
        return False

    def advanceable(self):
        if self.pos < len(self.text):
            return True
        return False

    # refactor this mess
    def tokenize(self):
        # whitespace and commas
        ignored_tokens = " ,	\t\n\r"
        special_chars = "[]{}()'`~^@"
        # return a list of string tokens
        tokens = []
        curr_tok = ""
        while self.advanceable():
            if self.text[self.pos] in ignored_tokens:
                self.pos += 1
                curr_tok = ""
                continue
            elif self.text[self.pos] == "~" and self.peek("@"):
                tokens.append("~@")
                self.pos += 2
                curr_tok = ""
                continue
            elif self.text[self.pos] in special_chars:
                tokens.append(self.text[self.pos])
                curr_tok = ""
                self.pos += 1
                continue
            elif self.text[self.pos] == "\"":
                curr_tok += self.text[self.pos]
                self.pos += 1
                while self.advanceable() and self.text[self.pos] != "\"" or self.peek_back == "\\":
                    curr_tok += self.text[self.pos]
                    self.pos += 1
                curr_tok += self.text[self.pos]
                temp_str = "\"" + curr_tok[1:len(curr_tok)-1] + "\""
                tokens.append(temp_str)
                self.pos += 1
                curr_tok = ""
                continue
            elif self.text[self.pos] == ";":
                while self.advanceable() and self.text[self.pos] != "\n":
                    curr_tok += self.text[self.pos]
                    self.pos += 1
                tokens.append(curr_tok)
                self.pos += 1
                continue
            else:
                while self.advanceable() and not self.text[self.pos] in "[]{}()'`~^@\n" \
                        and not self.text[self.pos] in ignored_tokens:
                    curr_tok += self.text[self.pos]
                    self.pos += 1
                tokens.append(curr_tok)
                curr_tok = ""
                continue
            cur_tok = ""
        return tokens