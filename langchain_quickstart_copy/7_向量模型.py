from langchain_community.embeddings import DashScopeEmbeddings

embedding = DashScopeEmbeddings()

# text = '你好，我是楷哥'
#
# vector = embedding.embed_query(text)
#
# print(vector)
# print(len(vector))

text_list = ['你好','我是','楷哥']

vectors = embedding.embed_documents(text_list)

print(vectors)
print(len(vectors))
print(vectors[0])
