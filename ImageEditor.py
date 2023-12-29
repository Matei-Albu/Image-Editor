from PIL import Image
from typing import List

def mirror(raw: List[List[List[int]]])-> None:

    for i in range(len(raw)):
        raw[i]=raw[i][::-1]
    return raw

def grey(raw: List[List[List[int]]])-> None:

    total = 0
    counter = 0
    for i in raw:
        for j in i:
            for k in j:
                counter += 1
                total = total + k 
                if counter == 3:
                    avg = total//3
                    counter = 0;
                    j[0] = j[1]= j[2] = avg
                    total = 0
    return raw


def invert(raw: List[List[List[int]]])-> None:
    for i in raw:
        for j in i:
            minimum = min(j)
            maximum = max(j)
           
            for k in range(len(j)):
                if j[k] == minimum or j[k] == maximum:
                    j[k] = minimum + maximum - j[k]

    return raw


def stripes(raw1: List[List[List[int]]], raw2: List[List[List[int]]])-> List[List[List[int]]]:
    height = max(len(raw1), len(raw2))

    width = max(len(raw1[0]) if raw1 and raw1[0] else 0,
                len(raw2[0]) if raw2 and raw2[0] else 0)

    new = [
        [
            raw1[i][j] if i < len(raw1) and j < len(raw1[i]) and i % 2 == 0 
            else raw2[i][0] if i < len(raw2) and j < len(raw2[i]) 
            else [255, 255, 255]
            
            for j in range(width)
        ]
        for i in range(height)
    ]

    return new
    
    


def compress(raw: List[List[List[int]]]) -> List[List[List[int]]]:
    compressed = []

    for i in range(0, len(raw), 2):
        row = []

        for j in range(0, len(raw[0]), 2):
            sum_channel = [0, 0, 0]

            for x in range(min(2, len(raw) - i)):
                for y in range(min(2, len(raw[0]) - j)):
                    pixel = raw[i + x][j + y]
                    sum_channel = [sum_c + pixel[channel] for channel, sum_c in enumerate(sum_channel)]

            avg = [channel // 4 for channel in sum_channel]  
            row.append(avg)

        compressed.append(row)

    return compressed

def get_raw_image(name: str)-> List[List[List[int]]]:
    
    image = Image.open(name)
    num_rows = image.height
    num_columns = image.width
    pixels = image.getdata()
    new_data = []
    
    for i in range(num_rows):
        new_row = []
        for j in range(num_columns):
            new_pixel = list(pixels[i*num_columns + j])
            new_row.append(new_pixel)
        new_data.append(new_row)

    image.close()
    return new_data


def image_from_raw(raw: List[List[List[int]]], name: str)->None:
    image = Image.new("RGB", (len(raw[0]),len(raw)))
    pixels = []
    for row in raw:
        for pixel in row:
            pixels.append(tuple(pixel))
    image.putdata(pixels)
    image.save(name)
                      

def main():
    image_name = "tree.png"

    raw_image_data = get_raw_image(image_name)
    raw_image_data_2 = get_raw_image(image_name) 


    #mirrored_image_data = mirror(raw_image_data)
    #grayscale_image_data = grey(raw_image_data)  
    #inverted_image_data = invert(raw_image_data)
    #raw_image_data_2 = get_raw_image("example2.png")
    stripes_image_data = stripes(raw_image_data, raw_image_data_2)
    #compressed_image_data = compress(raw_image_data)

    #image_from_raw(mirrored_image_data, "mirrored_tree.jpg")
    #image_from_raw(grayscale_image_data, "grayscale_tree.jpg")  
    #image_from_raw(inverted_image_data, "inverted_tree.jpg")
    image_from_raw(stripes_image_data, "stripes_tree.jpg")
    #image_from_raw(compressed_image_data, "compressed_tree.jpg")

if __name__ == "__main__":
    main()
                      
