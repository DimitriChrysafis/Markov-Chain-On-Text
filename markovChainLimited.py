import os
import re
import random
from collections import Counter

def find_words_after(word, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()
        pattern = re.compile(rf'\b{re.escape(word)}\s+(\w+)\b')
        words_after_word = pattern.findall(text)
        return words_after_word

def find_top_n_after_excluding(word, folder_path, exclude_list, n=3):
    word_counter = Counter()
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            words_after_word = find_words_after(word, file_path)
            word_counter.update(words_after_word)
    for excluded_word in exclude_list:
        if excluded_word in word_counter:
            del word_counter[excluded_word]
    most_common_words = word_counter.most_common(n)
    return most_common_words

folder_path = "articles"
current_word = "the"
iterations = 100
all_picked_words = []

for _ in range(iterations):
    top_3_words = find_top_n_after_excluding(current_word, folder_path, all_picked_words, n=3)
    unused_words = [word for word, _ in top_3_words if word not in all_picked_words]
    if not unused_words:
        break
    most_common_word = random.choice(unused_words)
    print(f"The most common word after '{current_word}' is '{most_common_word}'.")
    current_word = most_common_word
    all_picked_words.append(most_common_word)
