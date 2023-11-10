# CheckMyCerts
CheckMyCerts is a Python-based command-line tool designed for retrieving and displaying SSL/TLS certificate details from specified hosts. It provides valuable insights into certificate configurations, such as the certificate's name, issue, and expiry dates, and whether it is self-signed or expired.

## Features
- Retrieve SSL/TLS certificate details from specified hosts and ports.
- Display certificate details in a user-friendly tabular format.
- Check if certificates are self-signed.
- Determine if certificates have expired based on the current system date.
- Option to export the results to a CSV file.
- Debug mode for detailed error reporting.

## Requirements
- Python 3.x
- PrettyTable

## Installation
To use CheckMyCerts, clone this repository and install the required Python packages.

Clone the repository:
```normal
git clone https://github.com/smhuda/checkmycerts.git
```
Navigate to the cloned directory:

```normal
cd checkmycerts
```

## Install the required packages:

```normal
pip install -r requirements.txt
```

## Usage
Run the script from the command line by specifying either a single host and port or a file containing multiple hosts and ports.

### To check a single host and port:
```normal
python checkmycerts.py -hp host:port
```

### To check multiple hosts and ports from a file:

```normal
python checkmycerts.py -f path_to_file
```

### Enable debug mode to print detailed error messages:

```normal
python checkmycerts.py -hp host:port -d
```

## Contributing
Contributions to CheckMyCerts are welcome! Feel free to open a pull request with enhancements or fixes.

If you liked this or it helped you in anyway, would you like to [!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/smhuda)
