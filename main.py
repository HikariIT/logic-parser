import itertools as it


class Evaluator:

    def __init__(self):
        self.operators = {
            '~': [5, True],
            '^': [4, True],
            'v': [3, True],
            '=>': [2, False],
            '<=>': [1, True],
            '(': [0, True]
        }

        self.operations = {
            '~': lambda a: not a,
            '^': lambda a, b: a and b,
            'v': lambda a, b: a or b,
            '=>': lambda a, b: (not a) or b,
            '<=>': lambda a, b: a == b,
        }


    @staticmethod
    def process_string(string_form):

        split_string = string_form.split(' ')
        return split_string

    def convert_to_rpn(self, string):
        queue = []
        stack = []

        for element in string:
            if type(element) == bool:
                queue.append(element)
            elif element == '(':
                stack.append(element)
            elif element == ')':
                while True:
                    if len(stack) == 0:
                        print("Bad parentheses")
                        break
                    top_el = stack[-1]
                    if top_el != '(':
                        queue.append(top_el)
                        stack.pop()
                    else:
                        stack.pop()
                        break
            elif element in self.operators.keys():
                value = self.operators[element][0]
                if len(stack) > 0:
                    while True:
                        top_el = stack[-1]
                        if self.operators[element][1]:
                            if value <= self.operators[top_el][0]:
                                queue.append(top_el)
                                stack.pop()
                                if len(stack) == 0:
                                    stack.append(element)
                                    break
                            else:
                                stack.append(element)
                                break
                        elif value < self.operators[top_el][0]:
                            queue.append(top_el)
                            stack.pop()
                            if len(stack) == 0:
                                stack.append(element)
                                break
                        else:
                            stack.append(element)
                            break
                else:
                    stack.append(element)

        queue.extend(stack.__reversed__())
        return queue

    def evaluate_value(self, rpn_string):
        stack = []

        for element in rpn_string:
            if type(element) == bool:
                stack.append(element)
            elif element == '~':
                a = stack.pop()
                stack.append(self.operations[element](a))
            else:
                a = stack.pop()
                b = stack.pop()
                stack.append(self.operations[element](b, a))

        return stack[0]

    @staticmethod
    def set_bool_values(form, combination):
        result_form = []
        for i, element in enumerate(form):
            result_form.append(element)
            if element in combination.keys():
                result_form[i] = combination[element]
        return result_form

    @staticmethod
    def generate_combination_set(variable_names):
        combinations = it.product(*[[True, False] for _ in range(len(variable_names))])
        combination_set = []

        for combination in combinations:
            comb_dict = {}
            for i, name in enumerate(variable_names):
                comb_dict[name] = combination[i]
            combination_set.append(comb_dict)

        return combination_set

    def get_variable_names(self, processed_form):
        variable_names = set()
        for element in processed_form:
            if element not in self.operators.keys() and element != ')':
                variable_names.add(element)
        return variable_names

    def are_equal(self, form_1, form_2):
        # TODO: Extend this to many forms??

        new_form = '( ' + form_1 + ' ) ' + '<=>' + ' ( ' + form_2 + ' )'
        return self.is_tautology(new_form)

    def is_satisfiable(self, form):
        form = self.process_string(form)
        variable_names = self.get_variable_names(form)

        combination_set = self.generate_combination_set(variable_names)
        satisfiable = False

        for combination in combination_set:
            bool_form = self.set_bool_values(form, combination)
            rpn = self.convert_to_rpn(bool_form)
            if self.evaluate_value(rpn):
                satisfiable = True

        return satisfiable

    def is_tautology(self, form):
        form = self.process_string(form)
        variable_names = self.get_variable_names(form)

        combination_set = self.generate_combination_set(variable_names)
        tautology = True

        for combination in combination_set:
            bool_form = self.set_bool_values(form, combination)
            rpn = self.convert_to_rpn(bool_form)
            if not self.evaluate_value(rpn):
                tautology = False

        return tautology


def main():

    variable_names = ['p', 'q', 'r']
    string_form = "p => q <=> ~ p v q "

    evaluator = Evaluator()
    combination_set = evaluator.generate_combination_set(variable_names)
    processed_form = evaluator.process_string(string_form)

    # for combination in combination_set:
    #     bool_form = evaluator.set_bool_values(processed_form, combination)
    #     rpn = evaluator.convert_to_rpn(bool_form)
    #     value = evaluator.evaluate_value(rpn)

    print(evaluator.are_equal("( p => q ) => r", "( p v r ) ^ ( ~ q v r )"))


main()
