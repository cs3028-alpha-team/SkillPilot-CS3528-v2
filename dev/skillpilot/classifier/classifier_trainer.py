from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import random as rand
import pickle

from classifier_class import Classifier

if __name__ == "__main__":
    
    # construct the training dataframe
    df_cols = [ 'studentGPA', 'internshipGPA', 'compatibilityScore', 'GPADifference', 
    'fieldExperienceRelevance',  'contractModeCompatibility', 'contractPatternCompatibility', 'acceptedOffer' ]

    df_data = []
    for i in range(1000):
        studentGPA = rand.randint(60, 100)
        internshipGPA = rand.randint(60, 100)
        compatibilityScore = round(rand.uniform(1.25, 4), 2)
        GPADifference = abs(studentGPA-internshipGPA)/100 # scale down, can be 1.00 to 0.00
        fieldExperienceRelevance = rand.random()
        contractModeCompatibility = rand.random()
        contractPatternCompatibility = rand.random()
        acceptedOffer = True if ((compatibilityScore + fieldExperienceRelevance + contractModeCompatibility + contractPatternCompatibility) > 4 and GPADifference < 0.5) else False
        df_data.append([studentGPA, internshipGPA, compatibilityScore, GPADifference, fieldExperienceRelevance, contractModeCompatibility, contractPatternCompatibility, acceptedOffer])

    df = pd.DataFrame(data=df_data, columns=df_cols)

    print("Dataframe created\n")
    print(df.head())

    # instantiate the classifer and train it
    classifier = Classifier(df, 'acceptedOffer')    
    classifier.train()

    print("Classifier instantiated and trained\n")
    classifier.assess()

    # serialise the trained classifier and save it to a file
    file_path = 'classifier.pkl'
    with open(file_path, 'wb') as f:
        pickle.dump((classifier), f)

    print(f"Classifier serialized and saved to {file_path}")