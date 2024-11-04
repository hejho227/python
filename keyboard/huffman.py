import heapq
from collections import Counter, defaultdict

class TreeNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def calculate_frequency(input_string):
    freq = Counter(input_string)
    return freq


def build_huffman_tree(freq):
    priority_queue = [TreeNode(char, freq) for char, freq in freq.items()]
    heapq.heapify(priority_queue)
    
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        
        internal_node = TreeNode(freq=left.freq + right.freq)
        internal_node.left = left
        internal_node.right = right
        
        heapq.heappush(priority_queue, internal_node)
    
    return heapq.heappop(priority_queue)


def generate_huffman_codes(root):
    if not root:
        return {}
    
    codes = {}
    
    def dfs(node, code):
        if node:
            if node.char is not None:
                codes[node.char] = code
            dfs(node.left, code + '0')
            dfs(node.right, code + '1')
    
    dfs(root, '')
    return codes


def huffman_encoding(input_string):
    freq = calculate_frequency(input_string)
    if len(freq) == 1:
        char = next(iter(freq))
        huffman_codes = {char: '0'}
        encoded_string = ''.join(huffman_codes[char] for char in input_string)
    else:
        root = build_huffman_tree(freq)
        huffman_codes = generate_huffman_codes(root)
        encoded_string = ''.join(huffman_codes[char] for char in input_string)
    
    return encoded_string, huffman_codes


def huffman_decoding(encoded_string, huffman_codes):
    if not encoded_string:
        return ""
    
    reverse_codes = {v: k for k, v in huffman_codes.items()}
    decoded_string = []
    current_code = ""
    
    for bit in encoded_string:
        current_code += bit
        if current_code in reverse_codes:
            decoded_string.append(reverse_codes[current_code])
            current_code = ""
    
    return ''.join(decoded_string)


def calculate_compression_ratio(original_size, encoded_size):
    if original_size == 0:
        return 0.0
    return (1 - encoded_size / original_size) * 100


def main():
    input_string = "I love data structures"
    encoded_string, huffman_codes = huffman_encoding(input_string)
    
    print(f"Original string: {input_string}")
    print(f"Encoded string: {encoded_string}")
    print("Huffman Codes:")
    for char, code in sorted(huffman_codes.items()):
        print(f"{char}: {code}")
    
    original_size = len(input_string) * 8
    encoded_size = len(encoded_string)
    compression_ratio = calculate_compression_ratio(original_size, encoded_size)
    
    print(f"\nCompression ratio: {compression_ratio:.2f}%")
    
    decoded_string = huffman_decoding(encoded_string, huffman_codes)
    print(f"\nDecoded string: {decoded_string}")

if __name__ == "__main__":
    main()
