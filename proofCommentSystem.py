from __future__ import annotations

import hashlib, base64, random, string

class ProofCommentSystem:

    def __init__(self) -> None:
        self.hash_function = hashlib.sha3_224
        self.passphrase_len : int = 10
        self.current_proof : str = str()
        self.current_passphrase : str = self.generate_random_passphrase(self.passphrase_len)

    def generate_random_passphrase(self, length : int) -> str:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def hash(self, passphrase : str) -> hashlib._Hash:
        return self.hash_function(f"{passphrase}".encode())

    def serialize_data(self, proof : str, passphrase : str) -> str:
        data = f"{ proof } * {passphrase}"
        return base64.b64encode(data.encode()).decode()

    def deserealize_data(self, payload : str):
        decoded_payload = base64.b64decode(payload.encode())
        data = decoded_payload.decode().split(" * ")
        if len(data) == 2:
            return data 
        else:
            print("Wrong data")

    def is_the_same_guy(self, current_payload, prev_payload):
        print("[*] Checking comment authority...")
        try:
            proof_to_solve = self.deserealize_data(current_payload)[0]
            to_use_key = self.deserealize_data(prev_payload)[1]
            same = self.hash(to_use_key).hexdigest() == proof_to_solve
            if same:
                print("Is the same guy!!")
            else:
                print("Isn't the same guy")
        except:
            print("Error to check comment authority")


    def add_comment(self, comment : str) -> str:
        passphrase : str = str()

        # If a proof was hashed previously
        if self.current_proof:
            # integrity = self.hash() == self.current_proof
            passphrase = self.current_passphrase 
            # Regenerate passphrase
            self.current_passphrase = self.generate_random_passphrase(self.passphrase_len)

        # Hash the current passpharse
        proof = self.hash(self.current_passphrase).hexdigest()

        # Show the current proof and the passphrase for solve the previous proof
        payload = self.serialize_data(proof, passphrase)
        full_comment = f"{comment} #{payload}"

        # Save the current proof
        self.current_proof = proof

        print("-"*100)
        print(full_comment)
        print(f"{proof} ({comment}) <- {passphrase} ") 
        print("\n")
        return payload


comment_system = ProofCommentSystem()

# payload = hash + key for solve the previous 'proof'
payload_0 = comment_system.add_comment("Hi, i'm hwpoison!")

payload_1 = comment_system.add_comment("How its going, guys?")

payload_2 = comment_system.add_comment("I'm hwpoison! I have proofs!")

# Try to solve the 'proof' of the previous comment with the key of the next comment
# for check if is the same guy
comment_system.is_the_same_guy(payload_0, payload_1)
