from sentence_transformers import SentenceTransformer
import pickle as pkl
import langid
import numpy as np
class Prediction:
    _instance = None
    def __new__(cls,model,dict_path,encoder_path):
        if cls._instance is None:
            cls._instance = super(Prediction, cls).__new__(cls)
            cls._instance.__init__(model,dict_path,encoder_path)
        return cls._instance
    
    def __init__(self,model,dict_path,encoder_path) -> None:
        self.transformer_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        self.dict_intent_entity = pkl.load(open(dict_path,"rb"))
        self.label_encoder = pkl.load(open(encoder_path,"rb"))
        self.model = model
        
        
    def identify_entity(self,question,list_entities):
        
        _list_entities = list_entities
        _question = question
        _question = _question.lower()
        _count_entities = []
        _store_entities = []
        _len_entities = []
        _store_index = []
        for idx,entities in enumerate(_list_entities):
            _count_entities.append(0)
            _store_entities.append(entities)
            _len_entities.append(len(entities))
            _store_index.append(idx)
            for entity in entities:
                if entity in _question:
                    _count_entities[idx] = _count_entities[idx] + 1
        _count_entities = np.array(_count_entities)
        max_value = np.max(_count_entities)
        
        if max_value == 0:
            return None
        idx_max = _count_entities == max_value
        _store_entities = np.array(_store_entities,dtype=object)
        _max_entities = _store_entities[idx_max]
        _store_max_len = np.array(_len_entities)
        _store_max_len = _store_max_len[idx_max]
        min_id = np.argmin(_store_max_len)
        
        return _max_entities[min_id]

    def identify_language(self,question):
        return langid.classify(question)[0]
    def get_answer(self,question):
        _intent = self.model.predict(self.transformer_model.encode([question]))
        _intent = self.label_encoder.inverse_transform([_intent])[0]
        _dict_entities = self.dict_intent_entity[_intent]
        _list_entities = list(_dict_entities.keys())
        if _intent in ["greeting","polite"]:
            try:
                lang = self.identify_language(question)
                _answer = _dict_entities[tuple(_list_entities[0])][lang]
                if type(_answer) == list:
                    idx = np.random.randint(0,len(_answer))
                    return _answer[idx],True
                return _answer,True
            except:
                _answer = "I'm sorry, I don't have ability to answer this question yet."
                if lang == "km":
                    _answer = "ខ្ញុំសុំទោស ខ្ញុំមិនទាន់មានលទ្ធភាពឆ្លើយសំណួរនេះនៅឡើយទេ។"
                return _answer,False
        _identity = self.identify_entity(question,_list_entities)
        lang = None
        try:
            lang = self.identify_language(question)
            _identity = tuple(_identity)
            _answer = _dict_entities[_identity][lang]
            if type(_answer) == list:
                idx = np.random.randint(0,len(_answer))
                return _answer[idx],True
            return _answer,True
        except:
            _answer = "I'm sorry, I don't have ability to answer this question yet."
            if lang == "km":
                _answer = "ខ្ញុំសុំទោស ខ្ញុំមិនទាន់មានលទ្ធភាពឆ្លើយសំណួរនេះនៅឡើយទេ។"
            return _answer,False
        