"""
test_kmer_info.py

A script for typical test & edge cases for kmer_info.py

Each function has its purpose stated in the definition

Runs 11 cases total

"""

# -- IMPORTS -- 
import sys
import pytest
from pathlib import Path
from kmer_info import parse_args, read_sequences, get_info, output_info

# --- to test parse_args() ---
def test_parse_args(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "argv",
        ["kmer_info.py", "-k", "2", "-i", "foo.txt", "-o", "bar.tsv"])
    args = parse_args()
    assert args.size == 2
    assert args.input == "foo.txt"
    assert args.output == "bar.tsv"

# --- to test read_sequences() ---
# 3 cases: 
# one to ensure it works as intended
# one to see how it handles mixed case strings
# one to see how it handles empty inputs
# note: there is logic implemented to check for these cases as well
def test_read_sequences(tmp_path):
    p = tmp_path / "in.txt"
    p.write_text("AAA\n\nCCG\n")
    assert read_sequences(str(p)) == ["AAA", "CCG"]

def test_read_sequences_mixed_case(tmp_path):
    p = tmp_path / 'in2.txt'
    p.write_text('acgT\nttA\n')
    assert read_sequences(str(p)) == ['ACGT', 'TTA']

def test_empty_sequences_list():
    assert get_info([], 3) == {}

# --- to test get_info() ---
# 5 cases: 
# one to ensure it works as intended
# one to see how it handles when k = 1
# one to see how it handles when k = sequence length
# one to see how it handles when k > sequence length
# one to see how it handles when there are multiple sequences
# note: there is logic implemented to check for these cases as well
def test_get_info_basic():
    seqs = ["ATGT"]
    stats = get_info(seqs, 2)
    assert stats["AT"]["followers"]["G"] == 1
    assert stats["GT"]["count"] == 1

def test_get_info_k_equals_one():
    seqs = ['AAA']
    stats = get_info(seqs, 1)
    assert stats['A']['count'] == 3
    assert stats['A']['followers']['A'] == 2

def test_get_info_k_equals_length():
    seqs = ['ATG']
    stats = get_info(seqs, 3)
    assert stats == {'ATG': {'count': 1, 'followers': {}}}

def test_get_info_k_too_large():
    seqs = ['ACG']
    stats = get_info(seqs, 5)
    assert stats == {}

def test_get_info_multiple_sequences():
    seqs = ['ATAT', 'TATA']
    stats = get_info(seqs, 2)
    assert stats['AT']['count'] == 3
    assert stats['AT']['followers']['A'] == 2
    assert 'T' not in stats['AT']['followers']


# --- to test output_info() ---
# 2 cases: 
# one to ensure it works as intended
# one to ensure it maintains formatted output
def test_output_info_csv_format(tmp_path):
    stats = {'X': {'count': 2, 'followers': {'G': 1, 'C': 1}}, 'Y': {'count': 1, 'followers': {}}}
    out = tmp_path / 'o.csv'
    output_info(stats, str(out))
    lines = out.read_text().splitlines()
    assert lines[0] == 'kmer,total_count,follower_base,follower_count'
    assert 'X,2,G,1' in lines
    assert 'X,2,C,1' in lines
    assert 'Y,1,-,-' in lines

def test_output_info(tmp_path):
    stats = {'XX': {'count': 1, 'followers': {}}, 'YY': {'count': 2, 'followers': {'A': 2}}}
    out = tmp_path / 'out.csv'
    output_info(stats, str(out))
    lines = out.read_text().splitlines()
    assert lines[0] == 'kmer,total_count,follower_base,follower_count'
    assert 'XX,1,-,-' in lines
    assert 'YY,2,A,2' in lines