import numpy as np

measurements = 10
propability = 0.1
treshold = 3

x_block_size = 3
y_block_size = 2

x_size = 15
y_size = 10


def random_data():
    data = np.zeros((y_size,x_size))

    rows = data.shape[0]
    cols=data.shape[1]

    for r in range(rows):
        for c in range(cols):
            rn = np.random.choice(np.arange(0,2), p=[1 - propability, propability])
            data[r, c] = rn
    return data
    
sum_data = np.zeros((y_size,x_size))

for i in range(measurements):
    data = random_data()
    sum_data += data
    
print(sum_data)
print(np.max(sum_data))


print("VAR 1 - SUMMING QUANTITIES BY COORDINATES")
res = np.where(sum_data >=treshold)
#res = np.where(sum_data == np.max(sum_data))
data_noise = np.where(sum_data == measurements)

if len(data_noise[0])>0:
    print("DATA NOISE: \ny, x")
    for y,x in zip(data_noise[0], data_noise[1]):
        print(y,x)
    print("="*10)
        
if len(res)>0:
    print("VISITED OVER {} TIMES:".format(treshold))
    print(res)
    print("y, x:")
    for y,x in zip(res[0], res[1]):
        print(y,x)


print("\nVAR 2 - SUMMING QUANTITIES USING SPECIFIED BLOCKS")
blocks = {}
nb = 0
for i in range(0, x_size, x_block_size):
    if i + x_block_size < x_size:
        cols = x_block_size
    else:
        cols = x_size - i
        
    for j in range(0, y_size, y_block_size):
        if j + y_block_size < y_size:
            rows = y_block_size
        else:
            rows = y_size - j
            
        nb+=1
            
#        block = band.ReadAsArray(i, j, numCols, numRows)
        block = sum_data[j:j+rows, i:i+cols]
        
        sum = np.sum(block)
        blocks[sum] = (nb, block)
        
for k in sorted(blocks, reverse = True):
#    print(k, blocks[k])
    print("-"*10)
    print("Block number: {}".format(blocks[k][0]))
    print("Block sum : {}".format(k))
    print("Block:\n{}".format(blocks[k][1]))


    
    
    

