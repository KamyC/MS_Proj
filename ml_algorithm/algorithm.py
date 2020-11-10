import ml_algorithm.nlp
import tools.util
def detect_spam (str):
    add_to_test(str)
    # predict another dataset
    df = ml_algorithm.nlp.pd.read_csv('ml_algorithm/utkmls2/test.csv', encoding='ISO-8859-1')
    predictions = ml_algorithm.nlp.model.predict(ml_algorithm.nlp.count_vectorizer.transform(df['Tweet']))

    submission =ml_algorithm.nlp.pd.DataFrame({'Id': df['Id'], 'Type': predictions})
    submission['Type'] = submission['Type'].map({0: 'Quality', 1: 'Spam'})

    filename = 'ml_algorithm/predictions.csv'
    submission.to_csv(filename, index=False)
    res = get_res (filename)
    if res == 'Quality\n':
        return False
    elif res == 'Spam\n':
        return True

def get_prev_id(dest):
    with open(dest, 'rb') as f:
        return len(f.readlines())

def add_to_test(str):
    dest = 'ml_algorithm/utkmls2/test.csv'
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

#
# def conf_score():
#     print("test score:", model.score(Xtest, Ytest))
