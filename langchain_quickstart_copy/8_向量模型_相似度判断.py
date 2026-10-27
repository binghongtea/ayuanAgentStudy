import numpy as np
from langchain_community.embeddings import DashScopeEmbeddings

def getVectorSimilarity(a:str,b:str):
    return np.linalg.norm(np.array(a) - np.array(b))
# 这里是计算欧氏距离，越近越相似；若是余弦相似度，那就是越大越相似

if __name__ == '__main__':
    texts = ['小猫可爱','有个猫好可爱','天气不错']

    embedding = DashScopeEmbeddings()
    vectors = embedding.embed_documents(texts)

    print(getVectorSimilarity(vectors[0],vectors[1]))
    print(getVectorSimilarity(vectors[0],vectors[2]))
    print(getVectorSimilarity(vectors[1],vectors[2]))