import logging
import os
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

# sudo apt install tesseract-ocr
# pip3 install pytesseract


# sudo apt-get remove tesseract-ocr
# git clone https://github.com/tesseract-ocr/tesseract.git
# sudo apt-get install libtool
# sudo apt-get install libleptonica-dev
# cd tesseract
# ./autogen.sh
# ./configure
# make
# sudo make install
# sudo ldconfig
# make training
# sudo make training-install


class TextExtractor:
    def enhance(self, pil_img):
        # im = im.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(pil_img)
        res_img = enhancer.enhance(2)
        res_img = res_img.convert('L')
        return res_img


    @staticmethod
    def available_languages():
        print(pytesseract.get_languages(config=''))

    def extract_text_entries(self, img_path):
        if not os.path.exists(img_path):
            logging.error(f'Given path does not exist: {img_path}')
            return []

        img = Image.open(img_path)
        img = self.enhance(img)
        # img.show()
        raw_result = pytesseract.image_to_string(img,
                                                 lang='eng+lit',
                                                 # config="--psm 12 --oem 3 -c page_separator=''",
                                                 config="--oem 3 -c page_separator=''",
                                                 #output_type=pytesseract.Output.DICT,
                                                 output_type=pytesseract.Output.STRING,
                                                 timeout=10)

        # r1 = raw_result.replace('\n', ' and ')
        r1 = raw_result
        # r2 = r1.split('\n')
        # r3 = [x for x in r2 if len(x) > 1]
        return r1


if __name__ == '__main__':
    x = TextExtractor()
    x.available_languages()
    print(x.extract_text_entries('../card_samples/card_3.png'))