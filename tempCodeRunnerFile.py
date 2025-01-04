def imageEkualisasiHistogram():
    curentImage = ImageOps.equalize(imageAfter)
    saveImageLocal(curentImage)
    changeImageBox2(curentImage)