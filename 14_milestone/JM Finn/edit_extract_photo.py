import os
from PIL import Image
from io import BytesIO
import fitz


def extract_images_from_pdf(pdf_path, output_folder):
    target_resolution = (1240, 954)
    doc = fitz.open(pdf_path)
    
    for page_num in range(doc.page_count):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(BytesIO(image_bytes))
            
            if image.size == target_resolution:
                image_filename = os.path.join(output_folder, f"{os.path.basename(pdf_path)}_page{page_num + 1}_img{img_index + 1}.png")
                with open(image_filename, "wb") as image_file:
                    image_file.write(image_bytes)
                    
    doc.close()


def crop_image(img_path, output_folder1, output_folder2, original_dims=(1240, 954), target_dims1=(940, 820), target_dims2=(300, 954)):
    with Image.open(img_path) as img:
        if img.size == original_dims:
            # For the first crop: Lower left section
            left1 = 0
            upper1 = original_dims[1] - target_dims1[1]
            right1 = target_dims1[0]
            lower1 = original_dims[1]
            cropped_img1 = img.crop((left1, upper1, right1, lower1))
            
            # For the second crop: Rightmost section
            left2 = original_dims[0] - target_dims2[0]
            upper2 = 0
            right2 = original_dims[0]
            lower2 = target_dims2[1]
            cropped_img2 = img.crop((left2, upper2, right2, lower2))
            
            if not os.path.exists(output_folder1):
                os.makedirs(output_folder1)
            if not os.path.exists(output_folder2):
                os.makedirs(output_folder2)

            # Saving the first cropped image
            output_path1 = os.path.join(output_folder1, "crop1_" + os.path.basename(img_path))
            cropped_img1.save(output_path1)

            # Saving the second cropped image
            output_path2 = os.path.join(output_folder2, "crop2_" + os.path.basename(img_path))
            cropped_img2.save(output_path2)

        else:
            print(f"Skipped {img_path} as its dimensions are not {original_dims}")


def crop_all_images_in_folder(folder_path):
    output_folder1 = os.path.join(folder_path, "JM Finn Cropped assets")
    output_folder2 = os.path.join(folder_path, "JM Finn Cropped keys")
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(root, file)
                crop_image(full_path, output_folder1,output_folder2)


def crop_and_extract_images():
    input_folder = '14_milestone\JM Finn\JM Finn PDFs'
    image_output_folder = '14_milestone\JM Finn\JM Finn Images'
    cropped_output_folder = os.path.join(image_output_folder, "JM Finn Cropped Images")

    # Extract images from PDF
    if not os.path.exists(image_output_folder):
        os.makedirs(image_output_folder)
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            extract_images_from_pdf(pdf_path, image_output_folder)
    print("Image extraction completed!")

    # Crop extracted images
    crop_all_images_in_folder(image_output_folder)
    print("Cropping process complete!")


if __name__ == "__main__":
    crop_and_extract_images()
