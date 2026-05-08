import heapq
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from collections import deque
from datetime import datetime
from html.parser import HTMLParser
from urllib.parse import unquote, urljoin, urlparse

import requests

_CHROME_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    )
}

banned_links = [
    "/wiki/Category:",
    "/wiki/Help:",
    "/wiki/Special:",
    "/wiki/Portal:",
    "/wiki/File:",
    "/wiki/Wikipedia:"
]


class _WikiPageHTML(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self._base = base_url
        self.title: str | None = None
        self.urls: list[str] = []
        self._seen: set[str] = set()
        self._in_title = False
        self._title_buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: v for k, v in attrs if v is not None}
        if tag == "title":
            self._in_title = True
            return
        if tag != "a" or "href" not in a:
            return
        u = urljoin(self._base, a["href"])
        p = urlparse(u)
        if any(s in u for s in banned_links):
            return
        if (
            p.scheme in {"http", "https"}
            and p.netloc == "en.wikipedia.org"
            and p.path.startswith("/wiki/")
        ):
            if u not in self._seen:
                self._seen.add(u)
                self.urls.append(u)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self._in_title:
            self._in_title = False
            self.title = "".join(self._title_buf).strip()
            self._title_buf.clear()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_buf.append(data)


def _wiki_slug_first_bucket(url: str) -> str:
    """First character of the article slug (lowercase), for diversity-aware ordering."""
    path = unquote(urlparse(url).path)
    if not path.startswith("/wiki/"):
        return "\xff"
    slug = path[len("/wiki/") :].split("/")[0]
    if not slug:
        return "\xff"
    return slug[0].lower()


class _BucketWeightedFrontier:
    """Min-heap: lower weight is popped first. Weight = same-bucket count at enqueue time."""

    def __init__(self) -> None:
        self._heap: list[tuple[int, int, str]] = []
        self._seq = 0
        self._bucket_counts: dict[str, int] = {}

    def __bool__(self) -> bool:
        return bool(self._heap)

    def push(self, url: str) -> None:
        b = _wiki_slug_first_bucket(url)
        w = self._bucket_counts.get(b, 0)
        self._bucket_counts[b] = w + 1
        heapq.heappush(self._heap, (w, self._seq, url))
        self._seq += 1

    def pop(self) -> str:
        _, _, url = heapq.heappop(self._heap)
        b = _wiki_slug_first_bucket(url)
        self._bucket_counts[b] -= 1
        if self._bucket_counts[b] == 0:
            del self._bucket_counts[b]
        return url


def fetch_page(url: str) -> str:
    response = requests.get(url, headers=_CHROME_HEADERS, timeout=15)
    response.raise_for_status()
    return response.text


# Fixed-length sliding window for rate limiting (only the max GET count is tunable).
_FIXED_SLIDING_WINDOW_SECONDS = 5.0


def _wall_clock_ts() -> str:
    return datetime.now().isoformat(timespec="milliseconds")


class _SlidingWindowVisitLimiter:
    """At most `max_http_gets` GETs in any rolling _FIXED_SLIDING_WINDOW_SECONDS interval."""

    def __init__(self, max_http_gets: int) -> None:
        self._max = max_http_gets
        self._visit_starts: deque[float] = deque()

    def before_visit(self) -> None:
        w = _FIXED_SLIDING_WINDOW_SECONDS
        now = time.monotonic()
        # Sliding window: GET timestamps older than w seconds drop out — not counted anymore.
        while self._visit_starts and self._visit_starts[0] <= now - w:
            self._visit_starts.popleft()
        # Still at cap → must wait until the oldest kept GET ages past the window edge.
        if len(self._visit_starts) >= self._max:
            wait = self._visit_starts[0] + w - now
            if wait > 0:
                print(
                    f"{_wall_clock_ts()}  RATE_LIMIT  sleep {wait:.3f}s  "
                    f"({self._max} GETs / {w:g}s rolling window; "
                    "waiting for oldest GET to exit window)"
                )
                time.sleep(wait)
            now = time.monotonic()
            while self._visit_starts and self._visit_starts[0] <= now - w:
                self._visit_starts.popleft()
        # Record this GET at the slot we use for the next window checks (monotonic clock).
        self._visit_starts.append(time.monotonic())


# Parallel download hint (I/O-bound); scale-out would shard the frontier across processes/nodes.
_IO_WORKERS = 4


def main(max_urls: int = 10, max_http_gets_per_window: int = 10) -> None:
    base_url = "https://en.wikipedia.org/wiki/Google"
    frontier = _BucketWeightedFrontier()
    scheduled: set[str] = set()

    # Seed start URL (outside parser flow).
    scheduled.add(base_url)
    frontier.push(base_url)

    fetched = 0
    limiter = _SlidingWindowVisitLimiter(max_http_gets_per_window)
    limit_lock = threading.Lock()

    def fetch_one(url: str) -> tuple[str, str, list[str]]:
        with limit_lock:
            limiter.before_visit()
        html = fetch_page(url)
        parser = _WikiPageHTML(url)
        parser.feed(html)
        parser.close()
        return url, parser.title or "", parser.urls

    with ThreadPoolExecutor(max_workers=min(_IO_WORKERS, max_urls)) as pool:
        while frontier and fetched < max_urls:
            batch_cap = min(_IO_WORKERS, max_urls - fetched)
            batch: list[str] = []
            while frontier and len(batch) < batch_cap:
                batch.append(frontier.pop())
            if not batch:
                break
            for current, title, outs in pool.map(fetch_one, batch):
                fetched += 1
                b = _wiki_slug_first_bucket(current)
                print(
                    f"{_wall_clock_ts()}  GET  {fetched}  bucket={repr(b)}  "
                    f"{[current, title]}"
                )
                for u in outs:
                    if u not in scheduled:
                        scheduled.add(u)
                        frontier.push(u)


if __name__ == "__main__":
    main()
