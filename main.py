import json
import os
import sys

# DFA Reader Command Line Application
# This program reads a deterministic finite automaton from a file and then allows
# the user to test strings against it and track routes through an automaton.


# DFAObj -> DFAFromFile
# This object stores information about a deterministic finite automaton.
# It's not a new method of doing so, but it is the simplest by far.
# Other ways this could be implemented: a regular list, a linked list, a directional graph, an
# AnyTree with a little finagle, or even a vector database. That's an interesting idea.

class DFAObject:

    def has_transition(self, source_state, input_symbol):
        return (source_state, input_symbol) in self.transitions.keys()

    def test_string(self, input_string):
        self.last_path.clear()

        def ap_exit(cs, ch):
            self.last_path.append({(cs, ch): "none"})
            return False

        current_state = self.start_state
        for char in input_string:
            if not self.has_transition(current_state, char):
                ap_exit(current_state,char)
                return False
            target_state = self.transitions[(current_state, char)]
            self.last_path.append({(current_state, char): target_state})
            current_state = target_state
        return current_state in self.accept_states or ap_exit(current_state, input_string[-1:])

    # To a more usable library this should be split by its function but it is useful to both read and format here
    # print_last_path prints a human friendly readout of the last path taken through the network of all possibilities in
    # the last test.
    def print_last_path(self):
        result = []
        step = 0
        for dictionary in self.last_path:
            step += 1

            start_string = 'start ' if step == 1 else ''
            finalize_string = ''

            for (key, value) in dictionary.items():
                if step == len(self.last_path):
                    finalize_string = 'and is '
                    if value.strip() == 'none':
                        finalize_string += 'rejected'
                    else:
                        finalize_string += 'accepted'
                result.append(f"{step}: {start_string}state {' input '.join(map(str, key))} moves to state {value} {finalize_string}")

        return result

    def __init__(self, alphabet, all_states, start_state, accept_states, transitions=None):
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions or {}
        self.last_path = []
        self.alphabet = alphabet
        self.states = all_states

        # Prints the information that makes up this object. This can get pretty unreadable so we use
        # built-in json functions to prettyprint it.

    def __str__(self):
        return json.dumps({
            "alphabet": self.alphabet,
            "states": self.states,
            "accept_states": self.accept_states,
            "transitions": [f"{':'.join(map(str, key))}->{value}" for key, value in self.transitions.items()]
        }, separators=(',', '='), indent=1)

# A convenience class to initialize a DFAObj directly from a file path.
class DFAFromFile(DFAObject):
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        alphabet = lines[0][1:-1].split(',')
        states = lines[1][1:-1].split(',')
        start_state = lines[2]
        accept_states = lines[3][1:-1].split(',')
        transitions = {}

        for line in lines[4:]:
            parts = line.split('->')
            input_function = parts[0][1:-1].split(',')
            source_state = input_function[0]
            input_symbol = input_function[1]
            destination_state = parts[1]
            transitions[(source_state, input_symbol)] = destination_state

        super().__init__(alphabet, states, start_state, accept_states, transitions)


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
            elif parts[0] == "test":
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
                print("load <file_path>: Load a DFA from a text file.")
                print("test <input_string>: Test an input string against the loaded DFA.")
                print("lastpath: Print the last path used to process a string through the DFA.")
                print("info: Print information about the loaded DFA.")
            else:
                print("Invalid command.")

    def load_file(self, fa):
        if not os.path.exists(fa):
            print("Error: File does not exist")
            return
        self.dfa = DFAFromFile(fa)
        print("DFA Loaded: "+fa)

    def test_function(self, arguments):
        print("Testing function with string:", arguments)
        is_accepted = self.dfa.test_string(arguments)

        if is_accepted:
            print("String accepted by the DFA.")
        else:
            print("String not accepted by the DFA.")

    def __init__(self, **kwargs):
        self.running = False
        self.dfa = None

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



