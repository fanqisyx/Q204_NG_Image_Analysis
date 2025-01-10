import os
from ui import get_user_input
from data_analysis import count_images_by_folder
from pdf_generator import create_pdf

def main():
    input_directory, output_directory, images_per_folder = get_user_input()
    if not input_directory or not output_directory:
        return

    folder_image_count = count_images_by_folder(input_directory)
    output_pdf = os.path.join(output_directory, "output.pdf")
    create_pdf(input_directory, output_pdf, folder_image_count, images_per_folder)

if __name__ == "__main__":
    main()
