import chromadb
from chromadb.utils import embedding_functions

#default_ef = embedding_functions.DefaultEmbeddingFunction()

chroma_client = chromadb.Client()


#sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
collection = chroma_client.create_collection(name="my_collection")




collection.add(
    documents=[
        '''Abstract
Background: Older patients with dementia are often unable to take their medications as prescribed due to cognitive and
focus on the development and implementation of interventions
to help older patients with dementia and their caregivers make better use of medications.''',

        '''p-Type NdzFe4xCoxSb12 (z = 0.8, 0.9, 1.0 and x = 0, 0.5, 1.0) skutterudites
were synthesized by encapsulated melting and annealing, and consolidated
with hot pressing. The eff'''
    ],
    metadatas=[
        {"description": "Medication Adherence in Older Patients With Dementia: A Systematic Literature Review"},
        {"description": "Electronic Transport and Thermoelectric Properties of p-Type NdzFe4xCoxSb12 Skutterudites"}
    ],
    ids=[
        "doc1", "doc2"
    ]
)



results = collection.query(
    query_texts=["transportation"],
    n_results=2
)

print(results)