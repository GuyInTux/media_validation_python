# NOTE: This function removes ALL Metadata and Tags of input video files
# To remove ONLY GPS metadata, please use 'ffmpeg-test' Lambda function attached below:
# https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ffmpeg-test?tab=code

import boto3
import os
import subprocess

s3 = boto3.client("s3")


def lambda_handler(event, context):
    bucket_name = "s3-dev-g2g-user"
    input_folder = "sample_media"
    input_file_key = event["input_file_key"]

    input_file_path = f"/tmp/{input_file_key}"
    input_file_extension = os.path.splitext(input_file_key)[1]
    s3.download_file(bucket_name, f"{input_folder}/{input_file_key}", input_file_path)

    accepted_formats = [".mp4", ".mov", ".avi", ".3gp", ".wmv", ".flv"]
    accepted_image_formats = [".jpg", ".jpeg", ".png", ".gif", ".webp"]

    is_image = False
    is_video = False
    if input_file_extension.lower() in accepted_image_formats:
        is_image = True
    elif input_file_extension.lower() in accepted_formats:
        is_video = True
    else:
        print(
            f"Input file format not supported. Please upload a video file with one of the following extensions: {', '.join(accepted_formats)}"
        )
        return  # abort function

    if is_image:
        try:
            # to check if the file can be decoded/ incl. checking magic number internally
            cmd = [
                "/opt/ffmpeg",
                "-v",
                "error",
                "-i",
                input_file_path,
                "-f",
                "null",
                "-",
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            first_check = True
            print("Image is valid")
        except subprocess.CalledProcessError as e:
            print(f"Invalid image file: {e.stderr.decode().strip()}")
            return False

    if is_video:
        try:
            cmd = [
                "/opt/ffmpeg",
                "-v",
                "error",
                "-i",
                input_file_path,
                "-f",
                "null",
                "-",
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            first_check = True
            print("Video is valid")
        except subprocess.CalledProcessError as e:
            print(f"Invalid video file: {e.stderr.decode().strip()}")
            return False


# # NOTE: This function removes ALL Metadata and Tags of input video files
# # To remove ONLY GPS metadata, please use 'ffmpeg-test' Lambda function attached below:
# # https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ffmpeg-test?tab=code

# import boto3
# import os
# import subprocess

# s3 = boto3.client('s3')

# def lambda_handler(event, context):
#     bucket_name = 's3-dev-g2g-public-asset'
#     input_folder = 'test_input'
#     # input_file_key = 'gps_test vid.3gp'
#     input_file_key = 'test_video.mov'

#     input_file_path = f'/tmp/{input_file_key}'
#     input_file_extension = os.path.splitext(input_file_key)[1]
#     output_file_path = f'/tmp/after{input_file_extension}'
#     s3.download_file(bucket_name, f'{input_folder}/{input_file_key}', input_file_path)

#     accepted_formats = ['.mp4', '.mov', '.avi', '.3gp', '.wmv', '.flv']

#     # List of 25MB(Small) ,250MB (Large) and online downloaded test input vids
#     # small_vid_list = ['test_video.mov', 'vanilla2.3gp', 'vanilla2.mp4', 'vanilla2.MOV', 'formatted_vanilla2.avi', 'formatted_vanilla2.flv', 'formatted_vanilla2.wmv']
#     # large_vid_list =  ['formatted_test vid.mp4', 'formatted_test vid.3gp', 'formatted_test vid.mov', 'formatted_test vid.wmv', 'formatted_test vid.flv', 'formatted_test vid.avi']
#     # online_vid_list = ['formatted_online_test_video.mp4']

#     # Use whichever list for intended input, they are all in the test_input S3 folder
#     # input_file_key = online_vid_list[0]

#     if input_file_extension.lower() not in accepted_formats:
#         print(f"Input file format not supported. Please upload a video file with one of the following extensions: {', '.join(accepted_formats)}")
#         return #abort function

#     # if input_file_key in online_vid_list:
#     #     output_file_key = f'test_output/edited_online_output_video{input_file_extension}'
#     # elif input_file_key in large_vid_list:
#     #     output_file_key = f'test_output/output_video_250mb{input_file_extension}'
#     # elif:
#     #     output_file_key = f'test_output/output_video_25mb{input_file_extension}'
#     # else:
#     #     print("Removal Process failed.")

#     # Tweak the cmd here for desired output properties
#     # cmd = ["/opt/ffmpeg", "-i", input_file_path, "-map_metadata", "-1", "-c", "copy", output_file_path]
#     # cmd = ["/opt/ffmpeg", "-i", input_file_path, "-c", "copy", "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact", "-map_metadata", "-1", output_file_path]
#     # cmd = ["/opt/ffmpeg", "-i", input_file_path, "-c", "copy", "-bitexact", "-map_metadata", "-1", "-vbsf", "filter_units=remove_types=6", output_file_path]

#     cmd = ["/opt/ffmpeg", "-i", input_file_path, "-metadata", "title=", "-c:v", "copy", "-c:a", "copy", output_file_path]

#     subprocess.run(cmd)

#     output_file_key = f'test_output/everything_removed_v2{input_file_extension}'

#     s3.upload_file(output_file_path, bucket_name, output_file_key)

#     print(f"GPS Metadata for {input_file_key} removed and recreated successfully!")


# LEGACY (DEPRECATED)
# from moviepy.editor import VideoFileClip

# # import imghdr
# from PIL import Image


# def validate_video(file_path):
#     try:
#         clip = VideoFileClip(file_path)
#         return True
#     except Exception as e:
#         print(f"Invalid video file. Error: {str(e)}")
#         return False


# # Uses Pillow and PIL's Image to validate image file, read: https://pillow.readthedocs.io/en/stable/installation.html
# def validate_image(file_path):
#     #  First-check verifies file type
#     try:
#         im = Image.open(file_path)
#         im.verify()
#         im.close()
#         results = True
#     except Exception as e:
#         print(f"An error occurred while verifying.\n({str(e)})")
#         return False

#     #  Performs second-check by flipping image
#     if results:
#         try:
#             im = Image.open(file_path)
#             im.transpose(Image.FLIP_LEFT_RIGHT)
#             im.close()
#             return True
#         except Exception as e:
#             print(f"File corrupted. Error: {str(e)}")
#             return False


# # Same as above, just better readability
# # def validate_image(file_path):
# #     #  First-check verifies file type
# #     try:
# #         im = Image.open(file_path)
# #         im.verify()
# #         im.close()
# #         results = True

# #         #  Performs second-check by flipping image
# #         if results:
# #             try:
# #                 im = Image.open(file_path)
# #                 im.transpose(Image.FLIP_LEFT_RIGHT)
# #                 im.close()
# #                 return True
# #             except Exception as e:
# #                 print(f"File corrupted. Error: {str(e)}")
# #                 return False

# #     except Exception as e:
# #         print(f"An error occurred while verifying.\n({str(e)})")
# #         return False


# # Uses imghdr to validate image file (Prone to spoofing!)
# # def validate_image(file_path):
# #     try:
# #         if image_type := imghdr.what(file_path):
# #             return True
# #     except Exception as e:
# #         print(f"Invalid image file. Error: {str(e)}")
# #         return False

# video_file_path = "test_samples/output.MOV"
# image_file_path = "test_samples/corrupted_1mb_oriwebp.webp"

# if validate_video(file_path=video_file_path):
#     print(f"Video file {video_file_path} is valid.")

# if validate_image(file_path=image_file_path):
#     print(f"Image file {image_file_path} is valid.")

# # Test Results:
# # test_samples/output.mov is valid. (moviepy)
# # test_samples/1mb-png-non-pdf.pdf considered valid, despite being manually renamed to a .pdf file. (PIL)
# # test_samples/1500kb.webp is valid. (PIL)
# # test_samples/corrupted_1mb_oriwebp.webp considered invalid. Error: (cannot identify image file 'test_samples/corrupted_1mb_oriwebp.webp') (PIL)
# # test_samples/sample_valid_img.webp is valid. (PIL)
