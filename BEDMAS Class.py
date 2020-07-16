import numpy, traceback, time #REMOVE TIME

#MAKE POWERS FASTER | ERROR CHECKING COOL THING
class Equation_Solver:
    def __init__(self, equation):
        print(equation)
        self.steps = [equation]
        self.equation = self.format_equation(self.remove_redundant_brackets(equation)) #SAY SOMETHING ABOUT THE EXCESS BRACKETS (MAYBE ADD A COUNT — "Removed 13 redundant brackets"
        self.steps.append(self.equation)
        self.pairs = []
        #self.format_equation()
        #self.check_syntax()
        self.parse_brackets()
        print(self.equation)
        self.solve_hierarchy()

        
        
    def format_equation(self, value = ''):
        symbols = ['^', '/', '*', '+']
        if value != '':
            equation = value
        else:
            equation = self.equation
        if '(' in equation and ')' in equation:
            test = equation[equation.index('(')+1:equation.index(')')]
            if self.is_number(test):
                return test
        equation = equation.replace(' ', '')
        
        replacements = [
            ('{', '('), ('[', '('),
            ('}', ')'), (']', ')'),
            ('**', '^'),
            ('\\', '/'),
            ('--', '+'), ('+-', '-'), ('-+', '-')]
        for replacement in replacements:
            equation = equation.replace(*replacement)
        if equation[0] != '(' or equation[-1] != ')':
            equation = '(' + equation + ')'
        equation = list(equation)
       # print(self.equation, 'equation')
        for i in range(len(equation)):
            if equation[i] in symbols:
                equation[i-1] += ' '
                equation[i] += ' '
        for i in range(len(equation)):
            if equation[i] == '-':
                if equation[i - 1] not in symbols + ['(']:
                    equation[i-1] += ' '
                    equation[i] += ' '
                elif equation[i - 1] in symbols + ['(']:
                    equation[i] = '_'
        
        equation = ''.join(equation)
        if value != '':
            return equation
        self.equation = equation
    
##
##    def check_syntax(self): ##IMPLEMENT INTERACTIVE ERROR CHECKING
##        while True:
##            try:
##                eval(self.equation)
##                return True
##            except:
##                error = traceback.format_exc().split('\n')
##                print('Encounted ', end = '')
##                print(error)
##                print(error[6][error[6].index(' ') + 1:])
##                print('Error encountered when parsing the following point of the equation:')
##                print('\n'.join(error[4:6]))
##                print('Please edit and resubmit for calculation to continue')
##                import readline
##                what = 'tesitng'
##                #readline.set_startup_hook(lambda: readline.insert_text(what))
##                self.equation = input('testing : ')
##                print('what the heck')

    
    def parse_brackets(self, to_output = False, from_input = False, input_value = '', return_pairs_only = False):
        #s = time.time() #TIME TEST
        if return_pairs_only:
            to_output = True
        if not to_output:
            self.pairs = []
        else:
            internal_pairs = []
        starts, ends = [], []
        index = 0
        if from_input:
            equation = input_value
        else:
            equation = self.equation
        for character in equation:
            if character == '(':starts.insert(0, index) #OPTIMIZE WITH NUMPY ARRAYS 
            elif character == ')': ends.append(index)
            index += 1
        ends_length = len(ends)
        for start in starts:
            pair = numpy.array([start, 0])
            for end in range(ends_length):
                if ends[end] > start:
                    if not to_output:
                        self.pairs.append(equation[start : ends.pop(end) + 1])
                    else:
                        internal_pairs.append(equation[start : ends.pop(end) + 1])
                    ends_length -= 1
                    break
        if return_pairs_only: return internal_pairs
        #makes the parser work from the most brackets to the least brackets to create proper hierarchy
        if not to_output:
            self.pairs = [i for _, i in sorted(zip([i.count('(') for i in self.pairs], self.pairs), reverse = True)]
        else:
            internal_pairs = [i for _, i in sorted(zip([i.count('(') for i in self.pairs], self.pairs), reverse = True)]
        holder_pairs = []
        if not to_output: iterative_pairs = self.pairs
        else: iterative_pairs = internal_pairs
        for pair_one in iterative_pairs:
            index = 0
            if '(' in pair_one[1:-1]:
                for pair_two in iterative_pairs:
                    if pair_one != pair_two:
                        if pair_two in pair_one:
                            pair_one = pair_one.replace(pair_two, f'[{index}]')
                    index += 1
            holder_pairs.append(pair_one)
        #sorts the list of pairs to make them from the oldest to youngest children
        if to_output:
            return holder_pairs
        self.pairs = holder_pairs
        #self.pairs = [i for _, i in sorted(zip([i.count('[') for i in holder_pairs], holder_pairs), reverse = True)] REDUNDANT LINE BROKEN LINE, DON'T USE THIS UNLESS YOU ARE STUPID
    
        

    def solve_hierarchy(self):
        print(self.pairs, ': pairs')
        self.equation = self.pairs[0]
        value = 1
        while value != 0:
            print(self.pairs)
            self.create_step()
            value = self.solve_one_step() 
        while len(self.pairs[0].split()) != 1:
            self.solve_pair_at(0)
            self.equation = self.pairs[0]
            self.create_step()
            print('fucker', self.remove_redundant_brackets(self.pairs[0]))
        

    def solve_one_step(self):
        if '[' not in self.equation:
            return 0
        i = 1
        equation = self.equation
        while True:
            if f'[{i}]' in equation:
                equation = self.pairs[i]
                if '[' not in equation:
                    break
                i = 0
            i += 1
        self.solve_pair_at(i)
        self.equation = self.pairs[0]
            
                
    def solve_pair_at(self, index):
        equation = self.pairs[index]
        solved = equation
        solved = self.remove_redundant_brackets(self.perform_first_operation(solved)) #ERROR FOR BIG NUMBERS HERE
        self.pairs[index] = solved
        if len(solved.split()) == 1:
            solved = self.remove_redundant_brackets(solved)
            for i in range(len(self.pairs)):
                if i != index:
                    self.pairs[i] = self.pairs[i].replace(f'[{index}]', solved) #do for each step as you solve
                    #self.create_step(self.equation)
                    #if two:
                    #    self.pairs[i] = self.pairs[i].replace(solved, solved_2) #do for each step as you solve
                


    def perform_first_operation(self, equation):
        if '^' in equation:
            return self.perform_operation('^', equation)
        for i in (('/', '*'), ('+', '-')):
            one, two = i[0], i[1]
            if any(ii in equation for ii in (one, two)):
                ((equation.find(one), one), (equation.find(two), two))
                value = min(i for i in ((equation.find(one), one), (equation.find(two), two)) if i[0] > 0)[1]
                equation = self.perform_operation(value, equation)
                break
        return self.format_equation(equation) #could put something to check if the input is the same as the output
            

    def perform_operation(self, symbol, equation):
        try:
            equation = self.remove_redundant_brackets(equation)
        except:
            pass
        equation_list = []
        holder = ''
        number, number_back = False, False
        equation = equation.replace(' ', '')
        for i in equation:
            number_back = number
            number = self.is_number(i)
            if number:
                holder += i
            elif number_back:
                equation_list.append(holder)
                holder = ''
            if not number:
                equation_list.append(i)
        if holder != '':
            equation_list.append(holder)
        #print(equation_list, 'list of values')
        print(equation_list, 'list of values 1')
        try:
            for eindex in range(len(equation_list)):
                if 'e' in equation_list[eindex]:
                    print(equation_list[eindex])
                    equation_list[eindex] += equation_list.pop(eindex+1) + equation_list.pop(eindex+1)
        except:
            pass
        index = equation_list.index(symbol)
        amount_forward = 2
        print(equation_list, 'list of values')
        if equation_list[index+1]  == '_':
            amount_forward += 1
        amount_backward = 1
        if equation_list[index-2] == '_':
            amount_backward += 1
        equation_list = [i.replace('_', '-') for i in equation_list]
        #print(equation_list, 'list of values 2')
        #print(amount_backward)
        print('solve :', equation_list[index-amount_backward:index+amount_forward])
        if symbol == '^':
            equation_list[index-amount_backward:index+amount_forward] = [str(eval(''.join(equation_list[index-amount_backward:index+amount_forward]).replace('^', '**')))]
        else:
            replacer = (eval(''.join(equation_list[index-amount_backward:index+amount_forward])))
            print('solved', replacer)
            if 'e' in str(replacer):
                replacer = str(replacer)
                print(str(replacer).split('e'), 'testing')
                replacer = replacer.replace('-', '_')
            test = 0
            try:
                test = int(replacer)
            except:
                pass
            if test == replacer:   
                replacer = test
            equation_list[index-amount_backward:index+amount_forward] = [str(replacer)]
        #print('testing', self.format_equation(self.remove_redundant_brackets(' '.join(equation_list))))
        return self.format_equation(self.remove_redundant_brackets(' '.join(equation_list)))

    def remove_redundant_brackets(self, value):
        testing = value.replace('(', '').replace(')', '')
        if self.is_number(testing.replace('_', '')):
            return testing
            
        pairs = self.parse_brackets(from_input = True, input_value = value, return_pairs_only = True)
        length = len(pairs)
        length = length if length != 1 else 0
        for i in range(length):
            one = pairs[i]
            evaluation = eval(one.replace('_', '-'))
            redundancy_limit = 0
            try:
                while evaluation == eval(pairs[i+redundancy_limit+1].replace('_', '-')):
                    redundancy_limit += 1
            except:
                pass
            value = value.replace(pairs[i+redundancy_limit], one)
                            #ADDITIONAL USUAGE, POSSIBLE REWRITE IN THE FUTURE
            if '(' in one:
                testing = value.replace(one, one[1:-1])
                if eval(testing.replace('^', '**').replace('_', '-')) == eval(value.replace('^', '**').replace('_', '-')):
                    value = testing
        return value
        
    def is_number(self, value):
        try:
            value = value.replace('_', '-').replace('e', '10')
            if value == '.':
                return True
            int(float(value))
            return True
        except:
            return False

    def decrease_complexity(self, equation):
        
        if '[' not in equation:
            return equation
        i = 0
        while True:
            replace = f'[{i}]'
            if replace in equation:
                return equation.replace(replace, self.pairs[i])
            i += 1

    def create_step(self, value = ''):
        if value == '':
            equation = self.equation
        else:
            equation = value
        previous = ''
        while True:
            previous = equation
            equation = self.decrease_complexity(equation)
            if previous == equation:
                if equation in self.steps: return False
#                if self.steps != [] and self.steps[-1] == equation: return False
                if equation[0] == '(': equation = equation[1:-1]
                self.steps.append(equation.replace('_', '-'))
##                equation = self.remove_redundant_brackets(equation)
##                self.steps.append(equation)
                return True

        
        
            
            

















        
                
                
                    
            
            
            
        



if __name__ == "__main__":
     #   print(i)
    #print(eval('1*10*20*50**12312312'))
    #time.sleep(100000)
    thing = '((92-36747286348267489269*6**27)-2389+(6+(2+3+(2+3+(2+3+(2+3+(23678*789)**5))))))**3/0.00000000000000000000000000000000000000001'
    print(eval(thing))
    solver = Equation_Solver(thing)
    print()
    for i in solver.steps:
        print(i)
    print()
    print()
    print()
    print(solver.remove_redundant_brackets(thing))
    #for i in range(10):
     #   thing = (solver.perform_first_operation(thing))
      #  print(thing)
    #for i in range(10):
    #solver.parse_brackets()    
