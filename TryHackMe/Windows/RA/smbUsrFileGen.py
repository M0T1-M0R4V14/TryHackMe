import subprocess
import argparse
from colorama import init, Fore, Style

# Initialize colorama to support colored output on Windows
init(autoreset=True)

def run_crackmapexec(username, password, server_ip, verbose=False):
    command = f"crackmapexec smb {server_ip} -u '{username}' -p '{password}' --rid-brute"
    try:
        if verbose:
            print(Fore.CYAN + f"[*] Executing command: {command}" + Style.RESET_ALL)
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return e.output

def parse_output(output):
    usernames = []
    lines = output.splitlines()
    for line in lines:
        if "SMB" in line and "SidTypeUser" in line:
            parts = line.split("\\")
            if len(parts) > 1:
                usernames.append(parts[1].split()[0])
    return usernames

def main():
    parser = argparse.ArgumentParser(description="Execute crackmapexec with specified parameters.")
    parser.add_argument("-u", "--username", required=True, help="SMB username")
    parser.add_argument("-p", "--password", required=True, help="SMB password")
    parser.add_argument("-i", "--server_ip", required=True, help="SMB server IP address")
    parser.add_argument("-o", "--output_file", required=True, help="Output file for usernames")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

    # Parse arguments and handle missing arguments gracefully
    try:
        args = parser.parse_args()
    except argparse.ArgumentError as exc:
        print(Fore.RED + f"Error parsing arguments: {exc}" + Style.RESET_ALL)
        parser.print_help()
        return
    except SystemExit:
        return

    if not args.username or not args.password or not args.server_ip or not args.output_file:
        print(Fore.RED + "Error: One or more required parameters are missing." + Style.RESET_ALL)
        parser.print_help()
        return

    output = run_crackmapexec(args.username, args.password, args.server_ip, args.verbose)

    if "Brute forcing RIDs" in output:
        print(Fore.GREEN + "[+] Command executed successfully." + Style.RESET_ALL)
        if args.verbose:
            print(Fore.CYAN + "Verbose Output:" + Style.RESET_ALL)
            lines = output.splitlines()
            for line in lines:
                if "SMB" in line:
                    if "SidTypeUser" in line:
                        print(Fore.GREEN + line + Style.RESET_ALL)
                    else:
                        print(Fore.CYAN + line + Style.RESET_ALL)
                else:
                    print(line)
        usernames = parse_output(output)
        with open(args.output_file, 'w') as f:
            for username in usernames:
                f.write(username + "\n")
        print(Fore.CYAN + f"Usernames written to {args.output_file}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "[-] Command failed:" + Style.RESET_ALL)
        print(output)

if __name__ == "__main__":
    main()

