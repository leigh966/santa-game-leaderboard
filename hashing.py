import os
import hashlib
def generate_timed_checksum(name, score):
    string_to_hash = name+score + os.environ.get("SECRET_KEY")
    return hashlib.sha256(string_to_hash.encode('utf-8')).hexdigest()

def generate_every_house_checksum(name, score, time):
    return generate_timed_checksum(name, score+time)

