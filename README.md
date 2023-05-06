# Connect/Disconnect to the Internet with Python

This Python script allows you to connect or disconnect to the Internet by logging in or out of a specified network. It also includes options to check the connection status and VPN status.

## Requirements

- Python 3
- `requests` library
- macOS or Windows operating system (for WiFi connection)

## Usage

To use the script, navigate to the directory containing the Python file in the terminal and run it with the desired arguments.

### Arguments

- `-u`, `--username`: Username for network login
- `-p`, `--password`: Password for network login
- `-c`, `--connect`: Connect to the Internet
- `-d`, `--disconnect`: Disconnect from the Internet
- `-s`, `--status`: Check connection status
- `-v`, `--vpn`: Check VPN connection status

### Examples

- Connect to the Internet with default network and login credentials:

`python connect.py -c`

- Connect to the Internet with custom login credentials:

`python connect.py -c -u your_username -p your_password`

- Disconnect from the Internet:

`python connect.py -d`

- Check connection status:

`python connect.py -s`

- Check VPN connection status:

`python connect.py -v`


## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
