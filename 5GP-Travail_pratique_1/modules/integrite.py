# code inspiré de https://stackoverflow.com/questions/22058048/hashing-a-file-in-python

import hashlib

BUF_SIZE = 65536


def hash_fichier(chemin_fichier) -> str:
    
    sha256 = hashlib.sha256()

    with open(chemin_fichier, 'rb') as f:
        while True:
            donnee = f.read(BUF_SIZE)
            if not donnee:
                break
            
            sha256.update(donnee)

    return sha256.hexdigest()