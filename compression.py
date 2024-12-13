import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


#returns file path, path to save to
def promptForFile(overwriteTrue):
    #create root window
    root = tk.Tk()
    root.withdraw()

    #Open the file dialog
    file_path = filedialog.askopenfilename(filetypes = [('PDF Files', '*.png'),('JPG Files', '*.jpg')])
    
    if not overwriteTrue:
        # If not overwriting, allow the user to choose where to save
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[('JPEG Files', '*.jpg'), ('PNG Files', '*.png')])
    

    # Print the selected file path
    if file_path:
        if save_path:
            return {'File Path': file_path, 'Save Path': save_path}
        else:
            return {'File Path': file_path, 'Save Path': file_path}
def promptForOverwrite():
    root = tk.Tk()
    root.title("Select Overwrite Option")
    # Create a variable to store the selected value
    selected_value = tk.BooleanVar(value=False)

    radio_button1 = tk.Radiobutton(root, text="Overwrite Original", variable=selected_value, value=True)
    radio_button1.pack()

    radio_button2 = tk.Radiobutton(root, text="Save As New File", variable=selected_value, value=False)
    radio_button2.pack()
    def on_submit():
        print("On submit called")
        root.quit()
        root.destroy()
    
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack()

    # Start the Tkinter event loop
    root.mainloop()

    # Return the value of the selected option (True for overwrite, False for save as new)
    return selected_value.get()

def show_image_from_path(image_path):
    # Open the image from the file path
    image = Image.open(image_path)

    # Create a new window to display the image
    image_window = tk.Toplevel(width=250,height=250)
    image_window.title("Image")

    # Convert the image to a format Tkinter can use
    image_tk = ImageTk.PhotoImage(image)

    # Create a label to display the image
    label = tk.Label(image_window, image=image_tk)
    label.image = image_tk  # Keep a reference to avoid garbage collection
    label.pack()

    # Start the Tkinter event loop for the new window
    image_window.mainloop()

def main():

    overwriteTrue = promptForOverwrite()
    data = promptForFile(overwriteTrue)
    filePath = data['File Path']
    savePath = data['Save Path']

    # Open the image file
    img = Image.open(filePath)

    # Convert the image to a NumPy array
    img_array = np.array(img)

    R = img_array[:, :, 0]  # Red channel
    G = img_array[:, :, 1]  # Green channel
    B = img_array[:, :, 2]  # Blue channel

    U_r, S_r, Vt_r = np.linalg.svd(R, full_matrices=False)
    U_g, S_g, Vt_g = np.linalg.svd(G, full_matrices=False)
    U_b, S_b, Vt_b = np.linalg.svd(B, full_matrices=False)


    # CHANGE K TO A VARIABLE TO ACCEPT USER INPUT FOR COMPRESSION RATIO
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
    if(overwriteTrue):
        img_compressed_pil.save(filePath)
    else:
        img_compressed_pil.save(savePath)
    
    # Create the Tkinter window for the original image
    root = tk.Tk()

    # Display the original image from the file path
    show_image_from_path(filePath)
    
    # Display the compressed image from the file path
    root.after(1000, show_image_from_path, savePath)  # Delay to show the compressed image after a second

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
