import hashlib
import base64


def dot_to_document(v):

    word = v + " " 
    wordL = list(word)
    wordL[word.find('document')+8] = '.'
    dotedWord = "".join(wordL).strip()

    return dotedWord 
    
def preAuth_gen_hash(attributes, sk):

    ordredAttValues = [dot_to_document(attributes.get(v)) if "document" in attributes.get(v) else attributes.get(v,'')  for v in sorted(attributes, key=str.casefold) ]
    toHash = "|".join((ordredAttValues))
    toHash += f"|{sk}"
    
    h = hashlib.sha512()
    h.update(toHash.encode().strip())
    attributes['hash'] = base64.b64encode(h.digest()).decode('utf-8')
    attributes['encoding'] = 'UTF-8'

    return attributes 

def postAuth_gen_hash(attributes, sk):

    ordredAttValues = [attributes.get(v,'')  for v in sorted(attributes, key=str.casefold)]
    toHash = "|".join((ordredAttValues)) 
    toHash += f"|{sk}"

    h = hashlib.sha512()
    h.update(toHash.encode().strip())

    return h.digest()


