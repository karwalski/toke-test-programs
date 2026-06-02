def lzw_compress(data):
    # Initialize dictionary with single characters
    dictionary = {}
    for i in range(256):
        dictionary[chr(i)] = i
    
    result = []
    w = ""
    dict_size = 256
    
    for c in data:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    
    if w:
        result.append(dictionary[w])
    
    return result

def lzw_decompress(codes):
    # Initialize dictionary with single characters
    dictionary = {}
    for i in range(256):
        dictionary[i] = chr(i)
    
    result = []
    dict_size = 256
    
    if not codes:
        return ""
    
    w = dictionary[codes[0]]
    result.append(w)
    
    for i in range(1, len(codes)):
        code = codes[i]
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            entry = w + w[0]
        else:
            raise ValueError("Invalid code")
        
        result.append(entry)
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    
    return ''.join(result)

# Read input
mode = input().strip()
data_line = input().strip()

if mode == "compress":
    codes = lzw_compress(data_line)
    print(' '.join(map(str, codes)))
elif mode == "decompress":
    codes = list(map(int, data_line.split()))
    result = lzw_decompress(codes)
    print(result)