import json
import os
import sys

# DFA/NFA/PDA Reader Command Line Application
# This program reads a finite automaton from a file and then allows
# the user to test strings against it and track routes through.

# This object stores information about a finite automaton.
# It can handle a DFA/NFA or a PDA of either determined type

# We use dictionaries embedded within dictionaries along with seperate chaining for hash collision


class FAObject:
    def is_pda(self):
        return self.isPDA

    def is_nfa(self):
        return self.isNFA

    def num_transitions(self, source_state, input_symbol, consume_symbol=None):
        if not self.has_transition(source_state, input_symbol, consume_symbol):
            return 0
        return len(self.transitions[(source_state, input_symbol)][consume_symbol])

    def get_transitions(self, source_state, input_symbol, consume_symbol=None):
        if self.has_transition(source_state, input_symbol, consume_symbol):
            return self.transitions[(source_state, input_symbol)][consume_symbol]
        return False

    def has_transition(self, source_state, input_symbol, consume_symbol=None):
        result = (source_state, input_symbol) in self.transitions.keys()

        # The idea is that all combinations of source state and input symbol will have at least one
        # dictionary entry where the consume symbol IS none, even if it's not a PDA.

        if result is True:
            search_target = self.transitions[(source_state, input_symbol)]
            result = consume_symbol in search_target
        return result

    def run_machine(self, start_state, input_string, path=None, stack=None):

        if not path:
            path = list()
        if not stack:
            stack = list()

        # We read the top of the stack in any case. If it's not a PDA, then it's None. If the stack is empty, it's none.
        stack_read = stack[-1] if (self.is_pda() and len(stack) > 0) else None

        if len(input_string) > 0:

            target_jobs = []
            if self.has_transition(start_state, input_string[0], None):
                # we have a transition for state and input with no consume.
                # Append a tuple to the target states list with the transition list, input_consume_symbol
                # and stack_consume_symbol.
                target_jobs.append((self.get_transitions(start_state, input_string[0], None), input_string[0], None))

            if self.has_transition(start_state, None, None):
                # we have a transition for state with no input or consume.
                # if we also push nothing, then this is an epilson transition.
                # even if we do, we must look at the depth of recursion for a state we can repeat infinitely many times
                target_jobs.append((self.get_transitions(start_state, None, None), None, None))

            if stack_read is not None:
                if self.has_transition(start_state, input_string[0], stack_read):
                    # we have a transition for state with input and WITH consume.
                    # Append a tuple to the target states list containing possible transitions, with the symbol to consume.
                    # We aren't ready to consume yet.
                    target_jobs.append((self.get_transitions(start_state, input_string[0], stack_read), input_string[0], stack_read))
                if self.has_transition(start_state, None, stack_read):
                    # we have a transition for state with no input and with consume.
                    # We aren't ready to consume yet.
                    target_jobs.append((self.get_transitions(start_state, None, stack_read), None, stack_read))


            truths = []
            for target_job in target_jobs:
                target_states = target_job[0]
                input_consume_symbol = target_job[1]
                stack_consume_symbol = target_job[2]
                next_stack = stack

                if stack_consume_symbol is not None:
                    if len(next_stack) == 0:
                        # We have a dead end. The only route needs to consume something on the stack and the stack is empty.
                        truths.append(False)
                        continue

                    # We consume here and assume the symbol matches the top of the stack.
                    # Perhaps there should be some error checking there.
                    stack_consume_symbol = next_stack.pop()

                for target_func in target_states:
                    target_state = target_func[0]
                    push_symbol = target_func[1]

                    if self.is_pda() and push_symbol is not None:
                        next_stack += list(push_symbol)


                    this_route = [(start_state, input_consume_symbol, target_state, stack_consume_symbol, push_symbol)]

                    # Are we trapped in a loop?
                    trapped = False
                    # Assuming 'n' is the number of entries to check
                    if len(path) > 10:
                        last_n_entries = path[-10:]  # Get the last 'n' entries from the 'paths' list
                        # Compare each entry with the new one
                        is_equivalent = all(entry == this_route[0] for entry in last_n_entries)
                        # Check if all entries are equivalent
                        if is_equivalent:
                            trapped = True
                            # Yeah, we're trapped. Let's discontinue this call stack by not creating a new machine.

                    result = False
                    if not trapped:
                        next_input = input_string[1:] if input_consume_symbol is not None else input_string
                        result = self.run_machine(target_state, next_input, path + this_route, next_stack)
                    truths.append(result)
            # Only one truth in our table needs to be true for the string to be valid.
            if True in truths:
                return True

        else:
            # len is zero
            # If we are here, then we are at the end of the string. That doesn't necessarily mean we are done.
            # It could also be an empty string.

            # First, let's check if we are in a winning state and the stack is empty. Then we might really be done.
            if start_state in self.accept_states and stack_read is None:
                # If we are here, then we are at the end of the string and also in a state which we can accept. Ding ding ding.
                # TODO: It would be a good idea to notify the loop that we can quit early.
                self.last_path = path + [(start_state, "", "accept", None, None)]
                return True
            else:
                # We still pass our path in, but it wasn't accepted so we don't add the accept state
                self.last_path = path

            if self.has_transition(start_state, None, stack_read):
                next_stack = stack
                if len(next_stack) > 0 and stack_read is not None:
                    next_stack.pop()
                # we have a transition for state with no input and with consume matching the top of the stack.
                truths = []
                target_states = self.get_transitions(start_state, None, stack_read)
                for target_state in target_states:
                    state_name = target_state[0]
                    push_symbol = target_state[1]
                    if push_symbol is not None:
                        next_stack.append(push_symbol)

                    this_route = [(start_state, None, state_name, stack_read, push_symbol)]
                    truths.append(self.run_machine(target_state[0], input_string, path + this_route, next_stack))
                if True in truths:
                    return True
        return False

    def test_string(self, input_string):
        self.last_path.clear()

        return self.run_machine(self.start_state, input_string)

    def print_last_path(self):
        result = []
        step = 0
        for (start_state, input_string, target_state, consume_symbol, push_symbol) in self.last_path:
            step += 1
            start_string = 'start ' if step == 1 else ''
            finalize_string = ''
            if step == len(self.last_path):
                finalize_string = 'and is '
                if target_state == 'accept':
                    finalize_string += 'accepted'
                else:
                    finalize_string += 'rejected'
            pda_string = ""
            if self.is_pda():
                pda_string = f", consumes {consume_symbol}, pushes {push_symbol},"
            line_string = f"{step}: {start_string}state {start_state} inputs '{input_string}'"+\
                    pda_string + \
                    f" and moves to state {target_state} {finalize_string}"
            result.append(line_string)
        return result

    def __init__(self, alphabet, all_states, start_state, accept_states, stack_alphabet=None, transitions=None, isNFA=False, is_pda=False, description=None):
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions or {}
        self.last_path = []
        self.alphabet = alphabet
        self.states = all_states
        self.isNFA = isNFA
        self.isPDA = is_pda
        self.stack_alphabet = stack_alphabet
        self.stack = []
        self.description = description
        # Prints the information that makes up this object. This can get pretty unreadable so we use
        # built-in json functions to prettyprint it.

    def __str__(self):
        properties = {"description": self.description, "alphabet": self.alphabet, "states": self.states, "accept_states": self.accept_states,
                      "transitions": []}

        # I certainly hope nobody has to debug this desperate attempt to cram all this formatting into one line.
        # This really should be broken up but isn't it great in a terrible way?

        for key, dest_info in self.transitions.items():
            for pop, dest_list in dest_info.items():
                for (destination, push) in dest_list:
                    operation_string = (" -> ("+(f"Pop: {pop}" if pop is not None else "") +\
                                       (',' if push is not None and pop is not None else '') +\
                                       (f"Push: {push}" if push is not None else "")+")") if self.is_pda() else ""
                    state_string = f"state {' input '.join(key)}" if key[1] else f"{key[0]}"
                    properties["transitions"].append(state_string + f"{operation_string} -> {destination}")

        return json.dumps(properties, separators=(',', '='), indent=1)

class FAFromFile(FAObject):
    def __init__(self, file_path):

        def failed_machine_check(critical=False, error_line=None):
            print(
                f"Warning: This might not be a working machine."
                f"{f'There is a formatting error on line {error_line}' if error_line else ''}"
                f"{'Creating a default machine with dfa.txt instead.' if critical==True else ''}")
            if critical:
                self.__init__("dfa.txt")
                self.source = "dfa.txt"

        machine_description = None
        self.source = file_path
        lines = []
        index = 0
        with open(file_path, 'r') as file:
            raw_lines = file.readlines()
            for line in raw_lines:
                if line.strip() == "":
                    continue
                comment_index = line.find('//')
                if (comment_index is not -1) and (index == len(raw_lines)-1):
                    machine_description = line[(comment_index+2):]
                    continue
                modified_line = line.strip() if comment_index == -1 else line[0:comment_index].strip()
                # A couple of things here. Let's skip blank lines, and then lets get the comment
                # from last line if it exists. That will be our machine description.
                lines.append(modified_line)
                index += 1

        is_pda = False

        # We are going to use the index of the first occurance of "->" in lines to determine if we are reading a D/NFA or PDA
        state_start_index = next(i for i, v in enumerate(lines) if v.find("->")>-1)
        if state_start_index < 4 or state_start_index > 5:
            failed_machine_check(critical=True)
            return
        elif state_start_index == 5:
            # congrats its a pda
            is_pda = True

        alphabet = lines[0][1:-1].split(',')
        stack_alphabet = lines[1][1:-1].split(',') if is_pda else []
        states = lines[2 if is_pda else 1][1:-1].split(',')
        start_state = lines[3 if is_pda else 2]
        accept_states = lines[4 if is_pda else 3][1:-1].split(',')
        transitions = {}
        collision = False
        c_file_index = state_start_index + 1

        for line in lines[c_file_index-1:]:
            # Transition Loop Begin
            base_parts = line.split('->')
            if len(base_parts) < 2:
                failed_machine_check(error_line=c_file_index)
                continue

            source_state_parts = base_parts[0].split(':') if is_pda else base_parts

            input_function = source_state_parts[0][1:-1].split(',')
            if len(input_function) < 2:
                failed_machine_check(error_line=c_file_index)
                continue

            source_state = input_function[0]
            input_symbol = input_function[1]

            if input_symbol is "":
                # This is fine, even intended.
                input_symbol = None

            if source_state is "":
                # Less so.
                failed_machine_check(error_line=c_file_index)
                continue

            stack_push = None
            stack_consume = None
            if is_pda:
                stack_operations = source_state_parts[1][1:-1].split(',')
                stack_push = stack_operations[1] or None
                stack_consume = stack_operations[0] or None

            destination_state = base_parts[1]

            # Originally, for NFAs and DFAs we had a two-tuple for a key
            # With the addition of pushdown automaton processing, I decided the best way to proceed
            # was to add the stack consume symbol into the typle for the dictionary key. In a pushdown automaton
            # the top of the stack will always be 'read' and compared against a symbol to possibly 'consume'.

            # Even if we are reading a DFA/NFA without a stack - we can still put the key there and simply have
            # it empty.
            if (source_state, input_symbol) in transitions:
                # We have a hash collision and must start separate chaining destination states.
                # This means that the object we are reading is actually an NFA, so we flag it to specify such.
                if not collision:
                    print(
                        f"non-determinate flag set due to duplicate state found at -> {source_state} : {input_symbol} on line {c_file_index} Ignoring future messages ")
                collision = True

                # Big Important decision here: We are using a dictionary whose keys are (source_state, and input_symbol)
                # and whose values are a dictionary whose keys are stack consume operations and whose values list
                # combinations of possible destination states and push values.
                # I changed this structure four times on the way here so far.
                current_items = transitions[(source_state, input_symbol)].get(stack_consume) or []
                transitions[(source_state, input_symbol)].__setitem__(stack_consume, current_items + [(destination_state, stack_push)])
            else:
                transitions[(source_state, input_symbol)] = dict({stack_consume: [(destination_state, stack_push)]})

            c_file_index += 1
            # Transition Loop End

        super().__init__(alphabet, states, start_state, accept_states, transitions=transitions, isNFA=collision, is_pda=is_pda, stack_alphabet=stack_alphabet, description=machine_description)

class CLIProgram:

    def start(self):

        print("Available commands: exit, load, test, lastpath, info, help")
        self.running = True
        while self.running:
            command = input("Enter a command: ")
            self.process_command(command)

    def process_command(self, command):

        parts = command.split()
        if len(parts) > 0:
            if parts[0] == "exit":
                self.running = False
            elif parts[0] == "load" and len(parts) == 2:
                file_arg = parts[1]
                self.load_file(file_arg)
            elif parts[0] == "test" and self.dfa:
                arguments = ' '.join(parts[1:])
                self.test_function(arguments)
            elif parts[0] == "lastpath" and self.dfa:
                lp=self.dfa.print_last_path()
                print("\n".join(lp))
            elif parts[0] == "info" and self.dfa:
                print(self.dfa.__str__())
            elif parts[0] == "help":
                print("Available commands:")
                print("exit: Exit the program.")
                print("load <file_path>: Load a DFA/NFA/PDA from a text file.")
                print("test <input_string>: Test an input string against the loaded DFA/NFA/PDA.")
                print("lastpath: Print the last path used to process a string through the DFA/NFA/PDA.")
                print("info: Print information about the loaded DFA/NFA/PDA.")
            else:
                print("Invalid command.")
    def fa_label(self):

        return str("N-" if self.dfa.is_nfa() is True else "D-") + ("PDA" if self.dfa.is_pda() is True else "FA")
    def load_file(self, fa):
        if not os.path.exists(fa):
            print("Error: File does not exist")
            return
        self.dfa = FAFromFile(fa)
        print(self.fa_label() + " Loaded: "+self.dfa.source)

    def test_function(self, arguments):
        print("Testing function with string:", arguments)
        is_accepted = self.dfa.test_string(arguments)

        if is_accepted:
            print(f"String accepted by the {self.fa_label()}.")
        else:
            print(f"String not accepted by the {self.fa_label()}.")

    def __init__(self, **kwargs):
        self.running = False
        self.dfa = None
        self.falabel = None
        if "file" in kwargs:
            self.load_file(kwargs["file"])
            if "test" in kwargs:
                if kwargs['test'] is not None:
                    self.test_function(kwargs["test"])
                else:
                    self.start()

if len(sys.argv) > 1:
    # We are launching from the command line with one or both parameters set.
    file_arg = sys.argv[1]
    test_arg = sys.argv[2] if len(sys.argv) > 2 else None
    program = CLIProgram(file=file_arg, test=test_arg)
else:
    program = CLIProgram()
    program.start()



