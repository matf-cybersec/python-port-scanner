# Python TCP Port Scanner

A professional and educational TCP port scanner written in Python. This project is designed for cybersecurity learners and junior developers who want to demonstrate networking fundamentals, clean architecture, and realistic port scanning behavior.

## Features

- Scan a single host by IP or hostname
- Scan a list or range of ports
- Configurable timeout for TCP connections
- Optional banner grabbing for service inspection
- Basic service identification for common ports
- Colored CLI output for better readability
- Progress and status messages during scans
- Graceful error handling and Ctrl+C interruption support
- Export scan results to TXT or JSON
- Verbose mode for debugging and detailed logs
- Fast scan mode using thread-based concurrency
- Clear separation between scanning logic and CLI logic

## Instalação / Installation

1. Clone o repositório:

```bash
git clone https://github.com/username/python-port-scanner.git
cd python-port-scanner
```

2. Crie um ambiente virtual e instale as dependências:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso / Usage

Execute o scanner pela linha de comando:

```bash
python main.py --host scanme.nmap.org --ports 22,80,443 --timeout 1.5 --fast --banner --export json --output results.json
```

### Example commands

```bash
python main.py --host 127.0.0.1 --ports 1-1024 --timeout 1.0 --fast
python main.py --host example.com --ports 22,80,443 --banner --export txt --output scan.txt
python main.py --host 192.168.1.10 --ports 20-25 --verbose
```

## Example output

```text
[INFO] Resolving host: example.com
[INFO] Scanning 3 ports on example.com (93.184.216.34)
[OPEN] 22/tcp  - ssh
[CLOSED] 80/tcp
[OPEN] 443/tcp - https

Results saved to scan-results.json
```

## Files

- `localhost-scan-example.json`
  - Basic localhost scan exported as JSON

- `localhost-scan-example.txt`
  - Basic localhost scan exported as TXT

- `verbose-local-scan.json`
  - Verbose scan showing detection of a local HTTP server running on port 8000

## Networking concepts used

- TCP connect scans use a full three-way handshake to determine whether a port is accepting connections.
- The scanner creates a socket and attempts to connect to each port.
- A successful connection means the port is open; a timeout or connection refused indicates the port is closed or filtered.
- Banner grabbing reads a small amount of data after connection to identify application services.
- ThreadPoolExecutor enables faster scanning by performing multiple TCP connections concurrently.

## Aviso educacional / Educational disclaimer

Este projeto é destinado a fins de aprendizado e demonstração. Realize varreduras apenas em hosts que você possui ou tem permissão expressa para testar. Scans não autorizados podem ser considerados ilegais.

## Future improvements

- Add UDP scanning support
- Add service fingerprinting with protocol-specific probes
- Support output to CSV
- Add a graphical user interface or web dashboard
- Implement rate limiting and scan scheduling

## Screenshots

![Placeholder screenshot 1](screenshots/screenshot-1.png)
![Placeholder screenshot 2](screenshots/screenshot-2.png)

---

## Estrutura do projeto / Project structure

```text
python-port-scanner/
├── README.md
├── requirements.txt
├── .gitignore
├── scanner/
│   ├── __init__.py
│   ├── scanner.py
│   ├── network.py
│   ├── banner.py
│   ├── output.py
│   └── utils.py
├── examples/
├── screenshots/
└── main.py
```
