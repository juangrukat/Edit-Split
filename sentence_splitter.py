#!/usr/bin/env python3

import argparse
import csv
import re
import os

def load_abbreviations(file_path):
    """
    Load abbreviations from a file into a set for quick lookup.
    If the file doesn't exist, return a default set of common abbreviations.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return {line.strip() for line in file if line.strip()}
    except FileNotFoundError:
        print(f"Warning: Abbreviations file '{file_path}' not found. Using default abbreviations.")
        # Return a default set of common abbreviations
        return {
            "Mr", "Mrs", "Ms", "Dr", "Prof", "Rev", "Hon", "St", "Sr", "Jr", 
            "e.g", "i.e", "etc", "vs", "a.m", "p.m", "U.S", "U.K", "U.N", 
            "Ph.D", "M.D", "B.A", "M.A", "B.Sc", "M.Sc", "Inc", "Ltd", "Co", 
            "Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Sept", "Oct", "Nov", "Dec"
        }

def preprocess_text(text):
    """
    Preprocess the text by normalizing whitespace and marking paragraph breaks.
    """
    # Replace multiple newlines with a special marker
    text = re.sub(r'\n\s*\n', '\n[PARAGRAPH BREAK]\n', text)
    # Replace single newlines with spaces
    text = re.sub(r'\n(?![PARAGRAPH BREAK])', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_into_sentences(text, abbreviations):
    """
    Split text into sentences while handling various edge cases.
    """
    sentences = []
    current_sentence = ""
    
    # Split text by paragraph breaks first
    paragraphs = text.split('[PARAGRAPH BREAK]')
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
            
        # Process each paragraph
        i = 0
        while i < len(paragraph):
            char = paragraph[i]
            current_sentence += char
            
            # Check for potential sentence endings
            if char in '.!?':
                # Look ahead to determine if this is a real sentence ending
                next_chars = paragraph[i+1:i+20] if i+1 < len(paragraph) else ""
                
                # Check if we're inside quotes or parentheses
                open_quotes = current_sentence.count('"') % 2 != 0
                open_parens = current_sentence.count('(') > current_sentence.count(')')
                
                # Check for ellipsis
                is_ellipsis = False
                if char == '.' and i+2 < len(paragraph) and paragraph[i+1:i+3] == '..':
                    is_ellipsis = True
                    current_sentence += paragraph[i+1:i+3]
                    i += 2  # Skip the next two dots
                
                # Check if this is an abbreviation
                is_abbr = False
                # Check for abbreviations with periods
                if char == '.':
                    # Get the last word in the current sentence
                    words = current_sentence.strip().split()
                    if words:
                        last_word = words[-1]
                        
                        # Check for multi-part abbreviations with periods (Ph.D., U.S.A., etc.)
                        # This pattern matches words like Ph.D. where periods separate letters
                        if re.match(r'^([A-Za-z]+.)([A-Za-z]+.)+$', last_word) or re.match(r'^([A-Za-z].)([A-Za-z].)+$', last_word):
                            is_abbr = True
                        # Check for single-letter abbreviations (p. in p.m., etc.)
                        elif len(last_word) == 2 and last_word[0].isalpha() and last_word[1] == '.':
                            is_abbr = True
                        # Check if we're in the middle of a multi-part abbreviation (like Ph. in Ph.D.)
                        elif i+2 < len(paragraph) and paragraph[i+1].isalpha() and paragraph[i+2] == '.':
                            # Look ahead to see if this might be part of a multi-part abbreviation
                            is_abbr = True
                        # Check against our abbreviation list
                        else:
                            # Remove trailing period for comparison
                            word_without_period = last_word.rstrip('.')
                            if word_without_period in abbreviations:
                                is_abbr = True
                            # Also check if the word with period is in abbreviations
                            elif last_word in abbreviations:
                                is_abbr = True
                
                # Determine if this is a sentence end
                if (not open_quotes and not open_parens and not is_abbr and 
                   (not is_ellipsis or (is_ellipsis and re.match(r'^\s*[A-Z]', next_chars.lstrip())))):
                    
                    # Check for dialogue attribution
                    if re.search(r'^\s*"[^"]+[.!?]"\s*[a-z]', current_sentence):
                        # This might be dialogue attribution, continue
                        pass
                    else:
                        # This is a sentence end
                        sentences.append(current_sentence.strip())
                        current_sentence = ""
            
            i += 1
        
        # Add any remaining text in the paragraph
        if current_sentence.strip():
            sentences.append(current_sentence.strip())
            current_sentence = ""
        
        # Add paragraph break if this isn't the last paragraph
        if paragraph != paragraphs[-1]:
            sentences.append("[PARAGRAPH BREAK]")
    
    return sentences

def write_to_csv(sentences, output_file):
    """
    Write sentences to a CSV file, one sentence per row.
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for sentence in sentences:
            writer.writerow([sentence])

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Split text into sentences and save to CSV.')
    parser.add_argument('input_file', help='Path to the input text file')
    parser.add_argument('output_file', help='Path to the output CSV file')
    parser.add_argument('--abbr', default='abbreviations.txt', 
                        help='Path to abbreviations file (default: abbreviations.txt)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        return 1
    
    # Load abbreviations
    abbreviations = load_abbreviations(args.abbr)
    
    # Read input file
    try:
        with open(args.input_file, 'r', encoding='utf-8') as file:
            text = file.read()
    except Exception as e:
        print(f"Error reading input file: {e}")
        return 1
    
    # Process text
    preprocessed_text = preprocess_text(text)
    sentences = split_into_sentences(preprocessed_text, abbreviations)
    
    # Write output
    try:
        write_to_csv(sentences, args.output_file)
        print(f"Successfully processed {len(sentences)} sentences to {args.output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())