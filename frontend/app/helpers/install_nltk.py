import nltk

if __name__ == "__main__":
	for package in ['stopwords','punkt', 'wordnet']:
		nltk.download(package)
        
print("nltk packages downloaded successfully.")