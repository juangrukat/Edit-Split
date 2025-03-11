# Sentence Splitter

A Python utility for intelligently splitting text into sentences while handling various edge cases like abbreviations, quotations, ellipses, and more.

## Overview

The Sentence Splitter is a command-line tool that processes text files and splits them into individual sentences, saving the output to a CSV file. It's designed to handle complex text with various punctuation patterns, abbreviations, quotations, and other edge cases that make sentence splitting challenging.

## Features

- Smart Sentence Detection: Properly identifies sentence boundaries while handling:
  - Abbreviations (e.g., "Dr.", "Ph.D.", "U.S.A.")
  - Quotations and nested quotes
  - Parenthetical expressions
  - Ellipses (...)
  - Dialogue attribution
  - Multi-part abbreviations

- Paragraph Preservation: Maintains paragraph structure in the output with special markers

- Customizable Abbreviations: Comes with an extensive list of common abbreviations that can be extended

## Requirements

- Python 3.x
- No external dependencies (uses only standard library modules)

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.x installed
3. No additional installation steps required

## Usage

```bash
python sentence_splitter.py input_file.txt output_file.csv [--abbr abbreviations.txt]
```

### Arguments

- `input_file.txt`: Path to the input text file you want to process
- `output_file.csv`: Path where the output CSV file will be saved
- `--abbr abbreviations.txt`: Optional path to a custom abbreviations file (defaults to 'abbreviations.txt')

### Example

```bash
python sentence_splitter.py test_input.txt output.csv
```

## Input Format

The input should be a plain text file. The program handles:

- Multiple paragraphs (separated by blank lines)
- Various punctuation patterns
- Quoted text
- Text with abbreviations

See `test_input.txt` for an example of supported text formats.

## Output Format

The output is a CSV file where each row contains a single sentence. Paragraph breaks are preserved with the special marker `[PARAGRAPH BREAK]`.

## Customizing Abbreviations

The program uses a list of common abbreviations to avoid incorrectly splitting sentences at periods that are part of abbreviations. You can customize this list by:

1. Editing the included `abbreviations.txt` file
2. Creating your own abbreviations file and specifying it with the `--abbr` option

The abbreviations file should contain one abbreviation per line. Both forms (with and without periods) are supported.

## How It Works

The sentence splitter works through several steps:

1. Preprocessing: Normalizes whitespace and marks paragraph breaks
2. Abbreviation Loading: Loads a set of abbreviations from the specified file
3. Sentence Splitting: Processes text character by character, identifying sentence boundaries while handling edge cases
4. Output Generation: Writes the resulting sentences to a CSV file

## Edge Cases Handled

The splitter correctly handles many challenging cases:

- Abbreviations with periods ("Dr.", "Ph.D.", "U.S.A.")
- Sentences ending with quotation marks
- Ellipses at sentence boundaries
- Parenthetical expressions
- Dialogue with attribution ("Hello," she said.)
- Multi-part abbreviations (Ph.D., U.S.A.)

## Limitations

- Very complex nested quotations might not be handled perfectly
- Some rare abbreviation patterns might need to be added to the abbreviations list
- The program assumes well-formed input text

## License

Feel free to use, modify, and distribute this code as needed.