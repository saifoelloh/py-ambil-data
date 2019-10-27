from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
import csv

#====================================================== Defining Dataset
ipk=[]
name=[]
status=[]

# Assigning features and label variables
input_file = csv.DictReader(open("myBigData.csv"))
for row in input_file:
    ipk.append(int(float(row['ipk']))) #convert string to float to int
    name.append(row['name'])
    status.append(row['status'])

# creating labelEncoder
le = preprocessing.LabelEncoder()

# Converting string labels into numbers.
ipk_encoded = le.fit_transform(ipk)
le_ipk_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
#print(le_ipk_mapping.keys())

name_encoded = le.fit_transform(name)
le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
#print(le_name_mapping.keys())

label = le.fit_transform(status)
le_label_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
#print(le_label_mapping.keys())

print "IPK:",ipk_encoded
print "MKL",name_encoded
print "STS:",label

# Combinig weather and temp into single listof tuples
features=zip(name_encoded, ipk_encoded)
#print features

#====================================================== Generating Model
# Create a Gaussian Classifier
model = GaussianNB()

# Train the model using the training sets
model.fit(features, label)

# Predict Output
#for x, namex in enumerate(name_encoded):
for x in range(0, 30):
	for y in range(0, 4):
		predicted=model.predict([[x,y]])
		print "Predicted Value [IPK:", le_ipk_mapping.keys()[y], " MKL:",le_name_mapping.keys()[x],"] :", predicted
