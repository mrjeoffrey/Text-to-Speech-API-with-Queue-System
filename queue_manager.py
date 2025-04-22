import asyncio
import os
from dotenv import load_dotenv
import edge_tts
import aiohttp

load_dotenv()

MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", 50))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

class JobManager:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        asyncio.create_task(self.process_jobs())

    async def add_job(self, job_id, job_data):
        await self.queue.put((job_id, job_data))

    async def process_jobs(self):
        while True:
            job_id, job_data = await self.queue.get()
            async with self.semaphore:
                await self.process_job(job_id, job_data)

    async def process_job(self, job_id, job_data):
        try:
            tts = edge_tts.Communicate(
                text=job_data["text"],
                voice=job_data["voice"],
                rate=f"{job_data['speed']}%",
                volume=f"{job_data['volume']}%",
                pitch=f"{job_data['pitch']}%"
            )
            output_file = f"{job_id}.mp3"
            await tts.save(output_file)

            # Notify webhook
            await self.notify_webhook(job_id, "success")
        except Exception as e:
            await self.notify_webhook(job_id, "failure", str(e))

    async def notify_webhook(self, job_id, status, error=None):
        if not WEBHOOK_URL:
            return
        async with aiohttp.ClientSession() as session:
            payload = {"job_id": job_id, "status": status, "error": error}
            await session.post(WEBHOOK_URL, json=payload)
