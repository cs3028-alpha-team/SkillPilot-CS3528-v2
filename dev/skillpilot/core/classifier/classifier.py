from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

"""
class definition for the KNN classifier used during the matchmaking process
"""
class Classifier:

    def __init__(self, dataframe, target_column, centroid_limit=50):
        self.df = dataframe
        self.target_column = target_column
        self.scaler = StandardScaler()
        self.centroid_limit = centroid_limit # limit of centroids to be used during elbow method

    def train(self):

        # fit the scaler object to the dataframe
        self.scaler.fit(self.df.drop(self.target_column, axis=1))

        # transform the dataframe using the trained scaler 
        self.scaled_features = self.scaler.transform(self.df.drop(self.target_column, axis=1))

        # create a new dataframe using the scaled features from the original one, minus the target column
        self.scaled_df = pd.DataFrame(data=self.scaled_features, columns=self.df.columns[:-1])

        # split the datasets into 70% training data and 30% testing data
        self.X, self.y = self.scaled_df, self.df[self.target_column]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=42)

        # perform a search using the Elbow method to find the number of centroids which yields the minimum error rate during classification
        error_rate = []

        for i in range(1, self.centroid_limit):
            knn = KNeighborsClassifier(n_neighbors=i)
            knn.fit(self.X_train, self.y_train)
            predictions_i = knn.predict(self.X_test)
            # average error rate, where predicitons where not equal to actual test values 
            error_rate.append(np.mean(predictions_i != self.y_test))

        # instantiate the KNNClassifier with k = min_error_k, i.e. the number of centroids which yields the least error
        min_error_k = error_rate.index(min(error_rate))
        self.knn = KNeighborsClassifier(min_error_k)
        self.knn.fit(self.X_train, self.y_train)


    def assess(self):

        # display the confusion matrix and classfication report for this model
        self.predictions = self.knn.predict(self.X_test)
        print(confusion_matrix(self.y_test, self.predictions))
        print('\n')
        print(classification_report(self.y_test, self.predictions))
        
    # given an input dataframe, without the target column, return a list of predictions 
    def predict(self, offers):
        return [ self.knn.predict(offers.iloc[i].to_frame().T)[0] for i in offers.index ]