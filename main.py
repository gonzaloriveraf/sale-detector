from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"healthy": True}
```

---

**`requirements.txt`**
```
fastapi==0.111.0
uvicorn[standard]==0.29.0