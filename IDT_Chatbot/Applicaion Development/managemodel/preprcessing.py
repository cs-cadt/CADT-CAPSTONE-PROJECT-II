
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import LabelEncoder
import pickle as pkl
class ChatbotPreprocessing:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.transformer_ml = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
    
    def clean_dataset(self, dataset):
        columns = dataset.columns
        columns = [col.lower() for col in columns]
        dataset.columns = columns
        # get list of intents
        intents = dataset[["intent"]]
        intents = intents.dropna()
        list_intents = intents["intent"].values.tolist()
        length = len(dataset)
        k = -1
        # fill intent into missing values
        for i in range(length):
            if pd.isnull(dataset.loc[i,"intent"]):
                dataset.loc[i,"intent"] = list_intents[k]
            else:
                k+=1
                
        # get list of entities
        entities = dataset[["entity"]]
        entities = entities.dropna()
        list_entities = entities["entity"].values.tolist()
        entity_index = -1
        # fill entity into missing values
        for i in range(length):
            if pd.isnull(dataset.loc[i,"entity"]):
                dataset.loc[i,"entity"] = list_entities[entity_index]
            else:
                entity_index += 1
        return dataset
    
    def create_setting(self, dataset):
        dataset_intent_entity = dataset[["intent","entity"]]
        intent_entity = dataset_intent_entity.groupby(["intent","entity"]).size()
        intent_entity_df = intent_entity.reset_index()
        dict_intent_entity = {}
        length_ie = len(intent_entity_df)
        for i in range(length_ie):
            intent = intent_entity_df.loc[i,"intent"].lower()
            entity = intent_entity_df.loc[i,"entity"]
            flist_entity=entity.lower().split(",")
            flist_entity = [x.strip() for x in flist_entity]
            list_answer_en = dataset[dataset["entity"]==entity][["eng answer"]].dropna()["eng answer"].values.tolist()
            list_answer_km = dataset[dataset["entity"]==entity][["kh answer"]].dropna()["kh answer"].values.tolist()
            if intent not in dict_intent_entity:
                dict_intent_entity[intent] = {}
            dict_intent_entity[intent][tuple(flist_entity)] = {"en":list_answer_en,"km":list_answer_km}
        return dict_intent_entity
    
    def create_dataset(self,dataset):
        train_data = dataset[["intent","question"]].dropna()
        feature_questions = pd.DataFrame(train_data[["question"]].apply(lambda x: self.transformer_ml.encode(x[0]),axis=1).values.tolist())
        target_intents = train_data[["intent"]]
        target_intents = target_intents.applymap(lambda x: x.lower())
        label_encoder = LabelEncoder()
        target_intents = label_encoder.fit_transform(target_intents)
        return feature_questions,target_intents,label_encoder
    
    def preprocess(self, name_dataset, name_model):
        print("Preprocessing is done")
        dataset = pd.read_csv(f"data_storage\{name_dataset}")
        # change columns to lowercase
        cleaned_dataset = self.clean_dataset(dataset)
        dict_intent_entity = self.create_setting(cleaned_dataset)
        feature_questions,target_intents,label_encoder = self.create_dataset(cleaned_dataset)
        pkl.dump((dict_intent_entity,label_encoder),open(f"ds\setting\{name_model}.pkl","wb"))
        return feature_questions,target_intents
        
