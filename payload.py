# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from cryptography.fernet import Fernet
# import base64

# app = FastAPI()

# encryption_key = b'mcMAmuM2wLgNey7hgaCXDsaH__h13R2esSQ7fKvX3ak='



# def encrypt_data(data: str) -> str:
#     cipher = Fernet(encryption_key)
#     encrypted = cipher.encrypt(data.encode())
#     return base64.b64encode(encrypted).decode()


# def decrypt_data(data: str) -> str:
#     try:
       
#         missing_padding = len(data) % 4
#         if missing_padding:
#             data += '=' * (4 - missing_padding)

#         encrypted_token = base64.b64decode(data)
#         cipher = Fernet(encryption_key)
#         decrypted = cipher.decrypt(encrypted_token)

#         return decrypted.decode()

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Decryption failed: {str(e)}")


# class EncryptRequest(BaseModel):
#     text: str


# class DecryptRequest(BaseModel):
#     payload: str



# @app.post("/encrypt")
# def encrypt_api(req: EncryptRequest):
#     encrypted = encrypt_data(req.text)
#     return {"encrypted_data": encrypted}



# @app.post("/decrypt")
# def decrypt_api(req: DecryptRequest):
#     decrypted = decrypt_data(req.payload)
#     return {"decrypted_data": decrypted}