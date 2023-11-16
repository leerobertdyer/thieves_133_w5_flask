# In this little assignment you are given a string of space separated numbers,
# and have to return the highest and lowest number.
# Examples
# high_and_low("1 2 3 4 5")  # return "5 1"
# high_and_low("1 2 -3 4 5") # return "5 -3"
# high_and_low("1 9 3 4 -5") # return "9 -5"
# Notes
# All numbers are valid , no need to validate them.
# There will always be at least one number in the input string.
# Output string must be two numbers separated by a single space,
# and highest number is first.

#loop through the string
#try to check if the current index int(index)
#if so I'll add it to my list
#at the end I'll return max(list) and min(list)

def highAndLow(astring):
    mylist = []
    answer = ''
    flag = False
    for letter in astring:
        if letter == "-":
            flag = True
        try: 
            int(letter)
            if flag:
                mylist.append(int(letter)*-1)
                flag = False
            else:
                mylist.append(int(letter))
        except:
            pass
    return answer + str(max(mylist)) + (' ') + (str(min(mylist)))
    
    
print(highAndLow("1 2 3 4 5"))
print(highAndLow("1 2 -3 4 5"))
print(highAndLow("1 9 3 4 -5"))