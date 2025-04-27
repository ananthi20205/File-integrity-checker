import hashlib  # Used to create hash values (like digital fingerprints) of file contents
import os       # Used for interacting with the file system (folders/files)
import json     # Used to store and load hash data in a readable format (JSON)

def calculate_file_hash(filepath, algorithm='sha256'):
    """
    Calculate the hash of a file using the specified algorithm (default is SHA-256).
    This hash uniquely represents the contents of the file.
    """
    hash_func = hashlib.new(algorithm)  # Create a new hash object with the given algorithm
    try:
        with open(filepath, 'rb') as f:  # Open the file in binary mode
            while chunk := f.read(8192):  # Read the file in chunks (8192 bytes at a time)
                hash_func.update(chunk)   # Update the hash with the current chunk
        return hash_func.hexdigest()      # Return the final hash as a hexadecimal string
    except FileNotFoundError:
        print(f"Error: File not found - {filepath}")  # Handle missing files
        return None

def save_hashes(directory, output_file, algorithm='sha256'):
    """
    Save hash values of all files in a specified directory (and its subdirectories)
    into a JSON file. Useful for later comparison.
    """
    hashes = {}  # Dictionary to store file paths and their corresponding hash values
    for root, _, files in os.walk(directory):  # Walk through all subfolders and files
        for file in files:
            filepath = os.path.join(root, file)  # Get full file path
            file_hash = calculate_file_hash(filepath, algorithm)  # Calculate the file's hash
            if file_hash:
                hashes[filepath] = file_hash  # Save the hash in the dictionary
    with open(output_file, 'w') as f:
        json.dump(hashes, f, indent=4)  # Write the hashes to a JSON file
    print(f"Hashes saved to {output_file}")  # Confirm saving

def check_integrity(reference_file, algorithm='sha256'):
    """
    Compare current hash values of files with previously saved reference hashes.
    Detects if any files are changed, missing, or unchanged.
    """
    try:
        with open(reference_file, 'r') as f:
            reference_hashes = json.load(f)  # Load the reference hashes from JSON
    except FileNotFoundError:
        print(f"Error: Reference file not found - {reference_file}")
        return

    for filepath, old_hash in reference_hashes.items():  # Loop through each file and hash
        current_hash = calculate_file_hash(filepath, algorithm)  # Recalculate current hash
        if current_hash is None:
            print(f"Missing file: {filepath}")  # File is no longer present
        elif current_hash != old_hash:
            print(f"File changed: {filepath}")  # File was modified
        else:
            print(f"File unchanged: {filepath}")  # File is unchanged

if __name__ == "__main__":
    import argparse  # For building a command-line interface

    # Create the argument parser and define accepted arguments
    parser = argparse.ArgumentParser(description="File Integrity Checker")
    parser.add_argument("action", choices=["save", "check"], help="Action to perform: save hashes or check integrity")
    parser.add_argument("path", help="Path to directory (for save) or to reference file (for check)")
    parser.add_argument("--output", help="Output file to save hashes (only needed for 'save')")
    parser.add_argument("--algorithm", default="sha256", help="Hashing algorithm to use (default is sha256)")

    args = parser.parse_args()  # Parse the provided command-line arguments

    # Handle the "save" command
    if args.action == "save":
        if not args.output:
            print("Error: --output is required for 'save' action")  # Output file is needed
        else:
            save_hashes(args.path, args.output, args.algorithm)  # Save file hashes
    # Handle the "check" command
    elif args.action == "check":
        check_integrity(args.path, args.algorithm)  # Check integrity using reference hashes
