import click
import win32pipe
import win32file
import pywintypes

MODES = {
    "inbound": win32pipe.PIPE_ACCESS_INBOUND,
    "outbound": win32pipe.PIPE_ACCESS_OUTBOUND,
}

@click.group()
def cli():
    """
    This CLI tool demonstrates a simple usage of Windows Named Pipes. Example:

    # Run in terminal 1:

        create -m inbound test
    
    # Run in terminal 2:

        write test   
 
        <enter messages>
    """

@cli.command("create", help="Creates a named pipe either in inbound or outbound mode")
@click.option("-m", "--mode", type=click.Choice([m for m in MODES], case_sensitive=False), default="inbound", help="Operation mode.")
@click.argument("name")
def create(name: str, mode: str):
    addr = f'\\\\.\\pipe\\{name}'
    pipe = win32pipe.CreateNamedPipe(
        addr,
        MODES[mode],
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None
    )
    print(f"created {mode} pipe: {addr}")
    win32pipe.ConnectNamedPipe(pipe, None)
    print("got client")
    try:
        while True:
            if mode == "inbound":
                result, data = win32file.ReadFile(pipe, 64 * 1024)
                print("Reader received message: " + data.decode())
            elif mode == "outbound":
                message = input()
                win32file.WriteFile(pipe, message.encode())
    except pywintypes.error as e:
        if e.winerror == 109:
            print("Reader pipe closed")
        else:
            print(e)
    finally:
        win32file.CloseHandle(pipe)


@cli.command("read", help="Reads from an existing named pipe")
@click.argument("name")
def read(name: str):
    addr = f'\\\\.\\pipe\\{name}'
    try:
        handle = win32file.CreateFile(
            addr,
            win32file.GENERIC_READ,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )
        while True:
            result, message = win32file.ReadFile(handle, 64*1024)
            print(f"message: {message.decode()}")
    except pywintypes.error as e:
        if e.winerror == 109:
            print("Reader pipe closed")
        else:
            print(e)

@cli.command("write", help="Writes to an existing named pipe")
@click.argument("name")
def write(name: str):
    addr = f'\\\\.\\pipe\\{name}'
    try:
        handle = win32file.CreateFile(
            addr,
            win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )
        while True:
            message = input() + "\n"
            resp = win32file.WriteFile(handle, message.encode())
    except pywintypes.error as e:
        if e.winerror == 109:
            print("Reader pipe closed")
        else:
            print(e)

if __name__ == "__main__":
    cli()