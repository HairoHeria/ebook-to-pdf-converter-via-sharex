import os
import re
import cv2
import sys
import time
import img2pdf
import pyautogui
import numpy as np
import platform
import subprocess


def main():
    image_dir = get_dir()
    ebook_name = get_ebook_name()
    output_pdf = os.path.join(image_dir, f"{ebook_name}.pdf")

    start_time = time.time()  # Record the start time

    screenshot_ebook()
    convert_images_to_pdf(image_dir, output_pdf)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    if elapsed_time < 60:
        print(f"Time taken: {elapsed_time:.2f} seconds. ", end="")
    else:
        elapsed_time_minutes = elapsed_time / 60
        print(f"Time taken: {elapsed_time_minutes:.2f} minutes. ", end="")

    print(f"{ebook_name}.pdf has been saved to {image_dir}")
    open_pdf(output_pdf)


def get_dir():
    while True:

        # Ask for directory folder path from user
        image_dir = input(
            "Directory folder path where the screenshots are located: "
        ).strip()

        if valid_dir(image_dir):
            return image_dir
        else:
            print("Not a valid directory. Please try again")


def valid_dir(image_dir):
    # Assert whether the input is indeed directory folder path
    return re.search(
        r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$', image_dir
    )


def get_ebook_name():
    # Loop until file name is valid
    while True:

        # Ask user for the file name
        ebook_name = input("What will be the name of the new ebook?: ").strip()

        if valid_ebook_name(ebook_name):
            return ebook_name
        else:
            print(
                "File name cannot include windows reserved charaters. Please try again."
            )


def valid_ebook_name(ebook_name):
    # Assert that file name cannot include windows reserved characters: \ / : * ? " < > |
    return re.search(r'^[^\\/:*?"<>|]+$', ebook_name)


def screenshot_ebook():
    # Loop until page number is valid
    while True:

        # Get page number from user
        ebook_pages = int(input("How many pages does this ebook have?: "))

        if valid_ebook_pages(ebook_pages):

            # Confirm that the user is ready
            confirm_readiness()

            # Give a 3-seconds leeway for user to switch to ebook app
            time.sleep(3)

            # Start screenshotting all the ebook pages
            i = 0
            while i < ebook_pages:
                pyautogui.press("F3") # CHANGE to whatever hotkey you set in ShareX to capture last region
                pyautogui.press("space") # CHANGE to hotkey of next page in your ebook app 
                time.sleep(1)
                i += 1
            break

        else:
            print("Page number must be greater than zero")


def valid_ebook_pages(ebook_pages):
    # Assert the page number is greater than zero
    return ebook_pages > 0


def confirm_readiness():
    # Loop until user is ready
    while True:
        ready = (
            input(
                "The program will start to screenshot in 3 seconds once you are ready. Are you ready to switch to your ebook app? (Y/N): "
            )
            .strip()
            .upper()
        )
        if ready in ["Y", "N"]:
            if ready == "Y":
                return
            else:
                print(
                    "Please switch to your ebook app and be ready to start screenshotting."
                )
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")


def sharpen_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Set the kernel image quality
    kernel = np.array([[0, -0.2, 0], [-0.2, 1.8, -0.2], [0, -0.2, 0]])

    # Apply the kernel to the input image
    sharpened = cv2.filter2D(image, -1, kernel)

    return sharpened


def convert_images_to_pdf(image_dir, output_pdf):
    # Get all image files from the directory
    image_files = [
        f
        for f in os.listdir(image_dir)
        if f.endswith((".jpg", ".jpeg", ".png", ".bmp"))
    ]

    if not image_files:
        print("No image files found in the directory.")
        return

    # Get full path for each image file and their creation dates
    image_files_with_dates = [
        (os.path.join(image_dir, f), os.path.getctime(os.path.join(image_dir, f)))
        for f in image_files
    ]

    # Sort files by creation date
    sorted_image_files_with_dates = sorted(image_files_with_dates, key=lambda x: x[1])

    # Extract sorted file paths
    sorted_image_files = [f[0] for f in sorted_image_files_with_dates]

    enhanced_images = []

    for image_file in sorted_image_files:
        enhanced_image = sharpen_image(image_file)
        # Save the enhanced image temporarily
        temp_image_path = os.path.splitext(image_file)[0] + "_enhanced.png"
        cv2.imwrite(temp_image_path, enhanced_image)
        enhanced_images.append(temp_image_path)

    # Convert images to PDF
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(enhanced_images))

    # Cleanup temporary enhanced images
    for enhanced_image in enhanced_images:
        os.remove(enhanced_image)


def open_pdf(file_path):
    # Attempt to open the output pdf
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":
            subprocess.call(["open", file_path])
        else:
            subprocess.call(["xdg-open", file_path])
    except:
        sys.exit("Failed to open the output PDF file.")


if __name__ == "__main__":
    main()
