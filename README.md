# Hirschberg-Algorithm
Hirschberg Algorithm implementation for Sequence Alignment

This repository contains an implementation of the Hirschberg algorithm for sequence alignment in Python. The program can align sequences of characters or lines from files based on given scoring parameters.

## Description

The Hirschberg algorithm is a dynamic programming algorithm used to solve the Longest Common Subsequence problem in a memory-efficient way. This implementation can handle both character-level and line-level alignments. <br>
The assignment can be found [here](https://github.com/dmst-algorithms-course/assignment-2022-2/blob/main/assignment-2022-2.pdf)

## Usage

The program can be executed with various command-line arguments to specify the scoring system and input sequences or files.

### Command-Line Arguments

- `-t` (optional): Print every (i, j) index pair during the execution of the Hirschberg algorithm.
- `-f` (optional): Accept files as input.
- `-l` (optional): Match whole lines instead of characters.
- `gap`: The gap penalty (negative integer).
- `match`: The match score (integer).
- `differ`: The mismatch penalty (negative integer).
- `aa`: The first sequence (or filename if `-f` is specified).
- `bb`: The second sequence (or filename if `-f` is specified).

### Examples

1. Aligning two sequences of characters:
    ```sh
    python hirschberg.py -2 2 -1 AGTACGCA TATGC
    ```

2. Aligning sequences from files line-by-line:
    ```sh
    python hirschberg.py -f -l -2 1 -1 file1.txt file2.txt
    ```


## Implementation Details

The Python script `hirschberg.py` implements the Hirschberg algorithm. It uses dynamic programming to compute the alignment and can handle large sequences efficiently. The main functions and their purposes are as follows:

- `createf(a, b)`: Creates the dynamic programming table for alignment.
- `compare(a, b)`: Computes the score between two characters.
- `FinalScore(w1, z1)`: Computes the final alignment score.
- `ComputeAlignmentScore(a, b)`: Computes the alignment score for two sequences.
- `bestalignments(lw, lz)`: Finds the best alignments from all possible alignments.
- `hirschberg(a, b)`: The main function that implements the Hirschberg algorithm.

## Running the Program

To run the program, ensure you have Python 3 installed. Save the script as `hirschberg.py` and run it from the command line with the appropriate arguments as shown in the examples.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
