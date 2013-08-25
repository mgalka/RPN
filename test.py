'''
Created on 25-08-2013

@author: mgalka
'''
import unittest
import RPN

def substract(a, b):
    return a-b

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b


class TestInfixConversionToRPN(unittest.TestCase):

    def setUp(self):
        self.operators = [
                          RPN.RPNOperator("+", priority=1, number_of_operands=2, call=add),
                          RPN.RPNOperator("-", priority=1, number_of_operands=2, call=substract),
                          RPN.RPNOperator("*", priority=2, number_of_operands=2, call=multiply),
                          RPN.RPNOperator("/", priority=2, number_of_operands=2, call=divide)
                          ]
        self.long_operators = [
                          RPN.RPNOperator("++", priority=1, number_of_operands=2, call=add),
                          RPN.RPNOperator("---", priority=1, number_of_operands=2, call=substract),
                          RPN.RPNOperator("****", priority=2, number_of_operands=2, call=multiply),
                          RPN.RPNOperator("///", priority=2, number_of_operands=2, call=divide)
                          ]

    def testExpressionWithOneOperator(self):
        infix_expression = "2+2"
        parser = RPN.RPNParser(self.operators, open_parenthesis='(', close_parenthesis=')')
        rpn_expr = parser.generate_rpn_expression(infix_expression)
        print rpn_expr
        self.assertEqual(str(rpn_expr), "2 2 +")

    def testExpressionWithSymbolsLongerThanOneChar(self):
        infix_expression = "25+2-132"
        parser = RPN.RPNParser(self.operators, open_parenthesis='(', close_parenthesis=')')
        rpn_expr = parser.generate_rpn_expression(infix_expression)
        print rpn_expr
        self.assertEqual(str(rpn_expr), "25 2 + 132 -")

    def testInfixExpressionToList(self):
        infix_expression = '(12*4)+5'
        expected_result = ['(','12',self.operators[2],'4',')',self.operators[0],'5']
        parser = RPN.RPNParser(self.operators, open_parenthesis='(', close_parenthesis=')')
        self.assertEqual(parser._infix_to_list(infix_expression), expected_result)

    def testInfixExpressionToListWithLongParenthesisSymbols(self):
        infix_expression = '((12*4)))+5'
        expected_result = ['((','12',self.operators[2],'4',')))',self.operators[0],'5']
        parser = RPN.RPNParser(self.operators, open_parenthesis='((', close_parenthesis=')))')
        self.assertEqual(parser._infix_to_list(infix_expression), expected_result)

    def testInfixExpressionToListWithLongOperatorSymbols(self):
        infix_expression = '(12****4)++5'
        expected_result = ['(','12',self.long_operators[2],'4',')',self.long_operators[0],'5']
        parser = RPN.RPNParser(self.long_operators, open_parenthesis='(', close_parenthesis=')')
        self.assertEqual(parser._infix_to_list(infix_expression), expected_result)

    def testInfixExpressionToListWithLiteralsBeginingLikeOperator(self):
        infix_expression = '(12****4)+5'
        expected_result = ['(','12',self.long_operators[2],'4',')','+5']
        parser = RPN.RPNParser(self.long_operators, open_parenthesis='(', close_parenthesis=')')
        self.assertEqual(parser._infix_to_list(infix_expression), expected_result)

    def testInfixExpressionToListWithLongOperatorSymbolsAndLongParenthesis(self):
        infix_expression = '((12****4))++5'
        expected_result = ['((','12',self.long_operators[2],'4','))',self.long_operators[0],'5']
        parser = RPN.RPNParser(self.long_operators, open_parenthesis='((', close_parenthesis='))')
        self.assertEqual(parser._infix_to_list(infix_expression), expected_result)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()