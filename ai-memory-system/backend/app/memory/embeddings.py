def embed(text: str) -> list[float]:
    vec = [float(ord(c)) for c in text[:64]]
    
    # pad with zeros if shorter than 64
    if len(vec) < 64:
        vec.extend([0.0] * (64 - len(vec)))
    
    return vec
