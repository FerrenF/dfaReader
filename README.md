# DFA Reader Command Line Application

This is a command-line application that allows you to read and interact with a deterministic finite automaton (DFA). The program enables you to test strings against the DFA and track the routes through the automaton.

## How to Use

To run the program, execute the following command:

```python
python <filename>.py [file_path] [input_string]
```

If `file_path` and `input_string` are not provided, you can load the DFA and interact with it through the command-line interface.

## Commands

The following commands are available:

- `exit`: Exit the program.
- `load <file_path>`: Load a DFA from a text file.
- `test <input_string>`: Test an input string against the loaded DFA.
- `lastpath`: Print the last path used to process a string through the DFA.
- `info`: Print information about the loaded DFA.
- `help`: Display the list of available commands.

## DFAObject Class

The `DFAObject` class represents a deterministic finite automaton. It stores information about the DFA, such as the alphabet, states, start state, accept states, and transitions.

### Methods

- `has_transition(source_state, input_symbol)`: Checks if a transition exists from the `source_state` with the given `input_symbol`.
- `test_string(input_string)`: Tests the `input_string` against the DFA and returns `True` if it is accepted, `False` otherwise.
- `print_last_path()`: Prints a human-friendly readout of the last path taken through the DFA during the last test.
- `__str__()`: Returns a string representation of the DFA object.

## DFAFromFile Class

The `DFAFromFile` class is a convenience class that initializes a `DFAObject` directly from a file path. It reads the DFA information from the file and creates the DFA object accordingly.

### Method

- `__init__(file_path)`: Initializes the DFA object by reading the DFA information from the specified `file_path`.

## CLIProgram Class

The `CLIProgram` class represents the command-line interface for the DFA reader application.

### Methods

- `start()`: Starts the command-line interface and waits for user commands.
- `process_command(command)`: Processes the user command and performs the corresponding action.
- `load_file(file_path)`: Loads a DFA from the specified `file_path`.
- `test_function(arguments)`: Tests the `arguments` string against the loaded DFA.
- `__init__(**kwargs)`: Initializes the CLI program, optionally loading a DFA file and performing a test.

Note: The code provided at the end of the README allows for running the program from the command line with optional file and input string arguments.

---

This README provides a brief overview of the DFA reader command-line application. For more detailed information, please refer to the code comments and the class and method documentation within the source code.