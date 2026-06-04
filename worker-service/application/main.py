# worker.py
import json
import time
import redis
from core.config import settings
from core.pipeline import InferenceEngine
from db.database import SessionLocal
from db.models import JobModel

def run_worker():
    # 1. Initialize backend engines
    r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_SERVICE_PORT, decode_responses=True)
    predictor = InferenceEngine()
    db = SessionLocal()
    
    print(f"Worker active. Listening to queue: '{settings.REDIS_QUEUE_NAME}'...")
    
    try:
        while True:
            # blpop blocks until an item is pushed onto the list. 
            # 0 means wait indefinitely. Returns tuple: (queue_name, data)
            _, raw_data = r.blpop(settings.REDIS_QUEUE_NAME, timeout=0)
            
            # Parse payload
            payload = json.loads(raw_data)
            job_id = payload["job_id"]
            text_to_analyze = payload["text"]
            
            print(f"\n[Processing] Job {job_id}")
            
            # 2. Update status to 'processing'
            job_record = db.query(JobModel).filter(JobModel.id == job_id).first()
            if job_record:
                job_record.status = "processing"
                db.commit()
            
            try:
                # 3. Run Inference
                sentiment, confidence = predictor.predict(text_to_analyze)
                
                # 4. Save results and mark as 'done'
                if job_record:
                    job_record.status = "done"
                    job_record.result = sentiment
                    job_record.confidence = confidence
                    db.commit()
                print(f"[Success] Job {job_id} resolved as {sentiment} ({confidence*100:.1f}%)")
                
            except Exception as e:
                print(f"[Failure] Job {job_id} failed during execution: {str(e)}")
                if job_record:
                    job_record.status = "failed"
                    db.commit()
                    
    except KeyboardInterrupt:
        print("\nWorker shutting down gracefully...")
    finally:
        db.close()

if __name__ == "__main__":
    run_worker()