# MIT License
# 
# Copyright (c) 2024 Warren Houghton
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import binascii
import argparse
from Crypto.Cipher import DES3

def banner():
    print("""
 ██▓███   ██▓ ▄████▄   ▒█████    ▄████ ▓█████  ███▄    █ 
▓██░  ██▒▓██▒▒██▀ ▀█  ▒██▒  ██▒ ██▒ ▀█▒▓█   ▀  ██ ▀█   █ 
▓██░ ██▓▒▒██▒▒▓█    ▄ ▒██░  ██▒▒██░▄▄▄░▒███   ▓██  ▀█ ██▒
▒██▄█▓▒ ▒░██░▒▓▓▄ ▄██▒▒██   ██░░▓█  ██▓▒▓█  ▄ ▓██▒  ▐▌██▒
▒██▒ ░  ░░██░▒ ▓███▀ ░░ ████▓▒░░▒▓███▀▒░▒████▒▒██░   ▓██░
▒▓▒░ ░  ░░▓  ░ ░▒ ▒  ░░ ▒░▒░▒░  ░▒   ▒ ░░ ▒░ ░░ ▒░   ▒ ▒ 
░▒ ░      ▒ ░  ░  ▒     ░ ▒ ▒░   ░   ░  ░ ░  ░░ ░░   ░ ▒░
░░        ▒ ░░        ░ ░ ░ ▒  ░ ░   ░    ░      ░   ░ ░ 
          ░  ░ ░          ░ ░        ░    ░  ░         ░ 
             ░                                           
Author - 00Waz
    """)

def print_help():
    help_text = """
    Usage: python3 picogen.py [OPTIONS]

    Options:
      -cn, --card_number <number>   Starting card number
      -fc, --facility_code <code>   Facility code
      -f, --format <type>           Data format type
      -num, --count <number>        Number of card numbers to generate
      -o, --output <directory>      Custom output directory
      --info                        Show this help message and exit
        """
    print(help_text)

def calculate_even_parity(data):
    return sum(int(bit) for bit in data) % 2 == 0

def calculate_odd_parity(data):
    return sum(int(bit) for bit in data) % 2 == 1

def decimal_to_binary(decimal, bit_length):
    binary = bin(decimal)[2:]
    return '0' * (bit_length - len(binary)) + binary

def generate_card_numbers(card_number, facility_code, count, format_type):
    card_numbers = []
    
    # Check if the format type is supported
    if format_type not in ["h10301", "h10306", "c1k35s", "h10304", "c1k48s"]:
        print(f"Unsupported format type: {format_type}")
        return card_numbers

    for i in range(count):
        if format_type == "h10301":
            # Checks if within range of format
            if facility_code < 1 or facility_code > 255:
                print("Facility code must be between 1 and 255.")
                break
            if card_number < 1 or card_number > 65535:
                print("Card number must be between 1 and 65535.")
                break

            # Convert values given to binary and stick together to generate credential string   
            binary_facility_code = decimal_to_binary(facility_code, 8)
            binary_card_number = decimal_to_binary(card_number, 16)
            cred_string = f'{binary_facility_code}{binary_card_number}'

            # Calculate parity for format
            even_parity_data = cred_string[:12]
            odd_parity_data = cred_string[12:] 
            odd_parity_bit = '0' if calculate_odd_parity(odd_parity_data) else '1'
            even_parity_bit = '0' if calculate_even_parity(even_parity_data) else '1'
            
            # Output entire PACS string for encryption and conversion
            formatted_data = f'01{even_parity_bit}{cred_string}{odd_parity_bit}'
            hex_format = hex(int(formatted_data, 2))[2:].zfill(16)
            card_numbers.append((hex_format, card_number))

        elif format_type == "h10306":
            # Checks if within range of format
            if facility_code < 1 or facility_code > 65535:
                print("Facility code must be between 1 and 65535.")
                break
            if card_number < 1 or card_number > 65535:
                print("Card number must be between 1 and 65535.")
                break

            # Convert values given to binary and stick together to generate credential string
            binary_facility_code = decimal_to_binary(facility_code, 16)
            binary_card_number = decimal_to_binary(card_number, 16)
            cred_string = f'{binary_facility_code}{binary_card_number}'

            # Calculate parity for format
            even_parity_data = cred_string[:16]
            odd_parity_data = cred_string[16:] 
            odd_parity_bit = '0' if calculate_odd_parity(odd_parity_data) else '1'
            even_parity_bit = '0' if calculate_even_parity(even_parity_data) else '1'

            # Output entire PACS string for encryption and conversion
            formatted_data = f'01{even_parity_bit}{cred_string}{odd_parity_bit}'
            hex_format = hex(int(formatted_data, 2))[2:].zfill(16)
            card_numbers.append((hex_format, card_number))

        elif format_type == "c1k35s":
            # Checks if within range of format
            if facility_code < 1 or facility_code > 4095:
                print("Facility code must be between 1 and 4095.")
                break
            if card_number < 1 or card_number > 1048575:
                print("Card number must be between 1 and 1048575.")
                break

            # Convert values given to binary and stick together to generate credential string
            binary_facility_code = decimal_to_binary(facility_code, 12)
            binary_card_number = decimal_to_binary(card_number, 20)
            cred_string = f'{binary_facility_code}{binary_card_number}'

            # Calculate parity for format
            even_parity_data1 = cred_string[0:2] + cred_string[3:5] + cred_string[6:8] + cred_string[9:11] + cred_string[12:14] + cred_string[15:17] + cred_string[18:20] + cred_string[21:23] + cred_string[24:26] + cred_string[27:29] + cred_string[30:32]
            even_parity_bit1 = '0' if calculate_even_parity(even_parity_data1) else '1'
            cred_string2 = f'{even_parity_bit1}{cred_string}'

            odd_parity_data1 = cred_string2[0:2] + cred_string2[3:5] + cred_string2[6:8] + cred_string2[9:11] + cred_string2[12:14] + cred_string2[15:17] + cred_string2[18:20] + cred_string2[21:23] + cred_string2[24:26] + cred_string2[27:29] + cred_string2[30:32] 
            odd_parity_bit1 = '0' if calculate_odd_parity(odd_parity_data1) else '1'
            cred_string3 = f'{even_parity_bit1}{cred_string}{odd_parity_bit1}'

            odd_parity_data2 = cred_string3
            odd_parity_bit2 = '0' if calculate_odd_parity(odd_parity_data2) else '1'

            # Output entire PACS string for encryption and conversion
            formatted_data = f'01{odd_parity_bit2}{even_parity_bit1}{cred_string}{odd_parity_bit1}'
            hex_format = hex(int(formatted_data, 2))[2:].zfill(16)
            card_numbers.append((hex_format, card_number))

        elif format_type == "h10304":
            # Checks if within range of format
            if facility_code < 1 or facility_code > 65535:
                print("Facility code must be between 1 and 65535.")
                break
            if card_number < 1 or card_number > 524287:
                print("Card number must be between 1 and 524287.")
                break

            # Convert values given to binary and stick together to generate credential string
            binary_facility_code = decimal_to_binary(facility_code, 16)
            binary_card_number = decimal_to_binary(card_number, 19)
            cred_string = f'{binary_facility_code}{binary_card_number}'

            # Calculate parity for format
            even_parity_data = cred_string[:18]
            odd_parity_data = cred_string[17:] 
            odd_parity_bit = '0' if calculate_odd_parity(odd_parity_data) else '1'
            even_parity_bit = '0' if calculate_even_parity(even_parity_data) else '1'

            # Output entire PACS string for encryption and conversion
            formatted_data = f'01{even_parity_bit}{cred_string}{odd_parity_bit}'
            hex_format = hex(int(formatted_data, 2))[2:].zfill(16)
            card_numbers.append((hex_format, card_number))

        elif format_type == "c1k48s":
            # Checks if within range of format
            if facility_code < 1 or facility_code > 4194303:
                print("Facility code must be between 1 and 4194303.")
                break
            if card_number < 1 or card_number > 8388607:
                print("Card number must be between 1 and 8388607.")
                break

            # Convert values given to binary and stick together to generate credential string
            binary_facility_code = decimal_to_binary(facility_code, 22)
            binary_card_number = decimal_to_binary(card_number, 23)
            cred_string = f'{binary_facility_code}{binary_card_number}'

            # Calculate parity for format
            even_parity_data1 = cred_string[1:3] + cred_string[4:6] + cred_string[7:9] + cred_string[10:12] + cred_string[13:15] + cred_string[16:18] + cred_string[19:21] + cred_string[22:24] + cred_string[25:27] + cred_string[28:30] + cred_string[31:33] + cred_string[34:36] + cred_string[37:39] + cred_string[40:42] + cred_string[43:45]
            even_parity_bit1 = '0' if calculate_even_parity(even_parity_data1) else '1'
            cred_string2 = f'{even_parity_bit1}{cred_string}'

            odd_parity_data1 = cred_string2[1:3] + cred_string2[4:6] + cred_string2[7:9] + cred_string2[10:12] + cred_string2[13:15] + cred_string2[16:18] + cred_string2[19:21] + cred_string2[22:24] + cred_string2[25:27] + cred_string2[28:30] + cred_string2[31:33] + cred_string2[34:36] + cred_string2[37:39] + cred_string2[40:42] + cred_string2[43:45]
            odd_parity_bit1 = '0' if calculate_odd_parity(odd_parity_data1) else '1'
            cred_string3 = f'{even_parity_bit1}{cred_string}{odd_parity_bit1}'

            odd_parity_data2 = cred_string3
            odd_parity_bit2 = '0' if calculate_odd_parity(odd_parity_data2) else '1'

            # Output entire PACS string for encryption and conversion
            formatted_data = f'01{odd_parity_bit2}{even_parity_bit1}{cred_string}{odd_parity_bit1}'
            hex_format = hex(int(formatted_data, 2))[2:].zfill(16)
            card_numbers.append((hex_format, card_number))

        if card_number + 1 > 65535:
            break
        card_number += 1
    
    return card_numbers


def encrypt_block7(hex_format):
    # Define encryption key
    key_hex = "B4212CCAB7ED210F7B93D45939C7DD36"
    key_bytes = binascii.unhexlify(key_hex)

    cipher = DES3.new(key_bytes, DES3.MODE_ECB)
    input_bytes = binascii.unhexlify(hex_format)
    encrypted_data = cipher.encrypt(input_bytes)
    encrypted_hex = binascii.hexlify(encrypted_data).decode('utf-8').upper()
    block7 = ' '.join(encrypted_hex[i:i+2] for i in range(0, len(encrypted_hex), 2))

    return block7

def main():
    # Print the pretty banner
    banner()
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        prog="PicoGen",
        description="Generate card numbers for Flipper PicoPass app."
    )
    parser.add_argument(
        "-cn", "--card_number", type=int, 
        help="Starting card number"
    )
    parser.add_argument(
        "-fc", "--facility_code", type=int, 
        help="Facility code"
    )
    parser.add_argument(
        "-f", "--format", type=str, 
        choices=["h10301", "h10306", "c1k35s", "h10304", "c1k48s"],
        help="Data format type"
    )
    parser.add_argument(
        "-num", "--count", type=int, 
        help="Number of card numbers to generate"
    )
    parser.add_argument(
        "-o", "--output", type=str, 
        default="output", 
        help="Custom output directory"
    )
    parser.add_argument(
        "--info", action="store_true", 
        help="Show this help message and exit"
    )
    args = parser.parse_args()

    # Show help message if --info is provided
    if args.info:
        print_help()
        return

    # Check if all required arguments are provided
    if not all([args.card_number, args.facility_code, args.count]):
        print_help()
        return

    # Check if format type is provided
    if not args.format:
        print("""
No format type given
Use one of the below:

h10301 - Standard 26bit
h10306 - HID Standard 34bit
c1k35s - HID 35bit Corporate 1000
h10304 - HID Farpointe 37bit with Site Code
c1k48s - HID 48bit Corporate 1000
        """)
        return

    card_number = args.card_number
    facility_code = args.facility_code
    count = args.count
    output_dir = args.output
    format_type = args.format

    print("Creating files")

    # Generate card numbers
    card_numbers = generate_card_numbers(card_number, facility_code, count, format_type)

    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for hex_format, original_card_number in card_numbers:
        # Encrypt the card number and get Block 7
        block7 = encrypt_block7(hex_format)

        # Define the filename with facility code and the original card number in decimal format
        file_name = f"FC{facility_code}CN{original_card_number}{format_type}.picopass"
        file_path = os.path.join(output_dir, file_name)

        # Flipper Picopass device file format
        picopass_content = f"""Filetype: Flipper Picopass device
Version: 1
Credential: 00 00 40 00 64 00 00 C8
# Picopass blocks
Block 0: 96 D1 57 10 FE FF 12 E0
Block 1: 12 FF FF FF 7F 1F FF 3C
Block 2: F6 FE FF FF FF FF FF FF
Block 3: 71 A4 E1 21 62 1A 16 37
Block 4: FF FF FF FF FF FF FF FF
Block 5: FF FF FF FF FF FF FF FF
Block 6: 03 03 03 03 00 03 E0 17
Block 7: {block7}
Block 8: 2A D4 C8 21 1F 99 68 71
Block 9: 2A D4 C8 21 1F 99 68 71
Block 10: FF FF FF FF FF FF FF FF
Block 11: FF FF FF FF FF FF FF FF
Block 12: FF FF FF FF FF FF FF FF
Block 13: FF FF FF FF FF FF FF FF
Block 14: FF FF FF FF FF FF FF FF
Block 15: FF FF FF FF FF FF FF FF
Block 16: FF FF FF FF FF FF FF FF
Block 17: FF FF FF FF FF FF FF FF

"""
        # Write the data to the file
        with open(file_path, "w") as f:
            f.write(picopass_content)

    print(f"Files saved to: ./{output_dir}")

if __name__ == "__main__":
    main()