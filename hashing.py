import os
import hashlib
def generate_checksum(name, deaths,jumps, time):
    string_to_hash = name+deaths+jumps + time + os.environ.get("SECRET_KEY")
    return hashlib.sha256(string_to_hash.encode('utf-8')).hexdigest()

