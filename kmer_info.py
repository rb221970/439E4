"""
kmer_info.py

A python script that, given a user specified value 'k' 
and a text file of sequence fragments: 
- finds and counts each k-mer 
- finds and counts its immediate subsequent k-mer
then exports the results into another file. 

"""

# -- IMPORTS --
# argparse, to specify and use the command-line flags
import argparse


# -- FUNCTION: parse_args() --
# a function that sets command-line flags/arguments
# that allows the user to specify input, output, and 'k' value
def parse_args():
    """
    parse_args

    A function that interprets commandline flags/arguments for 'kmer_info'

    Returns an instance of argparse.Namespace containing 
    input, output, and size (where size is k).

    """

    # to initiate parser
    parser = argparse.ArgumentParser(
        description="Count k‐mers and its subsequents given a file of sequences"
    )

    # defines argument for k, gets accessed by '.size'
    parser.add_argument(
        '-k', '--size',
        type=int,
        required=True,
        help='Numerical value to specify string length of k-mer'
    )

    # defines argument for input file
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='To specify input file for sequence fragments'
    )

    # defines argument for output file
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='To specify output file to store test results'
    )

    # returns as an object
    return parser.parse_args()


# -- FUNCTION: read_sequences() --
# a function that reads an input file of genome sequences line by line
# strips each line, returns them in uppercase 
# stores the results in a list called 'sequences'
def read_sequences(input_file):
    """
    read_sequences

    A function that reads in a file of sequenced genome fragments line by line, 
    stripping whitespaces and skipping empty lines. 

    Returns the sequence strings in all uppercase characters. 

    """

    # define sequences
    sequences = []

    with open(input_file, 'r') as infile: # access and read file
        for line in infile: # for each line in the file
            seq = line.strip().upper() # strip the line, make it uppercase, set it to 'seq'
            if seq: # skip the blank lines
                sequences.append(seq) # add that stripped string to the 'sequences' list
    
    # return the 'sequences' list
    return sequences


# -- FUNCTION: get_info() --
# a function that takes the sequences and the k value to
# count the frequencies of found k-mers and their subsequents
# using a dictionary
def get_info(sequences, k):
    """
    get_info

    A function that uses the 'sequences' list and the specified value k
    to count total frequency for each k-mer and its subsequent k-mer.

    Returns each k-mer in a dict called 'stats', the count of the k-mers and their subsequents.

    """
    stats = {} 

    # if a genome sequence is shorter than k, skip it
    for seq in sequences:
        if len(seq) < k:
            continue

        # a loop that gets 'k' consecutive characters and stores it as 'kmer'
        # then checks the character after the k-mer, 'next_base'
        # https://www.geeksforgeeks.org/window-sliding-technique/
        for i in range(len(seq) - k):
            kmer = seq[i:i+k]
            next_base = seq[i+k]

            # put the k-mer into the dict if its not there already
            # and increase the count
            if kmer not in stats:
                stats[kmer] = {'count': 0, 'followers': {}}
            stats[kmer]['count'] += 1

            # add the first character after the selected k-mer, 'followers',
            # to the dict if its not there already
            # and increase the count
            if next_base not in stats[kmer]['followers']:
                stats[kmer]['followers'][next_base] = 0
            stats[kmer]['followers'][next_base] += 1

        # after looping through all 'k' consecutive characters 
        # add the last k-mer to the count as well
        last_kmer = seq[-k:]
        if last_kmer not in stats:
            stats[last_kmer] = {'count': 0, 'followers': {}}
        stats[last_kmer]['count'] += 1

    # return the dict
    return stats

# -- FUNCTION: output_info() --
# a function that takes the 'stats' dict and the output file name
# to output the results into a file
def output_info(stats, output_file):
    """
    output_info

    A function that outputs the results of get_info into a specified output file

    Returns the output file with the results

    """

    # start an output file with labeled headers
    with open(output_file, 'w') as outfile:
        outfile.write("kmer,total_count,follower_base,follower_count\n")

        # insertion order
        for kmer, data in stats.items():
            total = data['count']
            followers = data['followers']
            if followers:
                for base, cnt in followers.items():
                    outfile.write(f"{kmer},{total},{base},{cnt}\n")
            else:
                # no followers recorded
                outfile.write(f"{kmer},{total},-,-\n")

# -- MAIN --
def main():
    """
    main

    The main function to run the script using all of the above functions

    Returns the output result

    """

    # function calls
    args = parse_args()
    seqs = read_sequences(args.input)
    stats = get_info(seqs, args.size)
    output_info(stats, args.output)

if __name__ == '__main__':
    main()


