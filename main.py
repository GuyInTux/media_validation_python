import boto3
import os

s3 = boto3.client("s3")

# Magic numbers referenced from:
# https://www.garykessler.net/library/file_sigs.html
# https://asecuritysite.com/forensics/magic
# https://en.wikipedia.org/wiki/List_of_file_signatures

FILE_MAGIC_NUMBERS = {
    ".png": [b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a", b"\x89\x50\x4e\x47"],
    ".jpg": [
        b"\xff\xd8",
        b"\xff\xd8\xff\xe0",
        b"\xff\xd8\xff\xdb",
        b"\xff\xd8\xff\xee",
        b"\xff\xd8\xff\xe1",
        b"\xff\xd8\xff\xe2",
        b"\xff\xd8\xff\xe8",
    ],
    ".gif": [b"\x47\x49\x46\x38\x37\x61", b"\x47\x49\x46\x38\x39\x61"],
    ".mp4": [
        b"\x66\x74\x79\x70\x69\x73\x6f\x6d",
        b"\x66\x74\x79\x70\x4d\x53\x4e\x56",
        b"\x00\x00\x00\x18\x66\x74\x79\x70\x6d\x70\x34\x32",
        b"\x66\x74\x79\x70",
    ],
    ".3gp": b"\x66\x74\x79\x70\x33\x67\x70",
    ".mov": [
        b"\x00",
        b"\x6d\x6f\x6f\x76",
        b"\x66\x72\x65\x65",
        b"\x6d\x64\x61\x74",
        b"\x77\x69\x64\x65",
        b"\x66\x74\x79\x70\x71\x74\x20\x20",
        b"\x70\x6e\x6f\x74",
        b"\x73\x6b\x69\x70",
    ],
    ".wmv": b"\x30\x26\xb2\x75\x8e\x66\xcf\x11\xa6\xd9\x00\xaa\x00\x62\xce\x6c",
    ".avi": [b"\x52\x49\x46\x46", b"\x41\x56\x49\x20\x4c\x49\x53\x54"],
    ".flv": [b"\x46\x4c\x56\x01", b"\x66\x74\x70\x70\x4d\x53\x4e\x56"],
    ".pdf": b"\x25\x50\x44\x46",
}


def validate_file(response, file_type):
    try:
        bytes_to_read = 10
        while True:
            if bytes_to_read > 26214400:
                print("Magic number not found after 25mb read.")
                return False
            content_read = response["Body"].read(bytes_to_read)

            if any(
                magic_number in content_read
                for magic_number in FILE_MAGIC_NUMBERS.get(file_type, [])
            ):
                return True
            bytes_to_read *= (
                10  # Multiplies in factors of 10 until magic number found to limit cost
            )

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False

    return False


def lambda_handler(event, context):
    bucket_name = event["bucket_key"]
    input_folder = event["folder_key"]
    input_file_key = event["input_file_key"]
    file_extension = os.path.splitext(input_file_key.lower())[-1]
    if file_extension == ".jpeg":
        file_extension = ".jpg"

    if not input_folder == "":
        object_key = f"{input_folder}/{input_file_key}"
        get_object_response = s3.get_object(Bucket=bucket_name, Key=object_key)
    else:
        get_object_response = s3.get_object(Bucket=bucket_name, Key=input_file_key)

    if validate_file(response=get_object_response, file_type=file_extension):
        print(f"File is valid.")
    else:
        print(f"File is invalid.")
