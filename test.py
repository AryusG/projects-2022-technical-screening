from curses.ascii import isdigit
import re

courses_taken = ['COMP6666']
credits_pattern = re.compile(r"^\d?\d units of credit in level \d COMP courses")


test_1 = "COMP6666 and (COMP6666 or 12 units of credit in level 6 MATH courses)"
test_1 = re.sub(rf"{courses_taken[0]}", "True", test_1) 
test_1 = re.sub(rf"COMP\d\d\d\d", "False", test_1)
# print(test_1)
# print(eval(test_1))
# test_2 = "COMP6666 and ((COMP1511 or COMP3333) and COMP9020)"

test_3 = "12 units of credit in level 6 COMP courses"
nums = re.finditer(r"\d?\d", test_3) 
for n in nums:
   span = n.span()
   print(test_3[span[0]:span[1]])

