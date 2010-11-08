
import re

class Variable(object):
    def __init__(self, symbol, value=None,
                               dependencies=[]):

        self.symbol = symbol
        self.value = value
        self.dependencies = dependencies

    def __unicode__(self):
        return self.symbol
    def __str__(self):
        return self.__unicode__()
    def __repr__(self):
        return self.__unicode__()

class Expression(object):
    def __init__(self, code):
        self.code = code
        self.parse(code)

    def parse(self, code):
        special = ['+','-','*','/','^','(',')']
        tokens = []
        buffer = ''
        for char in code:
            if char in special:
                if buffer:
                    tokens.append(buffer)
                    tokens.append(char)
                    buffer = ''
                else:
                    tokens.append(char)
            else:
                buffer += char
        if buffer:
            tokens.append(buffer)
        self.tokens = tokens

        var_regex = re.compile('[A-Za-z_][A-Za-z0-9_]*')
        
        new_tokens = list(tokens)
        self.variables = []
        for i, token in enumerate(tokens):
            match = var_regex.match(token)
            if match is not None and match.group(0) == token:
                new_tokens[i] = Variable(token)
                self.variables.append(new_tokens[i])
        self.tokens = new_tokens
                
        
    def __unicode__(self):
        return self.code
    def __str__(self):
        return self.__unicode__()
    def __repr__(self):
        return self.__unicode__()

class Equation(Expression):
    def __init__(self, code):
        split = code.split('=')
        self.tokens = [Expression(split[0]), '=', Expression(split[1])]        

class PhysicalQuantity(Variable):
    def __init__(self, symbol, value=None, 
                               dependencies=[], 
                               conversion_factor=1, 
                               units=None):

        self.conversion_factor = conversion_factor
        self.convert_value = None 
        if value is not None:
            self.convert_value = conversion_factor * value

        super(PhysicalQuantity, self).__init__(symbol, 
                                               value=value,
                                               dependencies=dependencies)

class Scalar(PhysicalQuantity):
    pass
class Vector(PhysicalQuantity):
    def cross(self, vector):
        result = []
        a = self.value
        b = vector.value
        result.append(a[1]*b[2] - a[2]*b[1])
        result.append(a[2]*b[0] - a[0]*b[2])
        result.append(a[0]*b[1] - a[1]*b[0])
        return Vector(symbol='no_symbol', value=result)

    def dot(self, vector):
        a = self.value
        b = vector.value

        result = a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
        
class Tensor(PhysicalQuantity):
    pass
