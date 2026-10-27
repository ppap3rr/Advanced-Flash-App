
def generate_features(a, b, operation, correct_answer): 
    features = {}
    # Basic Features
    features["a"] = a
    features["a_digits"] = len(str(abs(a)))
    features["a_ends_5"] = int(a % 10 == 5)
    features["a_ends_0"] =  int(a % 10 == 0)
    features["a_digit_sum"] = digit_sum(a)
    features["a_decimal_places"] = decimal_places(a)
    features["operation"] = operation
    if b is not None: 
        features["b"] = b
        features["b_digits"] = len(str(abs(b)))
        features["b_ends_0"] = int(b % 10 == 0)
        features["b_ends_5"] =  int(b % 10 == 5)
        features["b_digit_sum"] = digit_sum(b)
        features["b_decimal_places"] = decimal_places(b)
    features["answer_digits"] =  len(str(abs(correct_answer)))
    features["answer_digit_sum"] = digit_sum(correct_answer)

    # Additional Features 
    if operation == "Multiplication": 
        pass
    elif operation == "Division": 
        features.update(generate_div_features(a, b, correct_answer))
    elif operation ==  "Squares": 
        pass
    elif operation == "Square Roots": 
        features.update(generate_sqr_root_features(a, b, correct_answer))
    elif operation == "Difference of Squares": 
        features.update(generate_diff_features(a, b))
    elif operation == "Cube Roots": 
        features.update(generate_cube_root_features(a, b, correct_answer))
    return features

def digit_sum(x): 
    x = str(x)
    sum = 0 
    for i in x: 
        if i != '.': 
            sum += int(i)
    return sum

def decimal_places(x): 
    x = str(x)
    count = 0 
    start = False
    for i in x: 
        if start: 
            count += 1 
        if i == ".": 
            start = True
    return count 

def generate_diff_features(a, b): 
    features = {
        "len_difference" : len(str(abs(a-b))),
        "len_sum" : len(str(abs(a+b))), 
        "neg_diff" : int(b > a)
    }
    return features

def generate_cube_root_features(a, b, answer) : 
    features = {
        "perfect_cube" : int(answer % 1 == 0)
    }
    return features

def generate_sqr_root_features(a, b, answer): 
    features = {
        "perfect_square" : int(answer % 1 == 0),
    }

    return features

def generate_div_features(a, b, answer): 
    features = {
        "divides_evenly": int(a%b==0)
    }
    return features
