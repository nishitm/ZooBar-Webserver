#!/usr/bin/python

import symex.fuzzy as fuzzy


# def f(x):
#     if x==100:
#         return 100
#     if x==70:
#         return 70;
#     if x==80:
#         return 80
#     if x==30:
#         return 33
#     else:
#         return 45

# def f(x):
#     y=0
#     if x == 1:
#         y=1
#     if x == 2:
#         y=2
#     if x == 3:
#         y= 3
#     if x == 4:
#         y= 4
#     if x == 5:
#         y= 5
#     return y

def f(x):
    if x == 7:
        return 100
    if x*2 == x+1:
        return 70
    if x > 2000:
        return 80
    if x < 500:
        return 33
    if x / 123 == 7:
        return 1234
    return 40

f_results = set()
def test_f():
    i = fuzzy.mk_int('i')
    v = f(i)
    print i, '->', v
    f_results.add(v)

print 'Testing f..'
fuzzy.concolic_test(test_f, verbose=10)
#f_expected = (1, 2, 3, 4, 5)
f_expected = (100, 70, 80, 33, 1234, 40)
if all(x in f_results for x in f_expected):
    print "Found all cases for f"
else:
    print "Missing some cases for f:", set(f_expected) - set(f_results)
