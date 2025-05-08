# kmer_info.py
## A python assessment for DSP439

### Introduction
A Python script used to assess sequenced genome fragments by counting both the frequency of substrings of length *k* (known as **k-mers**), and the character that follows it, and then returns those results in a text file. 

### Requirements
- Python 3.6+
- [pytest](https://docs.pytest.org/en/stable/)

### Usage
```bash
python kmer_info.py -k <k> -i <input_file> -o <output_file>
```
* `-k <k>`: Length of each k-mer
* `-i <input_file>`: Path to a text file where each line is a genome fragment only containing the letters A, C, T, or G
* `-o <output_file>`: Path where the output results are returned

### Output
1. **kmer**: The k-length substring
2. **total\_count**: Frequency of the k-mer 
3. **follower\_base**: The character that follows this k-mer (ouputs as `-` if there are none).
4. **follower\_count**: Frequency of the subsequent character

## Testing
To run the built-in pytest suite:
```bash
pytest kmer_info.py
```
