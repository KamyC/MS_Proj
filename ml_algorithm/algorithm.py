import tools.util

def detect_spam (str):
    add_to_test(str)
    return False

def get_prev_id(dest):
    with open(dest, 'rb') as f:
        return len(f.readlines())

def add_to_test(str):
    dest = 'ml_algorithm/utkmls2/history.csv'
    Id = get_prev_id(dest)+1
    list = [Id,str,0, 0, 0, 0, 0 ]
    tools.util.append_in_list(list, dest)

def get_res(dest):
    with open(dest, 'r') as f:
        opened_file = f.readlines()
        line = opened_file[-1].split(',')
        var = line[1]
        print(line)
        return var

