import pickle

# 1 = spam, 0 = non-spam
def is_spam(input_tweet):
    mode_path = 'ml_algorithm/model.pickel'
    model = pickle.load(open(mode_path, "rb"))
    return model.predict_one(input_tweet)

# input is raw tweet string, output is 1 or 0
def train_online(input_tweet, expected_output):
    mode_path = 'ml_algorithm/model.pickel'
    model = pickle.load(open(mode_path, "rb"))
    model.fit_one(input_tweet, expected_output)

# if __name__=="__main__":
#     model = pickle.load(open("model.pickel", "rb"))
#     print(is_spam("congratulation you won $1000"))
#     print(is_spam("I love coding"))
#
#     train_online("your IRS refund is pending", 1)
#
#     print(is_spam("congratulation you won $1000"))
#     print(is_spam("I love coding"))