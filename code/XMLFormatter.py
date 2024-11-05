from JackToken import lexi
import JackToken
import os
from VMCode import VMCode 
from VMCode import symbol 
class functionParameter:
    def __init__(self, xml_writer, tokenizer):
        assert isinstance(xml_writer, VMCode)
        assert isinstance(tokenizer, JackToken.JackToken)
        self.parameterList = []
        tokenizer.progress()
        if tokenizer.lookAheadToken().content != ')':
            self.parameterList.append((tokenizer.progress().content, tokenizer.progress().content))
        while tokenizer.lookAheadToken().content != ')':
            tokenizer.progress()
            self.parameterList.append((tokenizer.progress().content, tokenizer.progress().content))
        tokenizer.progress()

class localVariable:
    def __init__(self, xml_writer, tokenizer):
        assert isinstance(xml_writer, VMCode)
        assert isinstance(tokenizer, JackToken.JackToken)
        self.localVariableList = []
        
        tokenizer.progress()
        dataTYpe = tokenizer.progress().content
        
        xml_writer.subScope.define(dataTYpe, tokenizer.progress().content, 'local')
        self.localVariableNumber = 1
        while tokenizer.lookAheadToken().content != ';':
            tokenizer.progress()
            xml_writer.subScope.define(dataTYpe, tokenizer.progress().content, 'local')
            self.localVariableNumber += 1
        tokenizer.progress()

class XMLFormatter:
    space = '  '
    classVariable = []
    subroutineDecs = []
    VariableTriggers = ['static', 'field']

    vmSegment = ['static', 'this']

    expressionGlobalCounter = 0

    compilationStatementTrigger = ['let', 'if', 'while', 'do', 'return']
    VarTriggers = ['var']
    ParameterListTriggers = ['(']
    SubroutineBodyTriggers  = ['{']
    subroutineCallTriggers = ['(', '.']
    SubroutineDecTriggers = ['constructor', 'function', 'method']   
    operationTriggers = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
    vmOperation = ['add', 'sub', 'call Math.multiply 2', 'call Math.divide 2', 'and', 'or', 'lt', 'gt', 'eq']
    def __init__(self, output):
        self.output = output
        self.indentationNumber = 0
        
    
    def put(self, content):
       
        self.output.write(content)
    
    # XML related methods:
    def increaseIndent(self, step=1):
        self.indentationNumber += step

    def addTokenXml(self, tokenObj, addIndent=0):
        if not isinstance(tokenObj, lexi):
            raise TypeError('Expected a Token object')
        self.put(self.indentationNumber * self.space + '<'+tokenObj.category+'> ' +self._safeXml(tokenObj.content) +' </'+tokenObj.category+'>\n')
        
        return tokenObj
    
    def addXmlElement(self, tag, end=False, stepIndent=2):
        #change of indentation
        if end: self.increaseIndent(-stepIndent)
        self.put(self.indentationNumber * self.space + ('</' if end else '<') + tag + '>\n')
        if not end: self.increaseIndent(stepIndent)
        return tag

    def _safeXml(self, text):
        if not isinstance(text, str):
            raise TypeError('Text must be a string')
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\'', '&apos;').replace('"', '&quot;')\
        
    def process_file(self, file_path):
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file_name = os.path.join(os.path.dirname(file_path), base_name + ".vm")
        
        with open(file_path, 'r') as file:
            tokenizer = JackToken.JackToken(file)
            with open(output_file_name, 'w') as xml_file:
                xml_writer = VMCode(xml_file)
                xml_writer.scope = symbol()
                #if this is a class, then compile class 
                def compileClass():
                    def compileClassVarDec():
                        objKind = self.vmSegment[self.VariableTriggers.index(tokenizer.progress().content)]
                        objType = tokenizer.progress().content
                        #define logic:: type, name, kind 
                        xml_writer.scope.define(objType, tokenizer.progress().content, objKind)

                        #xml_writer.addXmlElement('classVarDec')
                     
                        while tokenizer.lookAheadToken().content != ';':
                            #skip , symbol
                            tokenizer.progress()
                             #define logic:: type, name, kind 
                            xml_writer.scope.define(objType, tokenizer.progress().content, objKind)
                        #write ; symbol
                        tokenizer.progress()
                        #xml_writer.addXmlElement('classVarDec', end=True)

                    def compileSubroutine():
                        #subroutineDec
                        #xml_writer.addXmlElement('subroutineDec')

                        xml_writer.subScope = symbol()

                        #constructor, function, method
                        triggerWord = tokenizer.progress().content
                        
                        isMethod = False
                        isConstructor = False
                       
                        if triggerWord == 'method':
                            isMethod = True
                       
                        if triggerWord == 'constructor':
                            isConstructor = True
                        #write constructor, function, method   
                        #skip return type
                        returnType = tokenizer.progress().content
                        #write subroutine name
                        functionName = tokenizer.progress().content
                        if isMethod:
                            xml_writer.subScope.define('body', 'this', 'argument')
                        #write constructor, function, method

                        for dataType, name in functionParameter(xml_writer, tokenizer).parameterList:
                             xml_writer.subScope.define(dataType, name, 'argument')
                        #write { symbol
                        tokenizer.progress()
                        #write subroutineBody
                        localVariableCount = 0

                        while tokenizer.lookAheadToken().content in self.VarTriggers:
                            #write varDec !!!!!!!!!!
                            localVariableCount += localVariable(xml_writer, tokenizer).localVariableNumber
                        #write statements
                        xml_writer.writeFunction(f'{xml_writer.name}.{functionName}', localVariableCount)

                       

                        if isConstructor:
                            xml_writer.writePush('constant', xml_writer.scope.varCount('this'))
                            xml_writer.writeCall('Memory.alloc', 1)
                            xml_writer.writePop('pointer', 0)
                        elif isMethod:
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!")
                            xml_writer.writePush('argument', 0)
                            xml_writer.writePop('pointer', 0)

                        

                        
                        #parameter list
                        
                        #subroutine body
                        
                        
                        def callMethod(currentToken=None):
                            isMethodCall = False
                            isClassMethod = False
                            methodName = ''
                            print(currentToken == None)
                            if currentToken == None: 
                                methodName = tokenizer.progress().content
                            else: 
                                methodName = tokenizer.getCurrentToken().content
                            print(methodName)
                            isMethodCall = xml_writer.searchThrName(methodName) != None
                        
                                # ?
                            subroutineName = '.'
                            if tokenizer.lookAheadToken().content == '.':
                                # .
                                tokenizer.progress()
                                # subroutineName
                                subroutineName += tokenizer.progress().content
                            else:
                                subroutineName = ''
                                isClassMethod = True
                                xml_writer.writePush('pointer', 0)
                            # (
                            tokenizer.progress()
                            # expressionList
                            print(isMethodCall, isClassMethod)
                            if isMethodCall:
                                
                                methodCall1 = xml_writer.searchThrName(methodName)
                                #???????????????????????????
                                xml_writer.writePush(methodCall1["kind"], (methodCall1["index"]))
                                print(methodCall1["kind"], (methodCall1["index"]))
                                
                            expressionList()
                            
                            if isClassMethod:
                                xml_writer.writeCall(f'{xml_writer.name}.{methodName}', self.expressionGlobalCounter + 1)
                            elif not isMethodCall:
                                xml_writer.writeCall(f'{methodName}{subroutineName}', self.expressionGlobalCounter)
                            else:
                                xml_writer.writeCall(f'{xml_writer.searchThrName(methodName)["dataType"]}{subroutineName}', self.expressionGlobalCounter +1)
                            # )
                            tokenizer.progress()
                        def term():
                                # xml_writer.addXmlElement('term')
                                # Update and get the current token from the tokenizer
                            currentToken = tokenizer.progress()

                            # Check if the current token is an integer constant
                            isInt = currentToken.category == 'integerConstant'

                           
                            isString = currentToken.category == 'stringConstant'

                            # Check if the current token is one of the specific keywords ('true', 'false', 'null', 'this')
                            isKeyword = (currentToken.content in ['true', 'false', 'null', 'this'])

                            # Check if the current token indicates the start of a subroutine call
                            isSubCall = (currentToken.category == 'identifier' and tokenizer.lookAheadToken().content in self.subroutineCallTriggers)

                            # Check if the current token is a variable name (excluding the case of a subroutine call)
                            isVarName = (currentToken.category == 'identifier' and not isSubCall)

                         
                            isNext = (currentToken.content == '(')

                            # Check if the current token is a unary operator ('-' or '~')
                            isUnary = (currentToken.content in ['-', '~'])

                            # Execute different actions based on the type of token
                            if isInt:
                                # For integers, generate a command to push the constant onto the stack
                                xml_writer.writePush('constant', currentToken.content)
                            elif isKeyword:
                                # For keywords, generate specific VM code
                                if currentToken.content in ['null', 'false']:
                                    xml_writer.writePush('constant', 0)
                                elif currentToken.content == 'true':
                                    xml_writer.writePush('constant', 1)
                                    xml_writer.writeArithmetic('neg')  # true is processed as -1
                                else:
                                    # For the 'this' keyword, push the this pointer
                                    xml_writer.writePush('pointer', 0)
                            elif isString:
                                # For strings, first create a new String object, then append each character
                                string = tokenizer.getCurrentToken().content
                                xml_writer.writePush('constant', len(string))  # Length of the string
                                xml_writer.writeCall('String.new', 1)  # Create a String object
                                for char in string:
                                    xml_writer.writePush('constant', ord(char))  # ASCII value of the character
                                    xml_writer.writeCall('String.appendChar', 2)  # Append the character
                            elif isVarName:
                                # For variables, find the variable in the symbol table and push it onto the stack
                                var = xml_writer.searchThrName(tokenizer.getCurrentToken().content)
                                xml_writer.writePush(var["kind"], var["index"])
                                if tokenizer.lookAheadToken().content == '[':
                                    # Handle array elements
                                    tokenizer.progress()
                                    expression()
                                    xml_writer.writeArithmetic('add')
                                    xml_writer.writePop('pointer', 1)
                                    xml_writer.writePush('that', 0)
                                    tokenizer.progress()
                            elif isSubCall:
                                # Handle subroutine calls
                                callMethod(currentToken)
                            elif isNext:
                                # Handle expressions inside parentheses
                                tokenizer.getCurrentToken()
                                expression()
                                tokenizer.progress()
                            elif isUnary:
                                # Handle unary operations
                                trigger1 = ['-', '~']
                                trigger2 = ['neg', 'not']
                                unaryOperation = trigger2[trigger1.index(currentToken.content)]
                                term()
                                xml_writer.writeArithmetic(unaryOperation)

                        def expression():
                                # xml_writer.addXmlElement('expression')
                                term()
                                while tokenizer.lookAheadToken().content in self.operationTriggers:

                                    vmparse = self.vmOperation[self.operationTriggers.index(tokenizer.progress().content)]
                                    
                                    term()
                                    xml_writer.writeArithmetic(vmparse)
                                # xml_writer.addXmlElement('expression', end=True)
                            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        def expressionList():
                            self.expressionGlobalCounter = 0
                            # xml_writer.addXmlElement('expressionList')
                            if tokenizer.lookAheadToken().content != ')':
                                expression()
                                self.expressionGlobalCounter += 1
                                while tokenizer.lookAheadToken().content == ',':
                                    tokenizer.progress()
                                    expression()
                                    self.expressionGlobalCounter += 1
                            # xml_writer.addXmlElement('expressionList', end=True)
                        # def subroutineBody():
                        #     def compileVarDec():
                        #             xml_writer.addXmlElement('varDec')
                        #             #write var keyword
                                   
                        #             xml_writer.addTokenXml(tokenizer.progress())
                        #             #write type
                                   
                        #             xml_writer.addTokenXml(tokenizer.progress())
                        #             #write varName
                        #             xml_writer.addTokenXml(tokenizer.progress())
                                    
                        #             while  tokenizer.lookAheadToken().content != ';':
                        #                     #write , symbol
                                          
                        #                     xml_writer.addTokenXml(tokenizer.progress())
                        #                     #write varName
                            
                        #                     xml_writer.addTokenXml(tokenizer.progress())
                            
                        #             #write ; symbol
                                    
                        #             xml_writer.addTokenXml(tokenizer.progress())
                        #             xml_writer.addXmlElement('varDec', end=True)
                            
                       
                           
                            
                                
                        #     #subroutineBody begins
                        #     xml_writer.addXmlElement('subroutineBody')
                        #     #write { symbol
                        #     xml_writer.addTokenXml(tokenizer.progress())

                        #     #write varDec if there is any var trigger

                            # while tokenizer.lookAheadToken().content in self.VarTriggers:
                                
                            #     compileVarDec()
                            #write statements
                        def compileStatements():
                                def compileLet():
                                    # xml_writer.addXmlElement('letStatement')
                                    #write let keyword
                                    tokenizer.progress()
                                    #write variable name
                                    letVarName = xml_writer.searchThrName(tokenizer.progress().content)
                                   
                                    #check array
                                    containedArray = False
                                    arrayExpression = None

                                    #process array !!!!!!!!!!!!!!!!!!!!!!! NEED IMPLEMENTATION
                                    if(tokenizer.lookAheadToken().content == '['):
                                        #write [ symbol
                                        xml_writer.writePush(letVarName['kind'], letVarName['index'])
                                        
                                        #skip next
                                        tokenizer.progress()
                                        #!!!!!!!!!!!! need implementation
                                        #write expression
                                        expression()
                                        #write ] symbol
                                        tokenizer.progress()
                                        xml_writer.writeArithmetic('add')
                                        containedArray = True
                                        xml_writer.writePop('temp', 0)
                                    #write = symbol
                                    tokenizer.progress()
                                    #write expression
                                    expression()
                                    
                                    
                                    if containedArray:
                                        xml_writer.writePush('temp', 0)
                                        xml_writer.writePop('pointer', 1)
                                        xml_writer.writePop('that', 0)
                                    else:
                                        xml_writer.writePop(letVarName['kind'], letVarName['index'])
                                    #write ; symbol
                                    tokenizer.progress()

                                def compileIf():
                                    # xml_writer.addXmlElement('ifStatement')
                                    #write if keyword
                                    tokenizer.progress()
                                    #write ( symbol
                                    tokenizer.progress()
                                    #write expression
                                    expression()
                                    #write ) symbol
                                    xml_writer.writeArithmetic('not')
                                    pc = xml_writer.pc()
                                    
                                    label_else = f'else{pc}'
                                    label_if = f'if{pc}'
                                    xml_writer.writeIf(label_else)
                                    tokenizer.progress()

                                    #write { symbol
                                    tokenizer.progress()

                                   
                                    #write statements
                                    compileStatements()
                                    xml_writer.writeGoto(label_if)
                                    #write } symbol
                                    tokenizer.progress()

                                    xml_writer.writeLabel(label_else)
                                    #write else keyword
                                    if(tokenizer.lookAheadToken().content == 'else'):
                                        #case for else
                                        tokenizer.progress()
                                        #write { symbol
                                        tokenizer.progress()
                                        #write statements
                                        compileStatements()
                                        #write } symbol
                                        tokenizer.progress()
                                    xml_writer.writeLabel(label_if)

                                def compileWhile():
                                    whilePC = xml_writer.pc()
                                    label_do = f'do{whilePC}'
                                    label_while = f'while{whilePC}'
                                    xml_writer.writeLabel(label_do)
                                    #write while keyword
                                    tokenizer.progress()
                                    #write ( symbol
                                    tokenizer.progress()
                                    #write expression
                                    expression()
                                    xml_writer.writeArithmetic('not')
                                    #write ) symbol
                                    xml_writer.writeIf(label_while)
                                    tokenizer.progress()
                                    #write { symbol
                                    tokenizer.progress()
                                    #write statements
                                    compileStatements()
                                    #write } symbol
                                    tokenizer.progress()
                                    xml_writer.writeGoto(label_do)
                                    xml_writer.writeLabel(label_while)

                                

                                def compileDo():
                                    
                                    #write do keyword
                                    tokenizer.progress()
                                    #write call method
                                    callMethod()
                                    #write ; symbol
                                    xml_writer.writePop('temp', 0)
                                    tokenizer.progress()
                                  

                                def compileReturn():
                                    #write return keyword
                                    tokenizer.progress()
                                    if tokenizer.lookAheadToken().content != ';':
                                        #write expression
                                        expression()
                                    else:
                                        xml_writer.writePush('constant', 0)
                                    #write ; symbol
                                    xml_writer.writeReturn()
                                    tokenizer.progress()
                                    

                                #write statements, continue function for subroutineBody
                                # xml_writer.addXmlElement('statements')  
                                while tokenizer.lookAheadToken().content in self.compilationStatementTrigger:
                                        
                                            if tokenizer.lookAheadToken().content == 'let':
                                                compileLet()
                                            elif tokenizer.lookAheadToken().content == 'if':
                                                compileIf()
                                            elif tokenizer.lookAheadToken().content == 'while':
                                                compileWhile()
                                            elif tokenizer.lookAheadToken().content == 'do':
                                                compileDo()
                                            elif tokenizer.lookAheadToken().content == 'return':
                                                compileReturn()

                                # xml_writer.addXmlElement('statements', end=True)
                                
                        compileStatements()
                        #write } symbol
                        tokenizer.progress()
                            
                        
                        #call subroutineBody
                        # subroutineBody()
                        #continue for compilesubroutine
                        
                        #xml_writer.addXmlElement('subroutineDec', end=True)

                                
                                
                    #continue for compile class     
                    #class keyword
                    #xml_writer.addXmlElement('class')
                    tokenizer.progress()
                    
                    #xml_writer.addTokenXml(className)
                    #class name
                    xml_writer.name = tokenizer.progress().content
                    #{ symbol
                    
                    symbolParenthesis = tokenizer.progress()
                    #xml_writer.addTokenXml(symbolParenthesis)
                    
                    # find classVarDec
                    
                    
                    # Before accessing .content, check if lookAheadToken() is not None
                    while tokenizer.lookAheadToken() is not None and tokenizer.lookAheadToken().content in self.VariableTriggers:
                        #[static', 'field']
                        compileClassVarDec()

                    # Similarly, for the next while-loop
                    while tokenizer.lookAheadToken() is not None and tokenizer.lookAheadToken().content in self.SubroutineDecTriggers:
                        # in ['constructor', 'function', 'method']
                        compileSubroutine()
                    #} symbol
                    symbolParenthesis = tokenizer.progress()
                    #xml_writer.addTokenXml(symbolParenthesis) 
                    #xml_writer.addXmlElement('class', end=True)
                                        
                                
                #continue for process_file
                #end of compileClass
                compileClass()

               
                
             

                
