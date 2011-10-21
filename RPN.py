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
        @type call: callback
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

    def calculate(self, *args):
        if self.call:
            return self.call(*args)
        else:
            return None


class RPNParser(object):
    """
    A parser which is able to create a RPNExpression object.
    It needs to have operators defined (as a list of RPNOperator objects)
    and parentheses symbols defined.
    """
    def __init__(self, operators=None,
                 open_parenthesis='(', close_parenthesis=')'):
        """
        initializes the parser.
        @type operators: list
        @param operators: list of RPNOperator objects.
                          These operators will be used in parsing process
        @type open_parenthesis: string
        @param open_parenthesis: a symbol that will be interpreted as
                                 a left (opening) parenthesis. default '('
        @type close_parenthesis: a symbol that will be interpreted as
                                 a right (closing) parenthesis. default ')'
        """
        self.open_parenthesis = open_parenthesis
        self.close_parenthesis = close_parenthesis
        self.operators = operators[:]

    def generateRPNExpression(self, infix_expression):
        """
        parses the expression in infix notation. It needs properly defined
        operators and parenthesis (@see: __init__).
        @type infix_expression: str
        @param infix_expression: infix expression to be parsed
        @rtype: RPNExpression
        @return: a RPNExpression object that is ready to be evaluated
                 (provided that operators are properly defined).
        """
        #TODO: optimize, check, test
        stack = []
        output = RPNExpression()
        for atom in infix_expression:
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
        while len(stack) > 0:
            output.append(stack.pop())
        return output


class RPNExpression(list):
    def evaluate(self):
        pass
