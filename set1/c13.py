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

from collections import defaultdict
from shared import (
    random_aes_key,
    ecb_encrypt,
    ecb_decrypt,
    repeated_blocks,
    pkcs7_pad,
    chunks,
)


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

    ## We need to find offset/alignment
    ## How many character we add until we start writing fresh blocks
    first_repeat_length = None
    for i in range(64):
        pad = "." * i
        ct = blackbox(pad)
        repeat = repeated_blocks(ct)
        if repeat > 1:
            print(f"Length {i} = repeats {repeat}")
            first_repeat_length = i
            break
    bs = 16
    off = first_repeat_length - (bs * 2)
    ## After OFF bytes in our email, we start writing fresh blocks
    print(f"Found offset: {off} bytes")
    testme = ("A" * off) + ("B" * (bs * 2))
    ct = blackbox(testme)
    print(f"{testme} = {ct}")
    print(f"Repeats: {repeated_blocks(ct)}")

    ## Find a block representing "user............", aka, user at end of string
    user_role = "user".encode("ascii")
    padded_user_role = pkcs7_pad(user_role, bs)
    testme_user = ("A" * off) + (padded_user_role.decode("ascii") * 2)
    ct_user = blackbox(testme_user)
    ## The repeated block in CT_USER will be "user............"
    seen = defaultdict(int)
    for block in chunks(ct_user, bs):
        seen[block] += 1
    user_block = None
    for block, count in seen.items():
        if count > 1:
            user_block = block
    assert user_block is not None
    print(f"Found user_block: {user_block}")

    ## Find a block representing "admin...........", aka, admin at end of string
    admin_role = "admin".encode("ascii")
    padded_admin_role = pkcs7_pad(admin_role, bs)
    testme_admin = ("A" * off) + (padded_admin_role.decode("ascii") * 2)
    ct_admin = blackbox(testme_admin)
    ## The repeated block in CT_ADMIN will be "admin..........."
    seen = defaultdict(int)
    for block in chunks(ct_admin, bs):
        seen[block] += 1
    admin_block = None
    for block, count in seen.items():
        if count > 1:
            admin_block = block
    assert admin_block is not None
    print(f"Found admin_block: {admin_block}")

    print("We need to find which email will give us a user_block aligned at the end.")
    ct = None
    for email_size in range(32):
        email = ("A" * email_size) + "@example.com"
        ct = blackbox(email)
        print(email)
        print(ct)
        if user_block in ct:
            print(f"Found it! email={email}")
            break
    print(ct)
    ct_admin = ct.replace(user_block, admin_block)
    return ct_admin


def main():
    print("Challenge 13")
    xyz = attack(encrypted_profile_for)
    print("")
    print("The attacker returned encrypted bytes. When I decrypt it, I get:")
    print(decrypt_profile(xyz))


if __name__ == "__main__":
    main()
