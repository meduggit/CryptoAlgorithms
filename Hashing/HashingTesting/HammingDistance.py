def hamming_distance(str1, str2):
    """Calculate the Hamming distance between two strings."""
    if len(str1) != len(str2):
        raise ValueError("Strings must be of equal length")
    
    # Initialize distance counter
    distance = 0
    
    # Calculate Hamming distance
    for ch1, ch2 in zip(str1, str2):
        # XOR the ASCII values of characters and count set bits
        distance += bin(ord(ch1) ^ ord(ch2)).count('1')
    
    return distance

# Example usage:
string1 = "u\x82\xcf\x08/\x02\x0ci\x06\x99\xa7\xa0\x96\xdf\xedp\x92\x85\xeb\xbe\xfb\x9b(\xcd.\xc0\x00y\x07\x00\xbc\x13\xfcv#\xe1\xd5\xd7\xb9U,\xa5S\x98\x9aMeT#\x91\x1fu\xa6/zg\xfd\x0b\xf3E\xccjT\x866~\xb9:\xf0\xed"
string2 = "\xf4\xbc\x90\x8c\xc0\x88G\xa2\xe6f\xa8\xac\x85p\x0e\xf9u\xd7\xfc\xaa\x01\x03\xbb\x07\xe4#w{l\xde\x8fe\xf0$#1j\x91;\x86cnS\xbb\xcd \xbfT# +\x95\xa7\x18\xb1x \xb9JENnT\x0bWe\xd7\xc8\xb24"
distance = hamming_distance(string1, string2)
print(f"The Hamming distance between '{string1}' and '{string2}' is {distance}.")
