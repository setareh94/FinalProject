a_list = [1,1,2,3,5]
a_list.remove(1)
print a_list

def convert_to_binary(n):
    s = ''
    while(n):
        s = str(n % 2) + s;
        n = n / 2
    print s

convert_to_binary(2)
    