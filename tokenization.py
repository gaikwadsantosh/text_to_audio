import nltk
from nltk.tokenize import sent_tokenize

# Ensure punkt is downloaded
nltk.data.path.append(r"C:\Users\gaikw\AppData\Roaming\nltk_data")
nltk.download('punkt')

# Test tokenization
text = "This is a test sentence. Let's see if it works!"
print(sent_tokenize(text))
