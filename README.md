# Finite Automaton Reader Command Line Application

This command-line application allows you to read and test strings against deterministic finite automata (DFAs) and non-deterministic finite automata (NFAs) stored in a file. It also provides functionality to track routes through the automaton.

## Prerequisites

Make sure you have the following dependencies installed:

- Python 3.x

## Installation

1. Clone the repository:

```shell
git clone <repository_url>
```

2. Navigate to the project directory:

```shell
cd <project_directory>
```

3. (Optional) Create and activate a virtual environment:

```shell
python -m venv venv
source venv/bin/activate
```

4. Install the required dependencies:

```shell
pip install -r requirements.txt
```

## Usage

You can use the application through the command-line interface. Available commands are:

- `exit`: Exit the program.
- `load <file_path>`: Load a DFA/NFA from a text file.
- `test <input_string>`: Test an input string against the loaded DFA/NFA.
- `lastpath`: Print the last path used to process a string through the DFA/NFA.
- `info`: Print information about the loaded DFA/NFA.
- `help`: Display the list of available commands.

To run the application, execute the following command:

```shell
python <filename.py>
```

Replace `<filename.py>` with the name of the Python file containing the code.

### Examples

Here are some examples of how to use the application:

- Load a DFA/NFA from a file:

  ```shell
  load example.txt
  ```

  Replace `example.txt` with the path to the file containing the automaton.

- Test an input string against the loaded DFA/NFA:

  ```shell
  test abc
  ```

  Replace `abc` with the input string you want to test.

- Print the last path used to process a string through the DFA/NFA:

  ```shell
  lastpath
  ```

- Print information about the loaded DFA/NFA:

  ```shell
  info
  ```

- Exit the program:

  ```shell
  exit
  ```

## File Format

The DFA/NFA file should follow a specific format. Here is an example of the format (labels omitted):

```
Alphabet:      a,b,c
States:        q0,q1,q2,q3
Start State:   q0
Accept States: q3
Transitions:   (q0,a)->q1
               (q1,b)->q2
               (q2,c)->q3
```

- The `Alphabet` line lists the symbols in the alphabet, separated by commas.
- The `States` line lists all the states in the automaton, separated by commas.
- The `Start State` line specifies the start state of the automaton.
- The `Accept States` line lists the accept states of the automaton, separated by commas.
- The `Transitions` section defines the transitions between states. Each transition is specified on a separate line in the format `(source_state,input_symbol)->target_state`.

Note: For NFAs, if a state has more than one possible exit for the same input symbol, simply list it as such.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

This application was developed using the DFA/NFA object implementation provided in the code.
