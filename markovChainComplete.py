import os
import re
import random
from collections import Counter


def tokenize_text(text):
    text = text.lower()
    return re.findall(r'\b\w+\b', text)


def find_words_after(word, tokens):
    pattern = re.compile(rf'\b{re.escape(word)}\s+(\w+)\b')
    words_after_word = pattern.findall(" ".join(tokens))
    return words_after_word


def find_top_n_after_excluding(word, tokens, exclude_list, n=3):
    word_counter = Counter()
    words_after_word = find_words_after(word, tokens)
    word_counter.update(words_after_word)
    for excluded_word in exclude_list:
        if excluded_word in word_counter:
            del word_counter[excluded_word]
    most_common_words = word_counter.most_common(n)
    return most_common_words


file_path = "mega.txt"

# Read and preprocess text from the specified file
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()
    all_tokens = tokenize_text(text)

num_sentences = 100

for _ in range(num_sentences):
    current_word = "a"

    iterations = 10
    all_picked_words = []

    for _ in range(iterations):
        top_2_words = find_top_n_after_excluding(current_word, all_tokens, all_picked_words, n=2)

        unused_words = [word for word, _ in top_2_words if word not in all_picked_words]
        if not unused_words:
            break
        most_common_word = random.choice(unused_words)
        print(most_common_word, end=' ')
        current_word = most_common_word
        all_picked_words.append(most_common_word)

    print()
