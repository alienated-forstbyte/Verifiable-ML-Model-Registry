from hash_model import hash_model

original_hash = "PUT_HASH_HERE"

current_hash = hash_model("model.pkl")

if original_hash == current_hash:
    print("Model verified")
else:
    print("Model tampered")