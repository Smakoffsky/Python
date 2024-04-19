# Enter your code here. Read input from STDIN. Print output to STDOUT
km = [x for x in map(int, input().split(' '))]
d = dict()

test = False

#if test:
    
    #km[0] = 7  
    #km[1] = 588  
    #d[0]= sorted(set([(n * n) % km[1] for n in map(int, '7 3729019 6589533 9497010 1956867 4094190 1785314 9410145'[2:].split(' '))]))
    #d[1]= sorted(set([(n * n) % km[1] for n in map(int, '7 6241592 9563118 4665482 3629252 418388 795859 816643'[2:].split(' '))]))
    #d[2]= sorted(set([(n * n) % km[1] for n in map(int, '7 7924805 2362312 7324277 3672134 1005196 8234278 9131319'[2:].split(' '))]))
    #d[3]= sorted(set([(n * n) % km[1] for n in map(int, '7 9978282 1999589 9658103 7451768 20958 1718778 3850870'[2:].split(' '))]))
    #d[4]= sorted(set([(n * n) % km[1] for n in map(int, '7 4802255 5530524 3732809 8531273 2120056 3229818 488140'[2:].split(' '))]))
    #d[5]= sorted(set([(n * n) % km[1] for n in map(int, '7 8730597 7531483 2414636 7488541 7094601 7080117 3634144'[2:].split(' '))]))
    #d[6]= sorted(set([(n * n) % km[1] for n in map(int, '7 7512988 392327 4450786 7954145 2754638 4291414 1626278'[2:].split(' '))]))

    #km[0] = 7  
    #km[1] = 867  
    #d[0]= sorted(set([(n * n) % km[1] for n in map(int, '7 6429964 4173738 9941618 2744666 5392018 5813128 9452095'[2:].split(' '))]))
    #d[1]= sorted(set([(n * n) % km[1] for n in map(int, '7 6517823 4135421 6418713 9924958 9370532 7940650 2027017'[2:].split(' '))]))
    #d[2]= sorted(set([(n * n) % km[1] for n in map(int, '7 1506500 3460933 1550284 3679489 4538773 5216621 5645660'[2:].split(' '))]))
    #d[3]= sorted(set([(n * n) % km[1] for n in map(int, '7 7443563 5181142 8804416 8726696 5358847 7155276 4433125'[2:].split(' '))]))
    #d[4]= sorted(set([(n * n) % km[1] for n in map(int, '7 2230555 3920370 7851992 1176871 610460 309961 3921536'[2:].split(' '))]))
    #d[5]= sorted(set([(n * n) % km[1] for n in map(int, '7 8518829 8639441 3373630 5036651 5291213 2308694 7477960'[2:].split(' '))]))
    #d[6]= sorted(set([(n * n) % km[1] for n in map(int, '7 7178097 249343 9504976 8684596 6226627 1055259 4880436'[2:].split(' '))]))

    #km[0] = 3
    #km[1] = 66
    #d[0]= sorted(set([(n * n) % km[1] for n in map(int, '6 847984069 128759845 89587078 83683271 622627080 375789769'[2:].split(' '))]))
    #d[1]= sorted(set([(n * n) % km[1] for n in map(int, '1 443420129'[2:].split(' '))]))
    #d[2]= sorted(set([(n * n) % km[1] for n in map(int, '2 242479052 251194086'[2:].split(' '))]))

    #km[0] = 3
    #km[1] = 66
    #d[0]= sorted(set([(n * n) % km[1] for n in map(int, '1 847984069'[2:].split(' '))]))
    #d[1]= sorted(set([(n * n) % km[1] for n in map(int, '7 1506500 3460933 1550284 3679489 4538773 5216621 5645660'[2:].split(' '))]))
    #d[2]= sorted(set([(n * n) % km[1] for n in map(int, '1 242479052'[2:].split(' '))]))

    #km[0] = 5
    #km[1] = 84
    #d[0]= sorted(set([(n * n) % km[1] for n in map(int, '1 765952241'[2:].split(' '))]))
    #d[1]= sorted(set([(n * n) % km[1] for n in map(int, '3 289380515 265118103 309882974'[2:].split(' '))]))
    #d[2]= sorted(set([(n * n) % km[1] for n in map(int, '2 747649220 587740446'[2:].split(' '))]))
    #d[3]= sorted(set([(n * n) % km[1] for n in map(int, '2 682866882 596381508'[2:].split(' '))]))
    #d[4]= sorted(set([(n * n) % km[1] for n in map(int, '1 342723101'[2:].split(' '))]))


#  index of value of each dictionary in our summ
usage = dict()
max_value = 0
# print(d)
result = []
retest = []

def init():
    summ = 0
    j = 0
    while summ < km[1]:
        for i in range(km[0]):
            if j < len(d[i]) - 1:
                summ = d[i][j] + summ
                usage[i] = j
                
                if j > 0:
                    summ = summ - d[i][j - 1]
        
        j = j + 1

def get_summ():
    summ = 0
    for i in range(km[0]):
        if (len(d[i]) > usage[i]):
            summ = summ + d[i][usage[i]]
        else:
            summ = summ + d[i][len(d[i]) - 1]
            usage[i] = len(d[i]) - 1
        
    return summ % km[1]

   
def get_next(max_value, row):
    diff = km[1] - max_value
    ind = 0
    n_val = max_value
    prev = d[row][usage[row]]
    for i in range(len(d[row])):
        if i != usage[row]:
            n_val = (n_val - prev + d[row][i]) % km[1]
            if abs(n_val - km[1]) < diff:
                diff = abs(n_val - km[1])
                ind = i
    return ind

def check_max(val):
    if val == km[0] - 1:
        return True
    else:
        return False
        
     
def iterate():
    max_value = get_summ()
    i = 0
    while i < km[0]:
        ind = get_next(max_value, i)
        usage[i] = ind
        max_value = get_summ()
           
        j= 0
        if max_value not in result:
            result.append(max_value)
            retest.append(usage)
        
        if (check_max(max_value)):
            break

        while j < km[0]:
            
            if (j != i):
                ind = get_next(max_value, j)
                usage[j] = ind
                max_value = get_summ()

                
                if max_value not in result:
                    result.append(max_value)
                    retest.append(usage)
                    
                if (check_max(max_value)):
                    break

            j = j + 1
        i = i + 1
    return max_value

     
for i in range(km[0]):
    if (not test):
        d[i] = sorted(set([(n*n) % km[1] for n in map(int, input()[2:].split(' '))]))
    max_value = max_value + d[i][len(d[i]) - 1]
    
if (max_value < km[1]):
    # this is out results
    print(max_value)
else:
       
    val = 0
    for i in range(km[0]):
        usage[i] = 0

    max_value = iterate()
    
    if not check_max(max_value):
        found = True
        i = 1
        while found:
            i = i + 1
            for m in (range(km[0])):
                found = False
                if (len(d[m]) > i):
                    found = True
                    usage[m] = i
                else:
                    usage[m] = len(d[m]) - 1

            max_value = iterate()
        
            if check_max(max_value):
                break
    
        if not check_max(max_value):
            for usage in retest:
                max_value = iterate()
                if check_max(max_value):
                    break
    
    print(sorted(result, reverse=True)[0])
