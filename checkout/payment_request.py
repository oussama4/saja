import hashlib
import base64


def generateHash(attributes, sk):

    ordredAttValues = [attributes.get(v,'') for v in sorted(attributes, key=str.casefold)]
    toHash = "|".join((ordredAttValues))
    toHash += f"|{sk}"
    
    h = hashlib.sha512()
    h.update(toHash.encode().strip())
    attributes['hash'] = base64.b64encode(h.digest()).decode('utf-8')
    attributes['encoding'] = 'UTF-8'

    return attributes 


