import JackToken

class symbol:
    def __init__(self):
        self.table = []

    def define(self, dataType, name, kind):
        self.table.append({'dataType': dataType, 'name': name, 'kind': kind, 'index': self.varCount(kind)})

    def varCount(self, kind):
        ct = 0
        for var in self.table:
            if var['kind'] == kind:
                ct += 1
        return ct
    
    def determineKind(self, name):
        for var in self.table:
            if var['name'] == name:
                return var['kind']
        return None
    
    def determineType(self, name):
        for var in self.table:
            if var['name'] == name:
                return var['dataType']
        return None
    
    def determineIndex(self, name):
        for var in self.table:
            if var['name'] == name:
                return var['index']
        return None
    
    def getNameRow (self, name):
        for row in self.table:
            if row['name'] == name:
                return row
        return None
    
class VMCode:
    def __init__(self, file):
        self.file = file
        self.name = ''
        self.scope = symbol()
        self.subScope = symbol()
        self.counter = 0

    def pc(self):
        self.counter += 1
        return self.counter
    
    def searchThrName(self, name):
        row = self.subScope.getNameRow(name)
        if row is None:
            row = self.scope.getNameRow(name)
        return row
    
    def write(self, code):
        self.file.write(code)
    
    def writePush(self, segment, index):
        self.write(f'push {segment} {index}\n')
    
    def writePop(self, segment, index):
        self.write(f'pop {segment} {index}\n')
    
    def writeArithmetic(self, command):
        self.write(f'{command}\n')
    
    def writeLabel(self, label):
        self.write(f'label {label}\n')
    
    def writeGoto(self, label):
        self.write(f'goto {label}\n')
    
    def writeIf(self, label):
        self.write(f'if-goto {label}\n')
    
    def writeCall(self, name, nArgs):
        self.write(f'call {name} {nArgs}\n')
    
    def writeFunction(self, name, nLocals):
        self.write(f'function {name} {nLocals}\n')
    
    def writeReturn(self):
        self.write('return\n')
    
