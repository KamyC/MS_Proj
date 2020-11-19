import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from creme import compose
from creme import preprocessing
from creme import linear_model
from creme import metrics

# N X K matrix -> list of list(len = K)
def format_input(Xtrain):
  Xtrain = Xtrain.toarray().tolist()

  K = ["f" + str(f_index) for f_index in range(len(Xtrain[0]))]
  # print(Xtrain)
  # print(K)
  format_xtrain = []
  for cnt_list in Xtrain:
    format_item = dict.fromkeys(K)
    format_item.update(zip(K, cnt_list))
    format_xtrain.append(format_item)
  return format_xtrain

def train_and_return_accuracy(Xtrain, Ytrain, model):
  Xtrain_df = pd.DataFrame(Xtrain)
  Ytrain_df = pd.Series(Ytrain)
  # print(Xtrain_df)
  # print(Ytrain_df)

# precision, recall, f1
  metric = metrics.Recall()

  loop_times = 1 #change to test
  for cnt in range(loop_times):
    batch_size = 1 #int(len(Xtrain_df) / 2)  #change to test
    batch_id = 1

    while batch_id * batch_size <= len(Ytrain_df):
      for i in range(batch_size):
        y_pred = model.predict_one(Xtrain[(batch_id-1) * batch_size + i])
        metric = metric.update(Ytrain[(batch_id-1) * batch_size + i], y_pred)

      print(metric)
      model = model.fit_many(Xtrain_df[(batch_id-1) * batch_size: batch_id * batch_size],
        Ytrain_df[(batch_id-1) * batch_size: batch_id * batch_size])
      batch_id += 1

  return metric

def compute_accuracy(Xtest, Ytest, model):
  metric = metrics.Recall()
  for i in range(len(Xtest)):
    y_pred = model.predict_one(Xtest[i])      # make a prediction
    metric = metric.update(Ytest[i], y_pred)  # update the metric
  return [y_pred,metric]

''' start running code '''
# load training csv to dataframe
def init():
  df = pd.read_csv('ml_algorithm/utkmls2/train_short.csv', encoding='ISO-8859-1')

  # create binary labels
  df['b_labels'] = df['Type'].map({'Quality': 0, 'Spam': 1})
  Y = df['b_labels'].values

  # split up the data
  df_train, df_test, Ytrain, Ytest = train_test_split(df['Tweet'], Y, test_size=0.33)

  count_vectorizer = CountVectorizer(decode_error='ignore')
  Xtrain = count_vectorizer.fit_transform(df_train)
  # Xtest = count_vectorizer.transform(df_test)

  # format input/output data to fit in creme framework
  Xtrain = format_input(Xtrain)
  Ytrain = Ytrain.tolist()
  # Xtest = format_input(Xtest)
  # Ytest = Ytest.tolist()

  # use creme training model
  model = compose.Pipeline(
    preprocessing.StandardScaler(),
    linear_model.LogisticRegression()
  )

  print("train score:", train_and_return_accuracy(Xtrain, Ytrain, model))
# print("test score:", compute_accuracy(Xtest, Ytest, model))

init();