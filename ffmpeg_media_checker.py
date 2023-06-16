import subprocess


def validate_image(image_path):
    # Level 1: File extension and magic number check
    allowed_extensions = ["jpg", "jpeg", "png", "gif", "webp"]
    file_extension = image_path.lower().rsplit(".", 1)[-1]
    if file_extension not in allowed_extensions:
        print("Invalid file extension")
        return False

    try:
        # to check if the file can be decoded/ incl. checking magic number internally
        cmd = ["ffmpeg", "-v", "error", "-i", image_path, "-f", "null", "-"]
        subprocess.run(cmd, check=True, capture_output=True)
        first_check = True
    except subprocess.CalledProcessError as e:
        print(f"Invalid image file: {e.stderr.decode().strip()}")
        return False

    # Level 2: hflip/crop check (example)
    try:
        cmd = [
            "ffmpeg",
            "-i",
            image_path,
            "-vf",
            "hflip,crop=100:100",
            "-f",
            "null",
            "-",
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        second_check = True
    except subprocess.CalledProcessError:
        print("Image failed hflip/crop check")
        return False

    # Level 3: TBD

    # If all checks pass, the image is considered valid
    if first_check and second_check:
        return True


def validate_video(video_path):
    # Level 1: File extension and magic number check
    allowed_extensions = ["mp4", "3gp", "mov", "wmv", "avi", "flv"]
    file_extension = video_path.lower().rsplit(".", 1)[-1]
    if file_extension not in allowed_extensions:
        print("Invalid file extension.")
        return False

    try:
        # Check if the video can be decoded/incl. magic number check
        cmd = ["ffprobe", "-v", "error", "-show_format", "-show_streams", video_path]
        subprocess.run(cmd, check=True, capture_output=True)
        first_check = True
    except subprocess.CalledProcessError as e:
        print(f"Invalid video file: {e.stderr.decode().strip()}")
        return False

    # Level 2: Video manipulation check (example: flip/cut/pause)
    try:
        cmd = ["ffmpeg", "-i", video_path, "-vf", "hflip", "-f", "null", "-"]
        subprocess.run(cmd, check=True, capture_output=True)
        second_check = True
    except subprocess.CalledProcessError:
        print("Video failed manipulation check")
        return False

    # Level 3: TBD

    # If all checks pass, the video is considered valid
    if first_check and second_check:
        return True


# Video Check
# video_path = "test_samples/output.MOV"
video_path = "test_samples/vanilla2.3gp"
if validate_video(video_path):
    print("Video is valid")

# Image Check
# image_path = "test_samples/ezgif-2-4222e09cff-orijpg.gif"
# image_path = "test_samples/corrupted_1mb_oriwebp.webp"
image_path = "test_samples/1500kb.webp"
if validate_image(image_path):
    print("Image is valid")
