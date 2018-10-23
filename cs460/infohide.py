import numpy as np
import cv2

def embed_image(secret, cover, bits):
    img_cover = cv2.imread(cover)
    #img_cover = cv2.resize(img_cover, (1280, 720))
    img_secret = cv2.imread(secret)
    #img_secret = cv2.resize(img_secret, (1280, 720))
    secret_shape = img_secret.shape
    blue = 0
    green = 1
    red = 2
    for row in range(0, secret_shape[0]):
        for col in range(0, secret_shape[1]):
            curr_pixel = img_secret[row, col]
            blue_secret = curr_pixel[blue]
            green_secret = curr_pixel[green]
            red_secret = curr_pixel[red]
            #Extract n number of bits from secrets
            binary_b = format(blue_secret, '08b')
            binary_g = format(green_secret, '08b')
            binary_r = format(red_secret, '08b')
            sigbits_blue = ""
            sigbits_green = ""
            sigbits_red = ""
            #Extract 4 most significant bits from each of the colors.
            for i in range(0, bits):
                sigbits_blue += binary_b[i]
                sigbits_green += binary_g[i]
                sigbits_red += binary_r[i]
            #Now lets apply these in the cover in the n number of least sig bits.
            cover_pixel = img_cover[row,col]
            cover_b_binary = format(cover_pixel[blue], '08b')
            cover_g_binary = format(cover_pixel[green], '08b')
            cover_r_binary = format(cover_pixel[red], '08b')
            b_binary2 = ""
            g_binary2 = ""
            r_binary2 = ""
            #recreate the byte
            bit_cnt = 8-bits
            curr_bit = 0
            for i in range(0, 8):
                if i == bit_cnt:
                    b_binary2 += sigbits_blue
                    g_binary2 += sigbits_green
                    r_binary2 += sigbits_red
                    break
                else:
                    b_binary2 += cover_b_binary[i]
                    g_binary2 += cover_g_binary[i]
                    r_binary2 += cover_r_binary[i]

            # now, lets apply our new covers to the image
            final_blue = int(b_binary2,2)
            final_green = int(g_binary2,2)
            final_red = int(r_binary2,2)
            img_cover.itemset((row,col,blue),final_blue)
            img_cover.itemset((row,col,green),final_green)
            img_cover.itemset((row,col,red),final_red)
    cv2.imwrite('hidden.png', img_cover)

def extract_image(picture, bits):
    img = cv2.imread(picture)
    #img = cv2.resize(img, (1280, 720))
    shape = img.shape
    blue = 0
    green = 1
    red = 2
    for row in range(0, shape[0]):
        for col in range(0, shape[1]):
            #Extract our original cover
            curr_pixel = img[row, col]
            binary_b = format(curr_pixel[blue], '08b')
            binary_g = format(curr_pixel[green], '08b')
            binary_r = format(curr_pixel[red], '08b')
            b_extract = ""
            g_extract = ""
            r_extract =""
            #Lets recreate the secret - MSB = LSB of stego,
            cnt = 8-bits
            for i in range(0, 8):
                if i < bits:
                    #if this is true, then we append the least sig bits of steg are the MSB of the secret
                    b_extract += binary_b[cnt]
                    g_extract += binary_g[cnt]
                    r_extract += binary_r[cnt]
                    cnt+=1
                else:
                    b_extract += '0'
                    g_extract += '0'
                    r_extract += '0'
            final_blue = int(b_extract, 2)
            final_green = int(g_extract, 2)
            final_red = int(r_extract, 2)
            img.itemset((row, col, blue), final_blue)
            img.itemset((row, col, green), final_green)
            img.itemset((row, col, red), final_red)
    cv2.imwrite('secret.png', img)
















if __name__ == '__main__':
    embed_image('deku.png', 'KH3.png', 1)
    extract_image('hidden.png', 1)
    #resized_image = cv2.resize(image, (100, 50))
