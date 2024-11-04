from itertools import zip_longest
import heapq
from bi_search import minimum_keyboard_distance

OFFSET = 2


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


#by using bidirectional search between keyboard keys we can somewhat quickly establish if they are close by
def levenshtein_distance_updated(s1, s2):
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            cost = min(insertions, deletions, substitutions)
            if substitutions == cost:
                if minimum_keyboard_distance(c1, c2) <= OFFSET:
                    current_row.append(previous_row[j])
            else: current_row.append(cost)
        previous_row = current_row

    return previous_row[-1]


def ind_distance(s1, s2):
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2) * 2
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def hamming_distance(s1, s2):
    if len(s1) != len(s2):
        return -1
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def hamming_distance_updated(s1, s2):
    if len(s1) != len(s2):
        return -1
    return sum((c1 != c2) * min(max(minimum_keyboard_distance(c1, c2) - OFFSET, 0), 1) for c1, c2 in zip(s1, s2)) #adds 0 if keys are withing OFFSET jumps of each other


def indel_distance(s1, s2):
    return abs(len(s1) - len(s2))


def suggest_word(word, dictionary):
    heap = []
    for dict_word in dictionary:
        dist = levenshtein_distance(word, dict_word)
        heapq.heappush(heap, (dist, dict_word))

    return heapq.heappop(heap)[1]


def correct_text(input_file, output_file, dictionary):
    with open(input_file, 'r') as file:
        words = file.read().split()

    corrected_words = [suggest_word(word, dictionary) for word in words]

    with open(output_file, 'w') as file:
        file.write(' '.join(corrected_words))


def load_dictionary(dictionary_file):
    with open(dictionary_file, 'r') as file:
        dictionary = set(file.read().split())
    return dictionary


def start(input_file, output_file, dictionary_file):
    dictionary = load_dictionary(dictionary_file)
    correct_text(input_file, output_file, dictionary)


str1 = "pom dor"
str2 = "pomidor"
distance = ind_distance(str1, str2)
print("Indel Distance:", distance)
distance = levenshtein_distance(str1, str2)
print("Levenshtein Distance:", distance)
#distance = levenshtein_distance_updated(str1, str2)
#print("Levenshtein Distance Updated:", distance)
distance = hamming_distance(str1, str2)
print("Hamming Distance:", distance)
#distance = hamming_distance_updated(str1, str2)
#print("Hamming Distance Updated:", distance)
#start('input.txt', 'corrected.txt', 'words_alpha.txt')