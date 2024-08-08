from managemodel.preprcessing import ChatbotPreprocessing
from sklearn.svm import SVC
from sklearn.model_selection import RandomizedSearchCV
import pickle as pkl
class TrainingModel:
    def __init__(self, name_dataset, model_name):
        self.model_name = model_name
        self.name_dataset = name_dataset
        self.preprocessing = ChatbotPreprocessing()
    def create_model(self,X, y):
        model = SVC()
        randomizedSearch = RandomizedSearchCV(model, {
            'C': [0.1, 1, 10, 100, 1000],
            'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
            'kernel': ['rbf', 'poly', 'sigmoid']
        }, n_iter=10, cv=5, n_jobs=-1, verbose=1)
        randomizedSearch.fit(X, y)
        best_model = randomizedSearch.best_estimator_
        return best_model
        
    def train(self):
        try:
            feature_questions,target_intents = self.preprocessing.preprocess(self.name_dataset,self.model_name)
            model = self.create_model(feature_questions,target_intents)
            pkl.dump(model,open(f"ds\models\{self.model_name}.pkl","wb"))
            return True
        except:
            return False
    
        

        
        