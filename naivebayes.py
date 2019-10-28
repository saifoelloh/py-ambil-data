from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
import csv

#====================================================== Defining Dataset
ipk=[]
mkul=[]
name=[]
status=[]

# Assigning features and label variables
input_file = csv.DictReader(open("myBigData.csv"))
for row in input_file:
    ipk.append(int(float(row['ipk']))) #convert string to float to int
    mkul.append(row['code'])
    name.append(row['name'])
    status.append(row['status'])

# creating labelEncoder
le = preprocessing.LabelEncoder()

# Converting string labels into numbers.
ipk_encoded = le.fit_transform(ipk)
le_ipk_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
mkul_encoded = le.fit_transform(mkul)
le_mkul_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
name_encoded = le.fit_transform(name)
le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
label = le.fit_transform(status)
le_label_mapping = dict(zip(le.classes_, le.transform(le.classes_)))

print "IPK:",ipk_encoded
print "MKL",mkul_encoded
print "STS:",label
#print(le_ipk_mapping.keys())
#print(len(le_mkul_mapping.keys()), le_mkul_mapping.keys())
#print(len(le_name_mapping))
#print(le_label_mapping.keys())

# Combinig mkul and ipk into single listof tuples
features=zip(mkul_encoded, ipk_encoded)
#print features

#====================================================== Generating Model
# Create a Gaussian Classifier
model = GaussianNB()

# Train the model using the training sets
model.fit(features, label)

# Predict Output
myPredictResult = []
for x in range(0, len(le_mkul_mapping.keys())):
	for y in range(0, len(le_ipk_mapping.keys())):
		predicted=model.predict([[x,y]])
		myPredict = {}
		myPredict['ipk'] = le_ipk_mapping.keys()[y]
		myPredict['mkul'] = le_name_mapping.keys()[x]
		myPredict['status'] = predicted
		myPredictResult.append(myPredict)
		print "Predicted Value [", x, y, "] [IPK:", le_ipk_mapping.keys()[y], ", MKL:",le_mkul_mapping.keys()[x],"] :", predicted

filename = 'resultData.csv'
with open(filename, 'wb') as f: 
    w = csv.DictWriter(f,['ipk','mkul','status']) 
    w.writeheader() 
    for myPredict in myPredictResult: 
        w.writerow(myPredict) 
