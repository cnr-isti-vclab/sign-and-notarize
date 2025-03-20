import os
import sys
import argparse
import subprocess
import re

def main():
    parser = argparse.ArgumentParser(description='Sign files using signtool.exe')
    parser.add_argument('-i', '--input_path', required=True, help='Path to the input file or directory')
    parser.add_argument('-cf', '--cert_file', required=True, help='Path to the certificate file')
    parser.add_argument('-cp', '--cert_pssw', required=True, help='Password for the certificate file')

    args = parser.parse_args()

    input_path = args.input_path
    cert_file = args.cert_file
    cert_pssw = args.cert_pssw

    if not os.path.isfile(cert_file):
        print(f"Certificate file {cert_file} not found. Exiting...")
        sys.exit(1)

    cert_win = cert_file.replace('/', '\\')

    if not os.path.exists(input_path):
        print(f"Input path {input_path} not found. Exiting...")
        sys.exit(1)
    else:
        print(f"Input path: {input_path}")

    def sign_file(file_path):
        if file_path.endswith('.dll') or file_path.endswith('.exe'):
            print(f"Signing {file_path}...")
            file_win = file_path.replace('/', '\\')
            try:
                subprocess.run([
                    'signtool.exe', 'sign', '/fd', 'SHA256', '/f', cert_win, '/p', cert_pssw, 
                    '/t', 'http://timestamp.comodoca.com/authenticode', file_win
                ], check=True)
            except subprocess.CalledProcessError as e:
                print(f"An error occurred: {e}")
                sys.exit(1)

    if os.path.isfile(input_path):
        sign_file(input_path)
    elif os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                sign_file(os.path.join(root, file))
    else:
        print("Input path not found. Exiting...")
        sys.exit(1)

if __name__ == "__main__":
    main()