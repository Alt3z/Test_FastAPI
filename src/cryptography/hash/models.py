from enum import Enum
import hashlib


class HashMethod(str, Enum):
    sha256 = "sha256"
    sha1 = "sha1"
    md5 = "md5"


hash_functions = {
    "sha256": hashlib.sha256,
    "sha1": hashlib.sha1,
    "md5": hashlib.md5
}