import json
import os
import sys

# DFA/NFA Reader Command Line Application
# This program reads a finite automaton from a file and then allows
# the user to test strings against it and track routes through.

# FAObj -> DFAObject
#       -> NFAObject


# This object stores information about a finite automaton.
# It can handle a DFA or a NFA
# We use seperate chaining in order to handle hash collisions (where a state has more than one possible exit)


class FAObject:

    def is_nfa(self):
        return self.isNFA
    def num_transitions(self, source_state, input_symbol):
        if not self.has_transition(source_state,input_symbol):
            return 0
        return len(self.transitions[(source_state, input_symbol)])

    def get_transitions(self, source_state, input_symbol):
        if self.has_transition(source_state,input_symbol):
            return self.transitions[(source_state, input_symbol)]
        return False

    def has_transition(self, source_state, input_symbol):
        return (source_state, input_symbol) in self.transitions.keys()

    def run_machine(self, start_state, input_string, path=None):

        if not path:
            path = list()
        if len(input_string):
            if not self.has_transition(start_state, input_string[0]):
                return False
            target_states = self.get_transitions(start_state, input_string[0])

            truths = []
            for target_state in target_states:
                # Only one truth in our table needs to be true for the string to be valid.
                truths.append(self.run_machine(target_state, input_string[1:], path+[(start_state, input_string[0], target_state)]))
            if True in truths:
                return True
        else:
            if start_state in self.accept_states:
                # If we are here, then we are at the end of the string and also in a state which we can accept. Ding ding ding.
                self.last_path = path + [(start_state, "", "accept")]
                return True
        return False

    def test_string(self, input_string):
        self.last_path.clear()



        return self.run_machine(self.start_state, input_string)

    # To a more usable library this should be split by its function but it is useful to both read and format here
    # print_last_path prints a human friendly readout of the last path taken through the network of all possibilities in
    # the last test.
    def print_last_path(self):
        result = []
        step = 0
        for (start_state, input_string, target_state) in self.last_path:

            step += 1
            start_string = 'start ' if step == 1 else ''
            finalize_string = ''
            if step == len(self.last_path):
                finalize_string = 'and is '
                if target_state == 'accept':
                    finalize_string += 'accepted'
                else:
                    finalize_string += 'rejected'
            result.append(
                    f"{step}: {start_string}state {start_state} takes input '{input_string}'"
                    f" and moves to state {target_state} {finalize_string}")
        return result

    def __init__(self, alphabet, all_states, start_state, accept_states, transitions=None, isNFA=False):
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions or {}
        self.last_path = []
        self.alphabet = alphabet
        self.states = all_states
        self.isNFA = isNFA
        # Prints the information that makes up this object. This can get pretty unreadable so we use
        # built-in json functions to prettyprint it.

    def __str__(self):
        return json.dumps({
            "alphabet": self.alphabet,
            "states": self.states,
            "accept_states": self.accept_states,
            "transitions": [f"{':'.join(map(str, key))}->{value}" for key, value in self.transitions.items()]
        }, separators=(',', '='), indent=1)

class FAFromFile(FAObject):
    def __init__(self, file_path):

        self.source = file_path
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        if len(lines) < 4:
            print(
                "This might not be a working machine. Creating a default machine with dfa.txt instead.")
            self.__init__("dfa.txt")
            self.source = "dfa.txt"
            return
        alphabet = lines[0][1:-1].split(',')
        states = lines[1][1:-1].split(',')
        start_state = lines[2]
        accept_states = lines[3][1:-1].split(',')
        transitions = {}
        collision = False
        index = 5

        for line in lines[4:]:
            parts = line.split('->')
            if len(parts) < 2:
                print("Bad transition entry found at line " + index.__str__() + ". Discarding this line. WARNING: you may not have a working machine.")
                continue
            index += 1
            input_function = parts[0][1:-1].split(',')
            if len(input_function) < 2:
                print(
                    "Bad transition entry found at line " + index.__str__() + ". Discarding this line. WARNING: you may not have a working machine.")
                continue
            source_state = input_function[0]
            input_symbol = input_function[1]
            destination_state = parts[1]
            if (source_state, input_symbol) in transitions:
                # We have a hash collision and must start separate chaining destination states.
                # This means that the object we are reading is actually an NFA, so we flag it to specify such.
                collision = True
                transitions[(source_state, input_symbol)].append(destination_state)
            else:
                transitions[(source_state, input_symbol)] = [destination_state]

        super().__init__(alphabet, states, start_state, accept_states, transitions, isNFA=collision)

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
                print("load <file_path>: Load a DFA/NFA from a text file.")
                print("test <input_string>: Test an input string against the loaded DFA/NFA.")
                print("lastpath: Print the last path used to process a string through the DFA/NFA.")
                print("info: Print information about the loaded DFA/NFA.")
            else:
                print("Invalid command.")

    def load_file(self, fa):
        if not os.path.exists(fa):
            print("Error: File does not exist")
            return
        self.dfa = FAFromFile(fa)
        self.falabel = "NFA" if self.dfa.is_nfa() else "DFA"
        print(self.falabel + " Loaded: "+self.dfa.source)

    def test_function(self, arguments):
        print("Testing function with string:", arguments)
        is_accepted = self.dfa.test_string(arguments)

        if is_accepted:
            print(f"String accepted by the {self.falabel}.")
        else:
            print(f"String not accepted by the {self.falabel}.")

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



