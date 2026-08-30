from fastapi import FastAPI
from client.rq_client import queue
from queues.worker import process

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
def chat(user_query: str):
    job = queue.enqueue(process, user_query)
    return {"status": "success", "job_id": job.id}

@app.get("/job_status/{job_id}")
def job_status(job_id: str):
    job = queue.fetch_job(job_id)
    result = job.return_value()
    return {"status": job.get_status(), "result": result}
