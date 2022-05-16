"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.

NOTE: We do not expect you to come up with a perfect solution. We are more interested
in how you would approach a problem like this.
"""
import json
import re 

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()

def substitution_clean(courses_list, prereq):
    prereq = re.sub(r"Prerequisite: ", "", prereq)
    prereq = re.sub(r"\s+", " ", prereq) # no extra spaces 
    prereq = re.sub(r"oc", "or", prereq)
    prereq = re.sub(r"OR", "or", prereq)
    prereq = re.sub(r"AND", "and", prereq)
    for course in courses_list:
        prereq = re.sub(rf"{course}", "True", prereq)
    prereq = re.sub(r"[A-Z]{4}\d\d\d\d", "False", prereq)

    return prereq

def completion_uoc_clean(credits_dict, prereq):
    completion_uoc_pattern = re.compile(r"(C|c)ompletion of \d?\d units of credit")
    match = re.search(completion_uoc_pattern, prereq)
    match_str = match.group()
    num = re.search(r"\d?\d", match_str)
    indexes = num.span()

    if credits_dict["total"] >= int(match_str[indexes[0]:indexes[1]]):
        prereq = re.sub(rf"{match_str}", "True", prereq)
    else:
        prereq = re.sub(rf"{match_str}", "False", prereq)

    return prereq

def uoc_levels_clean(credits_dict, prereq):
    credits_pattern = re.compile(r"\d?\d units of credit in level \d COMP courses")
    crd_ptrn_matches = re.finditer(credits_pattern, prereq)
    for match in crd_ptrn_matches:
        match_str = match.group()
        nums = re.finditer(r"\d?\d", match_str) # Get a hold of num of units and what level course
        units_of_credit = 0
        level = 0
        counter = 0 
        for n in nums: # First iteration is for units_of_credit & secound iteration is for level
            indexes = n.span()
            if counter == 0:
                units_of_credit = int(match_str[indexes[0]:indexes[1]])
            else:
                level = int(match_str[indexes[0]:indexes[1]])
            counter += 1
        
        # CHECK IF STUDENT Have Enough Credits
        if credits_dict[f"COMP{level}"] >= units_of_credit:
            prereq = re.sub(rf"{match_str}", "True", prereq)
        else:
            prereq = re.sub(rf"{match_str}", "False", prereq)
    
    return prereq

def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """

    # PROCESS AMOUNT OF CREDITS
    credits_dict = {
        "total": 0,
        "COMP1": 0,
        "COMP2": 0, 
        "COMP3": 0,
    }

    for c in courses_list:
        if c[0] == "C":
            if c[4] == "1":
                credits_dict["COMP1"] += 6
            if c[4] == "2":
                credits_dict["COMP2"] += 6
            if c[4] == "3":
                credits_dict["COMP3"] += 6
        credits_dict["total"] += 6

    prereq = CONDITIONS[target_course]

    if prereq == "":
        return True
    
    if not courses_list:
        return False 

    # DATA CLEANING with Substitutions 
    prereq = substitution_clean(courses_list, prereq)
    print(prereq)

    # Substitute "completion of \d\d units of credit" with True or False
    if re.search(r"(C|c)ompletion of \d?\d units of credit", prereq):
        prereq = completion_uoc_clean(credits_dict, prereq)

    # Substitute units of credit with True or False
    if re.search(r"\d?\d units of credit in level \d COMP courses", prereq):
        prereq = uoc_levels_clean(credits_dict, prereq)
    
    print(prereq)
    
    return eval(prereq)

    
courses_list = ["COMP1234", "COMP5634", "COMP4834"]
target_course = 'COMP9491'
print(is_unlocked(courses_list=courses_list, target_course=target_course))



    