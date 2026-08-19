from fastapi import FastAPI

app = FastAPI(title="AWS Linux Support Lab")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "aws-linux-support-lab"}

