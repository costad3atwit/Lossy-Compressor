import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image


def promptForFile():
    #create root window
    root = tk.Tk()
    root.withdraw()

    ## Open the file dialog
    file_path = filedialog.askopenfilename()

    # Print the selected file path
    if file_path:
        print("Selected file:", file_path)


def compressImage(img, percentage_compression):
    # Open the image file
    img = Image.open("reference.jpg")

    # Convert the image to a NumPy array
    img_array = np.array(img)

    R = img_array[:, :, 0]  # Red channel
    G = img_array[:, :, 1]  # Green channel
    B = img_array[:, :, 2]  # Blue channel

    U_r, S_r, Vt_r = np.linalg.svd(R, full_matrices=False)
    U_g, S_g, Vt_g = np.linalg.svd(G, full_matrices=False)
    U_b, S_b, Vt_b = np.linalg.svd(B, full_matrices=False)

    k = 50  # The number of singular values to keep

    # Keep only the top 'k' singular values for each channel
    S_r_k = np.diag(S_r[:k])
    S_g_k = np.diag(S_g[:k])
    S_b_k = np.diag(S_b[:k])

    U_r_k = U_r[:, :k]
    U_g_k = U_g[:, :k]
    U_b_k = U_b[:, :k]

    Vt_r_k = Vt_r[:k, :]
    Vt_g_k = Vt_g[:k, :]
    Vt_b_k = Vt_b[:k, :]

    #Reconstruct Image
    R_compressed = np.dot(U_r_k, np.dot(S_r_k, Vt_r_k))
    G_compressed = np.dot(U_g_k, np.dot(S_g_k, Vt_g_k))
    B_compressed = np.dot(U_b_k, np.dot(S_b_k, Vt_b_k))

    img_compressed = np.stack([R_compressed, G_compressed, B_compressed], axis=-1)

    # Clip the values to stay in the range [0, 255]
    img_compressed = np.clip(img_compressed, 0, 255).astype(np.uint8)

    # Convert the compressed array back to an image
    img_compressed_pil = Image.fromarray(img_compressed)

    # Save or show the compressed image
    img_compressed_pil.save("compressed_image.jpg")
    img = Image.open("compressed_image.jpg")
    img_compressed_pil.show()