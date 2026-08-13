import cv2

# 1. Read the image
image = cv2.imread('cat.png')
assert image is not None, "Error: Could not load image. Check the file path."

# Resize the image
resized = cv2.resize(image, (128, 160), interpolation=cv2.INTER_AREA)

# 2. Open binary file
with open('cat1.bin', 'wb') as f:
    for y in range(160):
        for x in range(128):
            
            b, g, r = map(int, resized[y, x])
            
            # Compress into standard 16-bit RGB565
            color565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            
            # THE FIX: Do not manually swap the bytes. 
            # Write it directly as standard Big-Endian.
            f.write(color565.to_bytes(2, 'big'))

print("Done! Upload this new image.bin to the board.")