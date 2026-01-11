from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.startup import on_startup

app = FastAPI(on_startup=[on_startup])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

"""
 If you want next (optional, not required):

1️⃣ “Help me prepare demo + explanation script”
2️⃣ “Convert this into resume project description”
3️⃣ “Prepare system-design interview explanation”

Say the number — otherwise, you’re done ✅
"""