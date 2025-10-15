# pywinpipe

This CLI tool demonstrates a simple usage of [Windows Named Pipes](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipes). Example:

```bash
# Run in terminal 1:

    create -m inbound test

# Run in terminal 2:

    write test

    <enter messages>

Options:
  --help  Show this message and exit.

Commands:
  create  Creates a named pipe either in inbound or outbound mode
  read    Reads from an existing named pipe
  write   Writes to an existing named pipe

```

# Setup

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```
