# -*- coding: utf-8 -*-
"""simple_transformers.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R1zh3y7f04Uj-ncWs_KSkCtOS7wJUuGn
"""

!pip install simpletransformers

from simpletransformers.classification import ClassificationModel, ClassificationArgs
from simpletransformers.classification import MultiLabelClassificationModel, MultiLabelClassificationArg
from sklearn.model_selection import train_test_split
import pandas as pd

from google.colab import drive
import os
import json
drive.mount('/content/gdrive')

fake = pd.read_csv('fake.csv')
true = pd.read_csv('true.csv')
fake['label'] = 'Fake'
true['label'] = 'True'
data = fake[['text', 'label']].append(true[['text', 'label']])
text, label = data['text'].array, data['label'].array
X_train, X_test, y_train, y_test = train_test_split(text, label, test_size=0.33, random_state=42)
train = pd.DataFrame({'text':X_train, 'labels':y_train})
test = pd.DataFrame({'text':X_test, 'labels':y_test})

model_args = ClassificationArgs()
model_args.labels_list = ['Fake', 'True']

model = ClassificationModel('bert', 'bert-base-uncased', args = model_args)
model.train_model(train)

model.eval_model(test)

from sklearn.model_selection import train_test_split
import numpy as np
import json
import pandas as pd

l = []
with open('/content/gdrive/MyDrive/News_Category_Dataset_v2.json', 'r') as f:
  for line in f.readlines():
    dic = json.loads(line)
    l.append(dic)

y = [dic['category'].split(' & ') for dic in l]
X = [dic['short_description'] for dic in l]

cat = []
for i in y:
  for k in i:
    if k not in cat:
      cat.append(k)

vec_list = []
for i in y:
  vec = [0 for i in range(len(cat))]
  for index in range(len(cat)):
    if cat[index] in i:
      vec[index] = 1
  vec_list.append(vec)

X_train, X_test, y_train, y_test = train_test_split(X, vec_list, test_size=0.33, random_state=42)
train = pd.DataFrame({'text':X_train, 'labels':y_train})
test = pd.DataFrame({'text':X_test, 'labels':y_test})

from simpletransformers.classification import MultiLabelClassificationModel, MultiLabelClassificationArgs
import logging 

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

# Optional model configuration
model_args = MultiLabelClassificationArgs(num_train_epochs=1)

# Create a MultiLabelClassificationModel
model = MultiLabelClassificationModel(
    "bert", "bert-base-uncased", num_labels=len(cat),
)

# Train the model
model.train_model(train)

# Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(
    test
)

result