def func(a, b):
    a += 1
    b.append(1)

a, b = 0, []
func(a, b)
print("After function call, value of a doesn't change (since no return), value of b change, since it's list pass by ref", a, b)

def has_pos_neg(nums):
    has_pos, has_neg = False, False
    for num in nums:
        has_pos = num > 0
        has_neg = num < 0
    
    return(has_pos, has_neg)

nums = [0, -1, -2]
print(has_pos_neg(nums))