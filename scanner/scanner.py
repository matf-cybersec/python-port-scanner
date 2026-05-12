"""High-level scanner orchestration and thread management."""

import concurrent.futures
import logging
from dataclasses import dataclass
from typing import List, Optional

from scanner import network
from scanner import utils


@dataclass
class ScanResult:
    port: int
    status: str
    service: str
    banner: Optional[str]
    error: Optional[str]


class PortScanner:
    def __init__(
        self,
        host: str,
        ports: List[int],
        timeout: float = 1.0,
        banner_grab: bool = False,
        use_threads: bool = True,
        thread_count: int = 20,
        verbose: bool = False,
    ) -> None:
        self.host = host
        self.ports = ports
        self.timeout = timeout
        self.banner_grab = banner_grab
        self.use_threads = use_threads
        self.thread_count = max(1, thread_count)
        self.verbose = verbose
        self.target_ip = ""

    def run(self) -> List[ScanResult]:
        self.target_ip = utils.resolve_host(self.host)
        logging.info("Resolving host: %s", self.host)
        logging.info("Target address: %s", self.target_ip)
        logging.info("Scanning %d ports", len(self.ports))

        if self.use_threads:
            return self._run_threaded()

        return [self._scan_port(port) for port in self.ports]

    def _run_threaded(self) -> List[ScanResult]:
        logging.info("Fast scan mode enabled with %d threads", self.thread_count)
        results: List[ScanResult] = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            future_to_port = {
                executor.submit(self._scan_port, port): port for port in self.ports
            }

            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    result = future.result()
                except Exception as exc:
                    logging.debug("Unexpected error scanning port %d: %s", port, exc)
                    result = ScanResult(
                        port=port,
                        status="error",
                        service=utils.get_service_name(port),
                        banner=None,
                        error=str(exc),
                    )
                results.append(result)

        results.sort(key=lambda entry: entry.port)
        return results

    def _scan_port(self, port: int) -> ScanResult:
        port_data = network.scan_port(
            self.target_ip,
            port,
            timeout=self.timeout,
            banner_grab=self.banner_grab,
        )
        status = "open" if port_data.is_open else "closed"
        service = utils.get_service_name(port)

        if self.verbose:
            logging.debug(
                "Port %d: %s, service=%s, banner=%s, error=%s",
                port,
                status,
                service,
                port_data.banner,
                port_data.error,
            )

        return ScanResult(
            port=port,
            status=status,
            service=service,
            banner=port_data.banner,
            error=port_data.error,
        )
