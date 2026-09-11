import sys
from pathlib import Path


class EppRuntime:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def run_program(self, source_text):
        sentences = [s.strip() for s in source_text.split('.') if s.strip()]
        self.execute_block(sentences)

    def execute_block(self, sentences):
        index = 0
        while index < len(sentences):
            sentence = sentences[index]
            lower = sentence.lower()

            if lower.startswith('if '):
                end_index = self.find_block_end(sentences, index, 'if', 'end if')
                else_index = next(
                    (position for position in range(index + 1, end_index)
                     if sentences[position].lower() == 'otherwise'),
                    end_index,
                )
                if self.evaluate_condition(sentence[3:].strip()):
                    self.execute_block(sentences[index + 1:else_index])
                elif else_index < end_index:
                    self.execute_block(sentences[else_index + 1:end_index])
                index = end_index + 1
                continue

            if lower.startswith('repeat '):
                end_index = self.find_block_end(sentences, index, 'repeat', 'end repeat')
                count = int(self.evaluate_expression(sentence[7:].replace(' times', '').strip()))
                for _ in range(count):
                    self.execute_block(sentences[index + 1:end_index])
                index = end_index + 1
                continue

            if lower.startswith('define a function named '):
                end_index = self.find_block_end(sentences, index, 'function', 'end function')
                self.handle_function_def(sentence, sentences[index + 1:end_index])
                index = end_index + 1
                continue

            if lower in ('otherwise', 'then') or lower.startswith('end '):
                index += 1
                continue

            self.execute_sentence(sentence)
            index += 1

    def find_block_end(self, sentences, start, block_name, end_sentence):
        depth = 0
        for index in range(start, len(sentences)):
            lower = sentences[index].lower()
            is_open = lower.startswith(f'{block_name} ')
            if block_name == 'function':
                is_open = lower.startswith('define a function named ')
            if is_open:
                depth += 1
            elif lower == end_sentence:
                depth -= 1
                if depth == 0:
                    return index
        raise ValueError(f'Missing {end_sentence}')

    def execute_sentence(self, sentence):
        lower = sentence.lower()

        if lower.startswith('let '):
            self.handle_let(sentence)
            return

        if lower.startswith('set '):
            self.handle_set(sentence)
            return

        if lower.startswith('display '):
            value = self.evaluate_expression(sentence[8:].strip())
            print(value)
            return

        if lower.startswith('print '):
            value = self.evaluate_expression(sentence[6:].strip())
            print(value)
            return

        if lower.startswith('read a '):
            self.handle_read(sentence)
            return

        if lower.startswith('if '):
            self.handle_if(sentence)
            return

        if lower.startswith('repeat '):
            self.handle_repeat(sentence)
            return

        if lower.startswith('define a function named '):
            self.handle_function_def(sentence)
            return

        if lower.startswith('call '):
            self.handle_call(sentence)
            return

        if lower.startswith('give back '):
            self.handle_return(sentence)
            return

        if lower.startswith('begin program'):
            return

        if lower.startswith('end program'):
            return

        if lower.startswith('end if'):
            return

        if lower.startswith('end repeat'):
            return

        if lower.startswith('end function'):
            return

        raise ValueError(f"Unknown sentence: {sentence}")

    def handle_let(self, sentence):
        rest = sentence[4:].strip()
        if ' be the ' in rest:
            name_part, value_part = rest.split(' be the ', 1)
            name = self.normalize_name(name_part)
            value = self.parse_literal(value_part)
            self.variables[name] = value
            return

        raise ValueError(f"Invalid let statement: {sentence}")

    def handle_set(self, sentence):
        rest = sentence[4:].strip()
        if ' to ' in rest:
            name_part, value_part = rest.split(' to ', 1)
            name = self.normalize_name(name_part)
            self.variables[name] = self.evaluate_expression(value_part)
            return

        raise ValueError(f"Invalid set statement: {sentence}")

    def handle_read(self, sentence):
        rest = sentence[8:].strip()
        if ' into ' in rest:
            _, name = rest.split(' into ', 1)
            value = input(f'{name.strip()}: ')
            self.variables[self.normalize_name(name)] = self.coerce_value(value)
            return

        raise ValueError(f"Invalid read statement: {sentence}")

    def handle_if(self, sentence):
        condition = sentence[3:].strip()
        if self.evaluate_condition(condition):
            return

    def handle_repeat(self, sentence):
        rest = sentence[7:].strip()
        if ' times' in rest:
            count_text = rest.replace(' times', '').strip()
            count = int(self.evaluate_expression(count_text))
            for _ in range(count):
                pass
            return

        raise ValueError(f"Invalid repeat statement: {sentence}")

    def handle_function_def(self, sentence, body):
        rest = sentence[len('define a function named '):].strip()
        name_part, _, params_part = rest.partition(' with the parameters ')
        name = self.normalize_name(name_part)
        params = [] if not params_part else [self.normalize_name(param)
                                             for param in params_part.split(' and ')]
        self.functions[name] = {'params': params, 'body': body}

    def handle_call(self, sentence):
        rest = sentence[5:].strip()
        if ' with ' in rest:
            name_part, args_part = rest.split(' with ', 1)
            name = self.normalize_name(name_part)
            func = self.functions.get(name)
            if func is None:
                raise ValueError(f"Function not found: {name}")
            args = [self.evaluate_expression(arg.strip()) for arg in args_part.split(' and ')]
            self.call_function(name, args)
            return

        raise ValueError(f"Invalid function call: {sentence}")

    def handle_return(self, sentence):
        value = self.evaluate_expression(sentence[len('give back '):].strip())
        return value

    def call_function(self, name, args):
        function = self.functions.get(name)
        if function is None:
            raise ValueError(f'Function not found: {name}')
        previous = self.variables
        self.variables = dict(previous)
        self.variables.update(dict(zip(function['params'], args)))
        result = None
        for sentence in function['body']:
            if sentence.lower().startswith('give back '):
                result = self.handle_return(sentence)
                break
            self.execute_sentence(sentence)
        self.variables = previous
        return result

    def evaluate_expression(self, expr):
        expr = expr.strip()
        if expr.lower().startswith('the result of calling '):
            call = expr[len('the result of calling '):]
            name, _, args_part = call.partition(' with ')
            args = [self.evaluate_expression(arg.strip()) for arg in args_part.split(' and ')]
            return self.call_function(self.normalize_name(name), args)
        if expr.lower() in ('true', 'false'):
            return expr.lower() == 'true'

        if expr.startswith('the word '):
            return expr[len('the word '):].strip()

        if expr.startswith('the number '):
            return int(expr[len('the number '):].strip())

        if expr.startswith('the letter '):
            return expr[len('the letter '):].strip()

        if expr.startswith('the list of '):
            items = expr[len('the list of '):].strip()
            return [self.evaluate_expression(part.strip()) for part in items.split(',')]

        if expr in self.variables:
            return self.variables[expr]

        if ' plus ' in expr:
            left, right = [self.evaluate_expression(part.strip()) for part in expr.split(' plus ', 1)]
            return left + right

        if ' minus ' in expr:
            left, right = [self.evaluate_expression(part.strip()) for part in expr.split(' minus ', 1)]
            return left - right

        if ' times ' in expr:
            left, right = [self.evaluate_expression(part.strip()) for part in expr.split(' times ', 1)]
            return left * right

        if ' divided by ' in expr:
            left, right = [self.evaluate_expression(part.strip()) for part in expr.split(' divided by ', 1)]
            return left / right

        if ' is equal to ' in expr:
            left, right = [self.evaluate_expression(part.strip()) for part in expr.split(' is equal to ', 1)]
            return left == right

        if ' is greater than ' in expr:
            left, right = [self.evaluate_expression(part.strip()) for part in expr.split(' is greater than ', 1)]
            return left > right

        if ' is less than ' in expr:
            left, right = [self.evaluate_expression(part.strip()) for part in expr.split(' is less than ', 1)]
            return left < right

        if ' is not equal to ' in expr:
            left, right = [self.evaluate_expression(part.strip()) for part in expr.split(' is not equal to ', 1)]
            return left != right

        if ' and ' in expr:
            left, right = [self.evaluate_condition(part.strip()) for part in expr.split(' and ', 1)]
            return left and right

        if ' or ' in expr:
            left, right = [self.evaluate_condition(part.strip()) for part in expr.split(' or ', 1)]
            return left or right

        if expr.startswith('not '):
            return not self.evaluate_condition(expr[4:].strip())

        if expr.isdigit():
            return int(expr)

        try:
            return float(expr)
        except ValueError:
            pass

        return expr

    def evaluate_condition(self, expr):
        expr = expr.strip()
        if expr in self.variables:
            return bool(self.variables[expr])
        return bool(self.evaluate_expression(expr))

    def parse_literal(self, value_part):
        value_part = value_part.strip()
        if value_part.lower() in ('true', 'false'):
            return value_part.lower() == 'true'

        if value_part.startswith('the word '):
            return value_part[len('the word '):].strip()

        if value_part.startswith('the number '):
            return int(value_part[len('the number '):].strip())

        if value_part.startswith('the letter '):
            return value_part[len('the letter '):].strip()

        if value_part.startswith('the list of '):
            items = value_part[len('the list of '):].strip()
            return [self.parse_literal(item.strip()) for item in items.split(',')]

        if value_part in self.variables:
            return self.variables[value_part]

        if value_part.isdigit():
            return int(value_part)

        try:
            return float(value_part)
        except ValueError:
            return value_part

    def coerce_value(self, raw):
        raw = raw.strip()
        if raw.lower() == 'true':
            return True
        if raw.lower() == 'false':
            return False
        try:
            if '.' in raw:
                return float(raw)
            return int(raw)
        except ValueError:
            return raw

    def normalize_name(self, name):
        name = name.strip().lower()
        return name.replace(' ', ' ')


def run_file(path):
    program_path = Path(path)
    source = program_path.read_text(encoding='utf-8')
    runtime = EppRuntime()
    runtime.run_program(source)


def main():
    if len(sys.argv) < 2:
        print('Usage: python eppfilerunner.py your_program.epp')
        return 1

    run_file(sys.argv[1])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
