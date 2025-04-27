import streamlit as st  # Streamlit is used to create the web-based dashboard.
import hashlib  # Used to generate hash values for files.
import os  # Provides functions to interact with the file system.
import json  # Used to store and retrieve hash data in JSON format.
import pandas as pd  # Used to create and display data in tabular format.
from datetime import datetime  # Used to add timestamps to hash data.

# 🔵 Core Functions for File Integrity Checking

def calculate_file_hash(filepath, algorithm='sha256'):
    """
    Calculate the hash of a file using the specified algorithm.
    - `filepath`: Path to the file to hash.
    - `algorithm`: Hashing algorithm to use (default is SHA-256).
    """
    hash_func = hashlib.new(algorithm)  # Create a new hash object with the specified algorithm.
    try:
        with open(filepath, 'rb') as f:  # Open the file in binary mode.
            while chunk := f.read(8192):  # Read the file in chunks of 8192 bytes.
                hash_func.update(chunk)  # Update the hash with the current chunk.
        return hash_func.hexdigest()  # Return the final hash as a hexadecimal string.
    except FileNotFoundError:
        return None  # Return None if the file is not found.

def save_hashes(directory, output_file=None, algorithm='sha256'):
    """
    Save hash values of all files in a directory to a JSON file.
    - `directory`: Directory to scan for files.
    - `output_file`: File to save the hash data (optional).
    - `algorithm`: Hashing algorithm to use (default is SHA-256).
    """
    hashes = {}  # Dictionary to store file paths and their hash values.
    for root, _, files in os.walk(directory):  # Walk through all subdirectories and files.
        for file in files:
            filepath = os.path.join(root, file)  # Get the full path of the file.
            file_hash = calculate_file_hash(filepath, algorithm)  # Calculate the file's hash.
            if file_hash:
                hashes[filepath] = {"hash": file_hash, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                # Store the hash and the current timestamp.
    if output_file:
        with open(output_file, 'w') as f:  # Save the hash data to a JSON file.
            json.dump(hashes, f, indent=4)
    return hashes  # Return the hash data.

def check_integrity(reference_file, directory, algorithm='sha256'):
    """
    Compare current hash values of files with previously saved reference hashes.
    - `reference_file`: JSON file containing the reference hashes.
    - `directory`: Directory to scan for files.
    - `algorithm`: Hashing algorithm to use (default is SHA-256).
    """
    try:
        with open(reference_file, 'r') as f:  # Open the reference file.
            reference_hashes = json.load(f)  # Load the reference hashes from JSON.
    except FileNotFoundError:
        st.error("Reference file not found.")  # Display an error if the reference file is missing.
        return None

    current_hashes = save_hashes(directory, None, algorithm)  # Get the current hashes of files.
    integrity_results = []  # List to store the results of the integrity check.
    all_files = set(reference_hashes.keys()).union(set(current_hashes.keys()))  # Combine all file paths.

    for filepath in all_files:
        ref_data = reference_hashes.get(filepath)  # Get the reference hash data.
        curr_data = current_hashes.get(filepath)  # Get the current hash data.

        if ref_data and not curr_data:
            # File was deleted.
            integrity_results.append({"File": filepath, "Status": "❌ Deleted", "Timestamp": ref_data["timestamp"]})
        elif not ref_data and curr_data:
            # File was added.
            integrity_results.append({"File": filepath, "Status": "✅ Added", "Timestamp": curr_data["timestamp"]})
        elif ref_data and curr_data:
            if ref_data["hash"] == curr_data["hash"]:
                # File is unchanged.
                integrity_results.append({"File": filepath, "Status": "✔️ Unchanged", "Timestamp": curr_data["timestamp"]})
            else:
                # File was modified.
                integrity_results.append({"File": filepath, "Status": "⚠️ Modified", "Timestamp": curr_data["timestamp"]})

    return pd.DataFrame(integrity_results)  # Return the results as a DataFrame.

# 🚀 Streamlit Layout

st.title("File Integrity Checker")  # Display the title of the dashboard.
st.subheader("Monitor changes in your files")  # Display the subtitle.

directory = "my_files"  # Fixed directory for simplicity.
output_file = "hashes.json"  # Fixed output file for simplicity.

# Layout for buttons
col1, col2 = st.columns(2)  # Create two columns for buttons.

with col1:
    if st.button("Save Hashes", key="save"):  # Button to save hashes.
        with st.spinner("Saving hashes..."):  # Display a spinner while saving hashes.
            hashes = save_hashes(directory, output_file)  # Save the hashes.
            st.success(f"Hashes saved successfully to {output_file}")  # Display success message.
            st.write(f"Total files hashed: {len(hashes)}")  # Display the total number of files hashed.

with col2:
    if st.button("Check Integrity", key="check"):  # Button to check integrity.
        with st.spinner("Checking file integrity..."):  # Display a spinner while checking integrity.
            if os.path.exists(output_file):  # Check if the reference file exists.
                integrity_df = check_integrity(output_file, directory, "sha256")  # Perform the integrity check.
                if integrity_df is not None and not integrity_df.empty:
                    st.success("Integrity check completed.")  # Display success message.
                    st.dataframe(integrity_df)  # Display the results in a table.
                elif integrity_df is not None and integrity_df.empty:
                    st.warning("No changes detected.")  # Display a warning if no changes are detected.
            else:
                st.error("Reference file not found. Please save hashes first.")  # Display an error if the reference file is missing.
