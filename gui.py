from pathlib import Path
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageEnhance
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import numpy as np
import cv2
import sys

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) /'assets' /'frame0'
    return Path(__file__).parent /'assets' /'frame0'

ASSETS_PATH = get_base_path()

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

imageBefore = None # menyimpan image saat ini
imageAfter = None # menyimpan image yang akan di save

def openFile():
    filepath = filedialog.askopenfilename(filetypes=(("Image files", "*.jpg *.png *.jpeg"),("All files", "*.*")))
    print(filepath)
    if filepath: #jika ada memasukan gambar
        img = Image.open(filepath)  #membuka gambar
        img = img.resize((275,242)) # rezise ukuran 
        saveImageOriginal(img) #save image saat ini
        saveImageLocal(img) #save image yang akan dioperasikan
        changeImageBox1(img) #ganti image di canvas
        namaFile = Path(filepath).name #ambil nama file
        canvas.itemconfig(namaGambar, text=namaFile)# update nama file

def saveFileImage():
    file = filedialog.asksaveasfile(mode='wb', defaultextension=".png", filetypes=(("PNG file", "*.png"),("All Files", "*.*") ))
    if file:
        imageAfter.save(file, format='PNG')

def saveImageOriginal(imageSekarang):
    global imageBefore
    imageBefore = imageSekarang

def saveImageLocal(imageSekarang):
    global imageAfter
    imageAfter = imageSekarang

def changeImageBox1(myImage):
    curentImage = ImageTk.PhotoImage(myImage) #simpan hasil image saat ini
    canvas.itemconfig(image_6, image=curentImage)  # Ganti gambar di canvas
    canvas.image_6 = curentImage

def changeImageBox2(myImage):
    curentImage = ImageTk.PhotoImage(myImage) #simpan hasil image saat ini
    canvas.itemconfig(image_8, image=curentImage)  # Ganti gambar di canvas
    canvas.image_8 = curentImage

def imgToGrayscale():
    curentImage = ImageOps.grayscale(imageAfter) # melakukan grayscale
    # update gambar
    saveImageLocal(curentImage)
    changeImageBox2(curentImage)
    # update penjelasan
    canvas.itemconfig(detail_menu, text="Grayscale")
    canvas.itemconfig(detail_penjelasan, text="mengubah gambar menjadi keabu-abuan")

def imgTresholding():
    imgToGrayscale()
    threshold = 127 #nilai treshold
    curentImage = imageAfter.point(lambda x: 255 if x > threshold else 0 ) # jika melebihi treshold maka warna putih
    saveImageLocal(curentImage)
    changeImageBox2(curentImage)
    # update penjelasan
    canvas.itemconfig(detail_menu, text="Tresholding")
    canvas.itemconfig(detail_penjelasan, text="mengubah gambar menjadi hitam atau putih tergantung treshold")

def imgBrightnessAdjustment():
    imageLokal = imageAfter.copy() # simpan image untuk kasus RGB
    imgToGrayscale()
    cek = imgEstimasiBrightness(imageAfter)
    jenisImage = cekJenisImage(imageLokal)
    factor = 1
    print(cek)
    print(jenisImage)

    if(cek>80):
        # gambar terlalu cerah
        factor = 0.65
    else:
        factor = 1.8
    
    if jenisImage == 2: # jika gambar merupakan rgb
        curentImage = ImageEnhance.Brightness(imageLokal)
    else:
        curentImage = ImageEnhance.Brightness(imageAfter)
    
    adjustedImage = curentImage.enhance(factor)
    saveImageLocal(adjustedImage)
    changeImageBox2(adjustedImage)
    # update penjelasan
    canvas.itemconfig(detail_menu, text="Brightness Adjustment")
    canvas.itemconfig(detail_penjelasan, text="menyesuaikan kecerahan gambar")

def imageSharpness():
    imageLokal = imageAfter.copy()
    curentImage = ImageEnhance.Sharpness(imageLokal)
    adjustedImage = curentImage.enhance(4)
    saveImageLocal(adjustedImage)
    changeImageBox2(adjustedImage)
    # update penjelasan
    canvas.itemconfig(detail_menu, text="Sharpness")
    canvas.itemconfig(detail_penjelasan, text="mempertajam gambar")

def medianFiltering():
    if imageAfter.mode == 'P':
        imageLokal = imageAfter.convert('RGB')
    else:
        imageLokal = imageAfter.copy()

    curentImage = imageLokal.filter(ImageFilter.MedianFilter(size = 3)) 
    saveImageLocal(curentImage)
    changeImageBox2(curentImage)
    # update penjelasan
    canvas.itemconfig(detail_menu, text="Median Filtering")
    canvas.itemconfig(detail_penjelasan, text="menghilangkan noise dari gambar")

def rotateImage():
    curentImage = imageAfter.transpose(Image.ROTATE_90)
    saveImageLocal(curentImage)
    changeImageBox2(curentImage)
    # update penjelasan
    canvas.itemconfig(detail_menu, text="Rotate")
    canvas.itemconfig(detail_penjelasan, text="merotasi gambar sebesar 90 derajat")

def imageFlipHorizontal():
    curentImage = imageAfter.transpose(Image.FLIP_LEFT_RIGHT)
    saveImageLocal(curentImage)
    changeImageBox2(curentImage)
    # update penjelasan
    canvas.itemconfig(detail_menu, text="Flip Horizontal")
    canvas.itemconfig(detail_penjelasan, text="membalik gambar secara horizontal")

def imageEkualisasiHistogram():
    if imageAfter.mode == 'RGBA':
        imageLokal = imageAfter.convert('RGB')
    else:
        imageLokal = imageAfter.copy()

    curentImage = ImageOps.equalize(imageLokal)

    if imageAfter.mode == 'RGBA':
        curentImage = curentImage.convert('RGBA')

    saveImageLocal(curentImage)
    changeImageBox2(curentImage)
    # update penjelasan
    canvas.itemconfig(detail_menu, text="Ekualisasi Histogram")
    canvas.itemconfig(detail_penjelasan, text="meningkatkan kontras gambar dengan mendistribusikan pixel secara merata")

def resetImageChanges():
    global image_image_8 # mengambil variabel image
    image_image_8 = PhotoImage(file=relative_to_assets("image_8.png")) #mendefinisikan ulang image awal
    curentImage = imageBefore.copy()
    saveImageLocal(curentImage) # mereset variabel operasinya
    canvas.itemconfig(image_8, image=image_image_8) # mengupdate canvas
    # update penjelasan
    canvas.itemconfig(detail_menu, text="Reset")
    canvas.itemconfig(detail_penjelasan, text="mengembalikan gambar seperti semula")

def cekJenisImage(img):
    shape = np.array(img).shape
    uniqueValues = np.unique(img)
    hasil = -1
    if len(uniqueValues) == 2 and (0 in uniqueValues and 255 in uniqueValues):
        jenis_img = "Thresholded"
        hasil = 3
    elif len(shape) == 2:
        jenis_img = "Grayscale"
        hasil = 1
    elif len(shape) == 3:
        jenis_img = "RGB"
        hasil = 2
        
    return hasil

def imgEstimasiBrightness(img):
    rerata = np.mean(img)
    return rerata

window = Tk()

window.geometry("960x540")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 540,
    width = 960,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    480.0,
    269.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    480.0,
    270.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    475.0,
    400.0,
    image=image_image_3
)

detail_penjelasan = canvas.create_text(
    451.0,
    401.0,
    anchor="nw",
    text="Penjelasan",
    fill="#E2DED3",
    font=("Roboto Italic", 12 * -1)
)

canvas.create_rectangle(
    450.0,
    395.0,
    914.0,
    396.0,
    fill="#FFFFFF",
    outline="")

detail_menu = canvas.create_text(
    451.0,
    353.0,
    anchor="nw",
    text="Menu",
    fill="#E2DED3",
    font=("Roboto BoldItalic", 26 * -1)
)

canvas.create_text(
    40.0,
    418.0,
    anchor="nw",
    text="Tinggi: 242",
    fill="#E2DED3",
    font=("Roboto MediumItalic", 22 * -1)
)

namaGambar = canvas.create_text(
    40,
    353.3448486328125,
    anchor="nw",
    text="Nama gambar",
    fill="#E2DED3",
    font=("Roboto MediumItalic", 22 * -1)
)

canvas.create_text(
    40,
    387.4827575683594,
    anchor="nw",
    text="Lebar: 275",
    fill="#E2DED3",
    font=("Roboto MediumItalic", 22 * -1)
)

canvas.create_rectangle(
    37.0,
    382.862060546875,
    298.0,
    383.862060546875,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    37.0,
    417.0,
    298.0,
    418.0,
    fill="#FFFFFF",
    outline="")

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    480.0,
    18.0,
    image=image_image_4
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=imgToGrayscale,
    relief="flat"
)
button_1.place(
    x=674.0,
    y=87.0,
    width=116.0,
    height=40.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=rotateImage,
    relief="flat"
)
button_2.place(
    x=809.0,
    y=88.0,
    width=116.0,
    height=40.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=imgTresholding,
    relief="flat"
)
button_3.place(
    x=677.0,
    y=147.0,
    width=116.0,
    height=40.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=imageEkualisasiHistogram,
    relief="flat"
)
button_4.place(
    x=810.0,
    y=147.0,
    width=116.0,
    height=40.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=imgBrightnessAdjustment,
    relief="flat"
)
button_5.place(
    x=674.0,
    y=207.0,
    width=116.0,
    height=40.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=imageFlipHorizontal,
    relief="flat"
)
button_6.place(
    x=809.0,
    y=207.0,
    width=116.0,
    height=40.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=medianFiltering,
    relief="flat"
)
button_7.place(
    x=674.0,
    y=265.0,
    width=116.0,
    height=40.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=imageSharpness,
    relief="flat"
)
button_8.place(
    x=809.0,
    y=265.0,
    width=116.0,
    height=40.0
)

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=saveFileImage,
    relief="flat"
)
button_9.place(
    x=506.0,
    y=482.0,
    width=420.0,
    height=40.0
)

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=openFile,
    relief="flat"
)
button_10.place(
    x=28.0,
    y=482.0,
    width=420.0,
    height=40.0
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    177.0,
    188.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    177.335693359375,
    187.9558868408203,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    488.0,
    187.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    488.335693359375,
    186.9558868408203,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    693.0,
    46.0,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    900.0,
    50.0,
    image=image_image_10
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    17.0,
    17.0,
    image=image_image_11
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    942.0,
    17.0,
    image=image_image_12
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    17.0,
    522.0,
    image=image_image_13
)

image_image_14 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(
    942.0,
    521.9999938804057,
    image=image_image_14
)

canvas.create_rectangle(
    955.9999648566534,
    34.999999947916024,
    959.9999648332596,
    516.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    -1.9999652494341262,
    32.999999948315235,
    2.0001021644770844,
    505.00006103515625,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    35.0,
    538.0,
    925.0,
    540.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    35.0,
    0.0,
    925.0,
    2.0,
    fill="#FFFFFF",
    outline="")

button_image_11 = PhotoImage(
    file=relative_to_assets("button_11.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=resetImageChanges,
    relief="flat"
)
button_11.place(
    x=752.0,
    y=30.0,
    width=85.0,
    height=40.0
)
window.resizable(False, False)
window.mainloop()
