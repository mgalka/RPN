class ParenthesisMismatchError(Exception):
    """ Raised when opening parentheses in infix notation doesn't match
        the closing ones.
    """
    def __init__(self, *args):
        Exception.__init__(self, *args)

    def __str__(self):
        return "Parentheses mismatch"

class RPNOperator(object):
    """
    An operator in terms of Reversed Polish Notation.
    This class is used by RPNExprFactory to parse and by RPNCalculator to
    calculate given expression value.
    """
    def __init__(self, symbol, priority=1, number_of_operands=2, call=None):
        """
        Creates the RPNOperator due to specified attributes.

        @type symbol: str
        @param symbol: A symbol of an operator.
                       It's used to find the operator in infix notation string.
        @type priority: int
        @param priority: The priority of the operator.
                         Higher number means higher priority.
        @type number_of_operands: int
        @param number_of_operands: The number of operands that operator needs.
        @type call: function
        @param call: A function that performs an operation on the operands
                     and returns a value.
                     If it's not defined the RPNCalculator won't be able
                     to evaluate the expression.
        """
        self.symbol = symbol
        self.priority = priority
        self.number_of_operands = number_of_operands
        self.call = call

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return "RPNOperator('%s')" % self.symbol

    def __call__(self, *args, **kwargs):
        self.calculate(*args, **kwargs)

    def calculate(self, *args, **kwargs):
        if self.call:
            return self.call(*args)
        else:
            return None


class RPNParser(object):
    """
    A parser which is able to create a RPNExpression object.
    It needs to have operators (as a list of RPNOperator objects)
    and parenthesis symbols defined. It should be used to generate
    RPNExpressions which can be stored and/or evaluated later on.
    """
    def __init__(self, operators=None,
                 open_parenthesis='(', close_parenthesis=')'):
        """
        initializes the parser.
        @type operators: list
        @param operators: list of RPNOperator objects.
                          These are used to determine what is an operator in the
                          expression.
        @type open_parenthesis: string
        @param open_parenthesis: a symbol that will be interpreted as
                                 a left (opening) parenthesis. default '('
        @type close_parenthesis: a symbol that will be interpreted as
                                 a right (closing) parenthesis. default ')'
        """
        self.open_parenthesis = open_parenthesis
        self.close_parenthesis = close_parenthesis
        self.operators = operators[:]

    def _infix_to_list(self, infix_expression):
        '''
        This method changes infix_expression to the list to help parsing
        by generate_rpm_expression. It's not meant to be used from outside.
        It creates a list where every symbol/literal, operator or parenthesis are
        a separate element in order to rpm expression generating method
        @type infix_expression: str
        @param infix_expression: Infix expression string
        '''
        pos = 0
        expr_list = list()
        slice_begin = 0
        #Get characters on which we should stop when parsing
        first_chars = [operator.symbol[0] for operator in self.operators]
        first_chars.append(self.open_parenthesis[0])
        first_chars.append(self.close_parenthesis[0])
        #map objects with their names first characters
        obj_to_stop = dict((char,list()) for char in set(first_chars))
        map(lambda x: obj_to_stop[x.symbol[0]].append(x), self.operators)
        obj_to_stop[self.open_parenthesis[0]].append(self.open_parenthesis)
        obj_to_stop[self.close_parenthesis[0]].append(self.close_parenthesis)
        while pos < len(infix_expression):
            if infix_expression[pos] in obj_to_stop:
                objects = obj_to_stop[infix_expression[pos]]
                for obj in objects:
                    if isinstance(obj, RPNOperator):
                        length = len(obj.symbol)
                        symbol = obj.symbol
                    elif isinstance(obj, basestring):
                        length = len(obj)
                        symbol = obj
                    if infix_expression[pos:pos + length] == symbol:
                        if slice_begin < pos:
                            expr_list.append(infix_expression[slice_begin: pos])
                        expr_list.append(obj)
                        pos += length
                        slice_begin = pos
                        break
                    else:
                        pos += 1
            else:
                pos += 1
        expr_list.append(infix_expression[slice_begin:])
        return expr_list

    def check_parentheses(self, infix_expression):
        counter = 0
        for ch in infix_expression:
            if ch == self.open_parenthesis:
                counter += 1
            if ch == self.close_parenthesis:
                counter -= 1
                if counter < 0:
                    raise ParenthesisMismatchError
        if counter:
            raise ParenthesisMismatchError

    def generate_rpn_expression(self, infix_expression):
        """
        parses the expression in infix notation. It needs properly defined
        operators and parenthesis (@see: __init__).
        @type infix_expression: str
        @param infix_expression: infix expression to be parsed
        @type: RPNExpression
        @return: a RPNExpression object that is ready to be evaluated
                 (provided that operators are properly defined).
        """
        #remove white characters
        infix_expression = ''.join(infix_expression.split())
        #TODO: optimize, check, test
        self.check_parentheses(infix_expression)
        stack = []
        output = RPNExpression()
        infix_expr_list = self._infix_to_list(infix_expression)
        for atom in infix_expr_list:
            if atom == self.open_parenthesis:
                stack.append(atom)
            elif atom == self.close_parenthesis:
                element = stack.pop()
                while str(element) != self.open_parenthesis:
                    output.append(element)
                    element = stack.pop()
            elif atom in self.operators:
                if (len(stack) == 0 or
                    str(stack[-1]) == self.open_parenthesis or
                    stack[-1].priority < atom.priority):
                    stack.append(atom)
                elif (isinstance(stack[-1], RPNOperator) and
                      stack[-1].priority >= atom.priority):
                    output.append(stack.pop())
                    while (len(stack) > 0 and
                           isinstance(stack[-1], RPNOperator) and
                           stack[-1].priority >= atom.priority):
                        output.append(atom.priority.pop())
                    stack.append(atom)
            else:
                #this is an operand
                output.append(atom)
        output.extend(stack[::-1])
        stack = []
        return output


class RPNExpression(list):
    def evaluate(self, values=None):
        raise NotImplementedError

    def __str__(self):
        return ' '.join([str(item) for item in self])