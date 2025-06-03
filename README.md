FILE INTEGRITY CHECKER

COMPANY:    CODTECH IT SOLUTIONS

NAME:    M.catherine presenna

INTERN ID:    CT06DF2555

DOMAIN:    CYBER SECURITY AND ETHICAL HACKING

DURATION:    4 WEEKS

MENTOR:    NEELA SANTOSH

OUTPUT:    ![Image](https://github.com/user-attachments/assets/af2fd8db-ae41-4622-ba8c-a007e58849b2)

Task 1: File Integrity Checker – DESCRIPTION

In today’s digital world, ensuring that files remain unchanged and unaltered is essential for maintaining system security and protecting sensitive data. 
File integrity checking is an important method used in cybersecurity to verify whether a file has been modified without authorization. 
This task involves building a File Integrity Checker tool using the Python programming language. 
The main goal of this tool is to monitor changes in files by calculating and comparing their hash values. 
A hash value is a unique fixed-size string generated from the contents of a file using a cryptographic hash function. 
If any small change is made to the file, its hash value will change completely, which makes hash comparison a reliable method to detect file modifications.

This tool will consist of two major steps. 
The first step is to calculate the hash values of selected files and store those values in a reference file. 
This reference file will act as a baseline to verify file integrity in the future. 
The second step is to run the tool again later and recalculate the current hash values of the same files. 
The tool then compares the newly calculated hash values with the previously stored ones. 
If the values match, the file has not been altered. 
If there is a mismatch, it indicates that the file has been modified.

The implementation of this tool will be done in Python using standard libraries. 
The hashlib library will be used to generate cryptographic hash values. 
It supports multiple algorithms such as MD5, SHA-1, and SHA-256. 
The os library will be used to navigate directories and access files. 
The json or csv library can be used to store the original hash values in a structured format. 
The tool will prompt the user to enter the file or folder path to monitor. 
It will then calculate the hash of each file in the specified location and save the hash values with file names for later comparison.

This tool is useful in many real-world applications. 
System administrators can use it to monitor critical system files to detect tampering. 
Developers can use it to make sure that their application files remain unchanged. 
Organizations can use it to verify the integrity of sensitive documents and prevent unauthorized access or corruption. 
It can also be used as part of a larger security system to alert users when important files are changed.

The final deliverable for this task is a Python script that performs the file integrity checking process. 
The script should allow the user to input the files or directories to monitor, calculate and store the hash values, and later compare the hashes to detect any changes. 
The output should clearly indicate which files are unchanged and which ones have been modified. 
The tool can be enhanced further by adding a logging system, email alerts, or GUI support, but for this task, a simple command-line script is sufficient.

In conclusion, this File Integrity Checker is a simple but powerful tool that helps detect file modifications using hash value comparison. 
It improves data security and system reliability by ensuring that important files remain unchanged over time.
