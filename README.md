# Finite Automaton Reader Command Line Application

This command-line application allows you to read and test strings against finite automatons. It supports deterministic finite automatons (DFA), non-deterministic finite automatons (NFA), and pushdown automatons (PDA).

## Caveats

The alphabet can not consist of words. Only single characters may exist in the alphabet.

You can push multiple symbols at once, however you cannot consume multiple symbols at once.

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

- Load an automaton from a file:

  ```shell
  load example.txt
  ```

  Replace `example.txt` with the path to the file containing the automaton.

- Test an input string against the loaded automaton:

  ```shell
  test abc
  ```

  Replace `abc` with the input string you want to test.

- Print the last path used to process a string through the automaton:

  ```shell
  lastpath
  ```

- Print information about the loaded automaton:

  ```shell
  info
  ```

- Exit the program:

  ```shell
  exit
  ```

## File Format

The automaton file should follow a specific format. Here is an example of the format (labels omitted):

An example format of a simple deterministic automaton would be as follows.
Multiple examples are included (pda.txt, marmalade.txt, and threezeros.txt)
```
Alphabet:      {a,b,c} // Comment
States:        {q0,q1,q2,q3}
// A discarded line
Start State:   q0
Accept States: {q3}
Transitions:   (q0,a)->q1
               (q1,b)->q2
               (q2,c)->q3
// The last comment is taken as a machine description.
```

- The `Alphabet` line lists the symbols in the alphabet, separated by commas.
- The `States` line lists all the states in the automaton, separated by commas.
- The `Start State` line specifies the start state of the automaton.
- The `Accept States` line lists the accept states of the automaton, separated by commas.
- The `Transitions` section defines the transitions between states. Each transition is specified on a separate line in the format `(source_state,input_symbol)->target_state`.

The format gets more complex for pushdown automatons:
Examples included in pda.txt, and twoandthree.txt.

```
Alphabet:         {0,1} // Comment 
Stack Alphabet:   {0,1}  
States:           {q1,q2,q3,q4}
Initial State:    q1  
Accept States:    {q4}
Transitions:      (q1,):(,$)->q2
                  (q2,):($,)->q4
// The last comment is taken as a machine description.
```

in addition to identical function above, there is one additional line that must be present for a PDA, and the formatting is extended.
- The `Stack Alphabet` line lists the symbols in the stack alphabet, separated by commas.
- The `Transitions` section follows the format:

  `(Source_State, Input Symbol):(Consume_Symbol, Push_Symbol) -> Result_State`
  - A consume operation is a pop operation.
  - You may push more than one character at once, but you may only consume one character at a time.
## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

This application was developed using the DFA/NFA object implementation provided in the code.
