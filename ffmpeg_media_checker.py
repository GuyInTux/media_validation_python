#  This module uses ffmpeg as a tool to validate media files. There are multiple layers of validation to fend against primarily spoofing and accidental corruption.
import ffmpeg


def validate_file(file_path):
    # Level 1: Check file extension, magic number
    try:
        probe = ffmpeg.probe(file_path)
    except ffmpeg.Error as e:
        print(f"Level 1 validation failed with error: {e.stderr.decode()}")
        return False

    # Level 2: Perform operation unique to intended file type
    try:
        (
            ffmpeg.input(file_path)
            .output("null:", vf="hflip", f="null")  # discards output, test only
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(f"Level 2 validation failed with error: {e.stderr.decode()}")
        return False

    # Level 3: Additioanl checks for image files (if necessary)
    # if probe["streams"][0]["codec_type"] == "video":
    return True


filepath = "test_samples/corrupted_1mb_oriwebp.webp"
final_slash_i = filepath.rfind("/")

if validate_file(filepath):
    print(f"REPORT\n{filepath[final_slash_i+1:]} is a valid file.")
