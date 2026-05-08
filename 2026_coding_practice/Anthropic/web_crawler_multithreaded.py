"""
https://leetcode.com/problems/web-crawler-multithreaded/solutions/418126/python3-multithreaded-bfs-with-queue-by-8pjim/

Use Lock: for worker writes: during add in "visited" set and "queue" 

Use Concurrent.Future for thread executors
        with futures.ThreadPoolExecutor(max_workers=8) as executor:
            for i in range(8): executor.submit(worker)
"""
from concurrent import futures
from Queue import Queue

import threading
class Solution(object):
    def crawl(self, startUrl, htmlParser):
        common_host = startUrl.split('/')[2]
        queue, seen, seen_lock = Queue(), {startUrl}, threading.Lock()
        def worker():
            try:
                while True:
                    url = queue.get(timeout=0.015) # make sure wait up to the time required for the `getUrls` call
                    for next_url in htmlParser.getUrls(url):
                        if next_url not in seen and next_url.split('/')[2] == common_host:
                            seen_lock.acquire()
                            # Acquire lock to ensure urls are no enqueed multiple times
                            if next_url not in seen:
                                seen.add(next_url)
                                queue.put(next_url)
                            seen_lock.release()
                    queue.task_done()
            except: pass
        
        queue.put(startUrl)
        with futures.ThreadPoolExecutor(max_workers=8) as executor:
            for i in range(8): executor.submit(worker)
        
        return list(seen)