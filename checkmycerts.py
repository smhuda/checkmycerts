import subprocess
import csv
import sys
import argparse
from prettytable import PrettyTable
from datetime import datetime

def show_banner():
    banner = """

█▀▀ █──█ █▀▀ █▀▀ █─█ █▀▄▀█ █──█ █▀▀ █▀▀ █▀▀█ ▀▀█▀▀ █▀▀ ─ █▀▀█ █──█ 
█── █▀▀█ █▀▀ █── █▀▄ █─▀─█ █▄▄█ █── █▀▀ █▄▄▀ ──█── ▀▀█ ▄ █──█ █▄▄█ 
▀▀▀ ▀──▀ ▀▀▀ ▀▀▀ ▀─▀ ▀───▀ ▄▄▄█ ▀▀▀ ▀▀▀ ▀─▀▀ ──▀── ▀▀▀ █ █▀▀▀ ▄▄▄█
    """
    print(banner)

def extract_cn(field):
    # Extract CN value from the given field
    cn_index = field.find('CN=')
    if cn_index != -1:
        cn_end_index = field.find(',', cn_index)
        if cn_end_index == -1:
            cn_end_index = len(field)
        return field[cn_index + 3:cn_end_index].strip()
    return ''

def parse_date(date_string):
    # Parse date from OpenSSL output
    return datetime.strptime(date_string.strip(), '%b %d %H:%M:%S %Y %Z')

def get_certificate_details(host, port, debug):
    try:
        # Run openssl to get detailed certificate information
        cmd = f"echo | openssl s_client -servername {host} -connect {host}:{port} 2>&1 | openssl x509 -text"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()

        if debug:
            print(f"Debug Info for {host}:{port}:\n{stderr.decode()}\n")

        # Extract Subject, Issuer, and validity dates from the output
        output = stdout.decode()
        subject = output[output.find('Subject:'):output.find('\n', output.find('Subject:'))]
        issuer = output[output.find('Issuer:'):output.find('\n', output.find('Issuer:'))]
        not_before = output[output.find('Not Before:'):output.find('\n', output.find('Not Before:'))]
        not_after = output[output.find('Not After :'):output.find('\n', output.find('Not After :'))]

        # Extract CN from Subject and Issuer
        subject_cn = extract_cn(subject)
        issuer_cn = extract_cn(issuer)

        # Check if self-signed
        is_self_signed = subject_cn == issuer_cn

        # Check if expired
        expiry_date = parse_date(not_after.split(': ')[1])
        is_expired = expiry_date < datetime.now()

        return subject, not_before.split(': ')[1], not_after.split(': ')[1], is_self_signed, is_expired
    except Exception as e:
        if debug:
            print(f"Error while processing {host}:{port}: {e}")
        return None, None, None, None, None

def display_and_save_results(results):
    table = PrettyTable()
    table.field_names = ["Host:Port", "Certificate Name", "Issue Date", "Expiry Date", "Self-Signed", "Expired"]
    table.align = "l"
    table.valign = "m"
    table.border = True
    table.horizontal_char = "="
    table.vertical_char = "|"
    table.junction_char = "+"
    table.format = True
    table.sortby = "Host:Port"
    table.max_width = 20  # Adjust max width of each column

    for host, port, name, issue_date, expiry_date, self_signed, expired in results:
        table.add_row([f"{host}:{port}", name, issue_date, expiry_date, "Yes" if self_signed else "No", "Yes" if expired else "No"])

    print(table.get_string())

    export_csv = input("Do you want to export the results to a CSV file? (yes/no): ").strip().lower()
    if export_csv == 'yes':
        csv_filename = input("Enter the CSV filename: ").strip()
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Host:Port", "Certificate Name", "Issue Date", "Expiry Date", "Self-Signed", "Expired"])
            for row in results:
                writer.writerow(row)
        print(f"Results exported to {csv_filename}")

def main():
    show_banner()
    parser = argparse.ArgumentParser(description='Gather SSL certificate details from specified hosts.')
    parser.add_argument('-f', '--file', help='Path to file containing host and port pairs (host:port per line).')
    parser.add_argument('-hp', '--hostport', help='Specify a single host and port pair (format host:port).')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode to print the whole stderr.')
    args = parser.parse_args()

    if args.hostport:
        results = [(args.hostport.split(':')[0], args.hostport.split(':')[1], *get_certificate_details(*args.hostport.split(':'), args.debug))]
    elif args.file:
        results = []
        with open(args.file, 'r') as file:
            for line in file:
                host, port = line.strip().split(':')
                results.append((host, port, *get_certificate_details(host, port, args.debug)))
    else:
        parser.print_help()
        sys.exit(1)

    display_and_save_results(results)

if __name__ == "__main__":
    main()
