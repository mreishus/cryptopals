#!/usr/bin/env python
"""
 Write a k=v parsing routine, as if for a structured cookie. The routine should
 take:

foo=bar&baz=qux&zap=zazzle

... and produce:

{
  foo: 'bar',
  baz: 'qux',
  zap: 'zazzle'
}

(you know, the object; I don't care if you convert it to JSON).

Now write a function that encodes a user profile in that format, given an email
address. You should have something like:

profile_for("foo@bar.com")

... and it should produce:

{
  email: 'foo@bar.com',
  uid: 10,
  role: 'user'
}

... encoded as:

email=foo@bar.com&uid=10&role=user

Your "profile_for" function should not allow encoding metacharacters (& and =).
Eat them, quote them, whatever you want to do, but don't let people set their
email address to "foo@bar.com&role=admin".

Now, two more easy functions. Generate a random AES key, then:

    Encrypt the encoded user profile under the key; "provide" that to the "attacker".
    Decrypt the encoded user profile and parse it.

Using only the user input to profile_for() (as an oracle to generate "valid"
ciphertexts) and the ciphertexts themselves, make a role=admin profile.
"""

from shared import random_aes_key, ecb_encrypt, ecb_decrypt


def parse_query(str_in):
    """str (query str) -> obj (user)"""
    return_obj = {}
    parts = str_in.split("&")
    for part in parts:
        [left, right] = part.split("=")
        return_obj[left] = right
    return return_obj


def unparse_query(obj_in):
    """obj (user) -> str (query str)"""
    parts = []
    for k, v in obj_in.items():
        parts.append(str(k) + "=" + str(v))
    return "&".join(parts)


def profile_for(email_in):
    """str (email) -> str (query str)"""
    email_in = email_in.replace("&", "")
    email_in = email_in.replace("=", "")
    user = {"email": email_in, "uid": 10, "role": "user"}
    return unparse_query(user)


def mykey():
    """Static Key"""
    if not hasattr(mykey, "key"):
        mykey.key = random_aes_key()
    return mykey.key


def encrypted_profile_for(email_in):
    """str (email) -> bytes (encrypted query str)"""
    profile_str = profile_for(email_in)
    profile_bytes = profile_str.encode("ascii")
    encrypted_profile = ecb_encrypt(profile_bytes, mykey())
    return encrypted_profile


def decrypt_profile(profile_bytes):
    profile_bytes = ecb_decrypt(profile_bytes, mykey())
    return profile_bytes


def randomtest():
    str_in = "foo=bar&baz=qux&zap=zazzle"
    z = parse_query(str_in)
    y = unparse_query(z)
    print(z)
    print(y)

    print(profile_for("foo@bar.com"))
    print(profile_for("foo@bar.com&role=admin"))

    key = random_aes_key()
    profile = profile_for("admin@example.com")
    profile_bytes = profile.encode("ascii")
    encrypted_profile = ecb_encrypt(profile_bytes, key)
    print(f"key      : {key}")
    print(f"profile  : {profile}")
    print(f"encrypted: {encrypted_profile}")

    z = encrypted_profile_for("user@example.com")
    print(z)
    print(decrypt_profile(z))


def attack(blackbox):
    ## I have a blackbox that is email string -> encrypted profile bytes.
    ## My goal is to use cut and paste to manually create an encrypted
    ## role=admin profile.
    ## I'm only allowed to use blackbox() + my input, and the ciphertexts
    ## that return from that.
    b1 = blackbox("user@example.com")
    print(b1)
    b2 = blackbox("user@example.com.......")
    print(b2)
    return b1


def main():
    print("c13")
    xyz = attack(encrypted_profile_for)
    print(decrypt_profile(xyz))


if __name__ == "__main__":
    main()
