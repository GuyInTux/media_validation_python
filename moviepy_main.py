from moviepy.editor import VideoFileClip

# import imghdr
from PIL import Image


def validate_video(file_path):
    try:
        clip = VideoFileClip(file_path)
        return True
    except Exception as e:
        print(f"Invalid video file. Error: {str(e)}")
        return False


# Uses Pillow and PIL's Image to validate image file, read: https://pillow.readthedocs.io/en/stable/installation.html
def validate_image(file_path):
    #  First-check verifies file type
    try:
        im = Image.open(file_path)
        im.verify()
        im.close()
        results = True
    except Exception as e:
        print(f"An error occurred while verifying.\n({str(e)})")
        return False

    #  Performs second-check by flipping image
    if results:
        try:
            im = Image.open(file_path)
            im.transpose(Image.FLIP_LEFT_RIGHT)
            im.close()
            return True
        except Exception as e:
            print(f"File corrupted. Error: {str(e)}")
            return False


# Same as above, just better readability
# def validate_image(file_path):
#     #  First-check verifies file type
#     try:
#         im = Image.open(file_path)
#         im.verify()
#         im.close()
#         results = True

#         #  Performs second-check by flipping image
#         if results:
#             try:
#                 im = Image.open(file_path)
#                 im.transpose(Image.FLIP_LEFT_RIGHT)
#                 im.close()
#                 return True
#             except Exception as e:
#                 print(f"File corrupted. Error: {str(e)}")
#                 return False

#     except Exception as e:
#         print(f"An error occurred while verifying.\n({str(e)})")
#         return False


# Uses imghdr to validate image file (Prone to spoofing!)
# def validate_image(file_path):
#     try:
#         if image_type := imghdr.what(file_path):
#             return True
#     except Exception as e:
#         print(f"Invalid image file. Error: {str(e)}")
#         return False

# video_file_path = "output.MOV"
video_file_path = "output.MOV"
# image_file_path = "sample_valid_img.webp"
image_file_path = "sample_valid_img.webp"

if validate_video(file_path=video_file_path):
    print(f"Video file {video_file_path} is valid.")

if validate_image(file_path=image_file_path):
    print(f"Image file {image_file_path} is valid.")
