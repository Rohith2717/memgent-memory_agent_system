import httpx

class LLMClient:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama3"

    async def generate(self, prompt: str, context: list[dict]) -> str:
        context_text = "\n".join(context)

        final_prompt = f"""
Previous Context:
{context_text}

User Input:
{prompt}
""".strip()

        try:
            async with httpx.AsyncClient(timeout=120) as client:
                resp = await client.post(
                    self.url,
                    json={
                        "model": self.model,
                        "prompt": final_prompt,
                        "stream": False
                    }
                )
        except Exception as e:
            # explicit message
            return f"[LLM CONNECTION ERROR] {repr(e)}"

        try:
            data = resp.json()
        except Exception:
            return "[LLM ERROR] Invalid JSON response from model server"

        if isinstance(data, dict):
            if "response" in data and data["response"]:
                return data["response"]
            if "error" in data:
                return f"[LLM ERROR] {data['error']}"

        return "[LLM ERROR] Empty or unknown LLM response"
