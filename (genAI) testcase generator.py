import os
import zipfile

#The following code is AI generated

ROOT = "dummy_data"

print("Building mock hospital filesystem...")
os.makedirs(ROOT, exist_ok=True)

# --- TEST CASE 1: OCT Zip Bomb & Collision ---
# Tests if you can unzip a file, find 016.png, and handle duplicate 016.png names
oct_path_1 = os.path.join(ROOT, "OCT", "patient_A")
oct_path_2 = os.path.join(ROOT, "OCT", "patient_B")
os.makedirs(oct_path_1, exist_ok=True)
os.makedirs(oct_path_2, exist_ok=True)

# Create a temporary 016.png, zip it into patient_A, then delete the loose file
temp_img = "016.png"
with open(temp_img, "w") as f: f.write("fake image data")
with zipfile.ZipFile(os.path.join(oct_path_1, "scan_data.zip"), 'w') as zf:
    zf.write(temp_img)
os.remove(temp_img)

# Put a loose 016.png in patient_B to guarantee a filename collision
with open(os.path.join(oct_path_2, "016.png"), "w") as f: f.write("fake image data")


# --- TEST CASE 2: FUNDUS Logic Trap ---
# Tests the rule: If XML exists AND an image starts with '0', only keep the other images.
fundus_path_1 = os.path.join(ROOT, "FUNDUS", "patient_C")
os.makedirs(fundus_path_1, exist_ok=True)

with open(os.path.join(fundus_path_1, "metadata.xml"), "w") as f: f.write("<data></data>")
with open(os.path.join(fundus_path_1, "0_bad_retina.jpg"), "w") as f: f.write("fake")
with open(os.path.join(fundus_path_1, "keep_this_retina.jpg"), "w") as f: f.write("fake")


# --- TEST CASE 3: Standard FUNDUS ---
# Tests standard copying when the complex rules don't apply
fundus_path_2 = os.path.join(ROOT, "FUNDUS", "patient_D")
os.makedirs(fundus_path_2, exist_ok=True)
with open(os.path.join(fundus_path_2, "normal_eye.png"), "w") as f: f.write("fake")


print(f"Success! A fake dataset has been generated in the '{ROOT}' folder.")