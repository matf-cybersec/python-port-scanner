# Python TCP Port Scanner

A modular TCP port scanner built with Python, featuring threaded scanning, optional banner grabbing, service identification, and JSON/TXT export. Developed as a cybersecurity learning project focused on network reconnaissance and Python development.

## Features

- Scan a single host by IP address or hostname.
- Support for comma-separated ports and port ranges (e.g., `22,80,443,8000-8100`).
- Configurable TCP connection timeout.
- Optional banner grabbing for open ports.
- Built-in service identification for common ports.
- Colored CLI output with optional `--no-color` flag.
- Thread-based scanning with `--fast` and configurable `--threads`.
- JSON and TXT export of scan results.
- Input validation for port ranges, positive timeout values, and positive thread counts.
- Error handling for invalid input and unresolved hosts.
- Verbose logging with `--verbose`.

## Installation

```bash
git clone https://github.com/matf-cybersec/python-port-scanner.git
cd python-port-scanner

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt
```

## Usage

```bash
python main.py --host scanme.nmap.org --ports 22,80,443 --timeout 1.5 --fast --banner --export json --output results.json
```

## CLI Options

| Argument | Description |
|---|---|
| `--host` | Hostname or IP address to scan (required). |
| `--ports` | Comma-separated ports and ranges. |
| `--timeout` | TCP connection timeout in seconds; must be greater than zero. |
| `--banner` | Enable optional banner grabbing. |
| `--fast` | Enable threaded scanning. |
| `--threads` | Number of worker threads; must be positive and only applies with `--fast`. |
| `--export` | Export format: `json` or `txt`. |
| `--output` | Export file path; required when using `--export`. |
| `--verbose` | Enable debug logging. |
| `--no-color` | Disable ANSI color output. |

## Examples

```bash
# Scan common ports
python main.py --host 127.0.0.1 --ports 22,80,443

# Scan a port range using threads
python main.py --host 127.0.0.1 --ports 1-1024 --fast --threads 20

# Grab banners and export results
python main.py --host example.com --ports 22,80,443 --banner --export txt --output scan.txt

# Enable verbose logging
python main.py --host 192.168.1.10 --ports 20-25 --verbose

# Export results to JSON
python main.py --host 192.168.1.5 --ports 22,80,443 --export json --output ./results/scan.json
```

## Example Output

```text
[INFO] Resolving host: example.com
[INFO] Target address: 93.184.216.34
[INFO] Scanning 3 ports
[OPEN] 22/tcp - ssh
[CLOSED] 80/tcp - http
[OPEN] 443/tcp - https

Scanned 3 ports: 2 open, 1 closed, 0 filtered, 0 with errors
[INFO] Results saved to results.json
```

## Export Formats

- **JSON:** Includes port, status, service, banner, and error details.
- **TXT:** Lists scanned ports with their status, service, and optional banner or error information.

## Project Structure

```text
python-port-scanner/
├── README.md
├── CHANGELOG.md
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
│   ├── scan-results.jpg
│   └── verbose-scan.jpg
└── main.py
```

## Notes

- Use scans only on hosts you own or have permission to test.
- A timeout error is treated as a filtered port and may indicate network filtering or packet loss.
- The scanner supports up to 1024 unique ports by default, but more can be scanned as needed.

## Changelog

See `CHANGELOG.md` for the full list of recent upgrades and release notes.

## Publishing to GitHub

1. Stage the updated files:
   ```bash
   git add README.md CHANGELOG.md main.py scanner/network.py scanner/scanner.py scanner/output.py scanner/utils.py
   ```

````
2. Commit with a descriptive message:
   ```bash
git commit -m "Document scanner upgrades and add changelog for CLI, export, timeout, and threading improvements"
````

3. Push the branch to GitHub:
   ```bash
   git push origin your-branch-name
   ```

```
4. Create a Pull Request or release on GitHub and use the changelog entries as release notes.
```
