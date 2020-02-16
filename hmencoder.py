import textwrap 
import sys

# Get contents of file to be encoded
inputFile = sys.argv[1]
with open(inputFile) as file:
    contents = file.read()

# Create sorted database of every symbol and its frequency of occurence
charFreq = {}
for ch in contents:
    if ch in charFreq:
        charFreq[ch] = charFreq[ch] + 1
    else:
        charFreq[ch] = 1
db = sorted( charFreq.items(), key = lambda x: (x[1], x[0]) )

# initialize dictionary of codes for every symbol
codes = {}
for ch in db:
    codes[ ch[0] ] = ''  

# Begin code generation process
while ( len(db) > 1):
    # Maintain sorted database and pull least value symbols to eliminate ambiguity
    db = sorted( db, key = lambda x: (x[1], x[0]) )
    t1 = db.pop(0)
    t2 = db.pop(0)
    left, right = sorted([t1, t2])

    # Generate encoding for symbol according to position in tree
    for ch in left[0]:
        codes[ch] = '0' + codes[ch]
    for ch in right[0]:
        codes[ch] = '1' + codes[ch]

    # Create new node, which is parent of "left" and "right"
    # children from above, and append to database
    newString = left[0] + right[0]
    newFreq = left[1] + right[1]
    newNode = (newString, newFreq)
    db.append(newNode)

# Encode message
encodedMsg = ''
for ch in contents:
    encodedMsg = encodedMsg + codes[ch]

# Format and write encoded string to file "encodemsg.txt"
wrapper = textwrap.TextWrapper(width=80)
lines = wrapper.wrap(text=encodedMsg)
with open("encodemsg.txt", "w") as f:
    for i in range(len(lines) - 1):
        print(lines[i], file=f)
    print(lines[len(lines)-1], end='', file=f)

# Store codewords and average number of bits for each symbol
codes = sorted(codes.items(), key = lambda x: x[0])
sumFreq = 0
sumLenxFreq = 0
with open("code.txt", "w") as f: 
    for index in range(len(codes)):
        if codes[index][0] == ' ':
            line = "Space: " + codes[index][1]
            print(line, file=f)
            temp = charFreq.get(codes[index][0])
            sumFreq = sumFreq + temp 
            prod = len(codes[index][1]) * temp
            sumLenxFreq = sumLenxFreq + prod
        else:
            line = codes[index][0] + ": " + codes[index][1]
            print(line, file=f)
            temp = charFreq.get(codes[index][0]) 
            sumFreq = sumFreq + temp 
            prod = len(codes[index][1]) * temp
            sumLenxFreq = sumLenxFreq + prod
    avg = str(round((sumLenxFreq/sumFreq), 2))
    print("Ave = " + avg + " bits per symbol", end='', file=f)

