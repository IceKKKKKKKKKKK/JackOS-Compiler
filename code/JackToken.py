import os
class lexi:
    reservedWords = {'class': 'class', 'constructor': 'constructor', 'function': 'function', 'method': 'method', 'field': 'field', 'static': 'static', 'var': 'var', 'int': 'int', 'char': 'char', 'boolean': 'boolean', 'void': 'void', 'true': 'true', 'false': 'false', 'null': 'null', 'this': 'this', 'let': 'let', 'do': 'do', 'if': 'if', 'else': 'else', 'while': 'while', 'return': 'return'}
    tokenTypes = {'symbol': 'symbol', 'stringConstant': 'stringConstant', 'integerConstant': 'integerConstant', 'keyword': 'keyword', 'identifier': 'identifier'}
    
    def __init__(self, content, category, reserved=None):
        assert category is None or category in self.tokenTypes
        assert reserved is None or reserved in self.reservedWords

        self.content = content
        self.category = category
        self.reserved = reserved

class JackToken:
    charSymbols = '{[]}().,;+-*/&!|<>=~'
    controlKeywords = 'class, constructor, function, method, field, static, var, int, char, boolean, void, true, false, null, this, let, do, if, else, while, return'.split(', ')
    quoteChar = '"'

    def __init__(self, sourceFile):
        self.inCommentBlock = False
        self.activeToken = None
        self.previousToken = None
        self.sourceFile = sourceFile
        self.currentLine = ''
    
    def hasAdditionalTokens(self) -> bool:
        return self._retrieveNextToken(False) is not None
    
    def progress(self) -> lexi:
        if not self.hasAdditionalTokens():
            raise RuntimeError('No more tokens to process')
        self.previousToken = self.activeToken
        self.activeToken = self._retrieveNextToken()
        return self.activeToken

    def getCurrentToken(self):
        return self.activeToken
    
    def getPreviousToken(self):
        return self.previousToken
    
    def lookAheadToken(self):
        return self._retrieveNextToken(False)

    def _retrieveNextToken(self, updateLine=True):
        self.currentLine = self._sanitizeLine(self.currentLine)
        while not self.currentLine:
            line = self.sourceFile.readline()
            if not line:
                return None
            self.currentLine = self._sanitizeLine(line)
        
        token, tokenLength = self._parseToken()
        if updateLine:
            self.currentLine = self.currentLine[tokenLength:]
        return token
    

    
    def _parseToken(self):
        firstChar = self.currentLine[0]

        if firstChar in self.charSymbols:
            return (lexi(firstChar, lexi.tokenTypes['symbol']), 1)
        elif firstChar == self.quoteChar:
            endQuoteIndex = self.currentLine.find(self.quoteChar, 1)
            stringContent = self.currentLine[1:endQuoteIndex]
            # Handle character after the string constant
            nextCharIndex = endQuoteIndex + 1
            if nextCharIndex < len(self.currentLine):
                nextChar = self.currentLine[nextCharIndex]
                if nextChar in self.charSymbols or nextChar == ')':
                    return (lexi(stringContent, lexi.tokenTypes['stringConstant']), nextCharIndex)
            return (lexi(stringContent, lexi.tokenTypes['stringConstant']), nextCharIndex)
        else:
            for i, char in enumerate(self.currentLine):
                if char in self.charSymbols or char.isspace():
                    if i == 0:
                       #if white space, then continue 
                        continue
                    else:
                        # return the token before symbol
                        tokenString = self.currentLine[:i].strip()
                        tokenType, tokenValue = self._determineTokenType(tokenString)
                        return (lexi(tokenString, tokenType, tokenValue), i)

            # no syntax symbols found, return entire line
            tokenString = self.currentLine.split(maxsplit=1)[0].strip()
            tokenType, tokenValue = self._determineTokenType(tokenString)
            return (lexi(tokenString, tokenType, tokenValue), len(tokenString))


    
    def _determineTokenType(self, tokenString):
        if tokenString.isdigit():
            return (lexi.tokenTypes['integerConstant'], None)
        elif tokenString in self.controlKeywords:
            return (lexi.tokenTypes['keyword'], lexi.reservedWords[tokenString])
        else:
            return (lexi.tokenTypes['identifier'], None)

    def _sanitizeLine(self, line):
        line = line.strip()
        if self.inCommentBlock:
            endCommentPos = line.find('*/')
            if endCommentPos == -1:
                return ''
            line = line[endCommentPos + 2:]
            self.inCommentBlock = False
        while '/*' in line:
            startCommentPos, endCommentPos = line.find('/*'), line.find('*/')
            if endCommentPos == -1:
                self.inCommentBlock = True
                return line[:startCommentPos]
            line = line[:startCommentPos] + line[endCommentPos + 2:]
        if '//' in line:
            line = line[:line.index('//')]
        return line
    
    def process_path(self, path):
        if os.path.isdir(path):
            for file_name in os.listdir(path):
                if file_name.endswith('.jack'):
                    full_path = os.path.join(path, file_name)
        elif os.path.isfile(path) and path.endswith('.jack'):
            full_path = path
        else:
            print("exception")
        return full_path
        
