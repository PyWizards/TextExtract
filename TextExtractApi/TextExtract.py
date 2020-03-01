# coding=utf-8
"""
Tesseract version used is : tesseract 4.0.0-beta.3
"""
import subprocess
import time
from difflib import SequenceMatcher
import threading
import cv2
from queue import Queue
import numpy as np
from PIL import Image
import os

def run_cmd(cmd, timeout_sec=5):
    """
    Run cmd command with timeout
    Args:
        cmd(list): The command to be run
        timeout_sec(int) : The timeout of cmd

    Returns:
        str (stdout) : The output of subprocess
        str(stderr) : The error in subprocess

    """
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timer = threading.Timer(timeout_sec, process.kill)
    try:
        timer.start()
        stdout, stderr = process.communicate()
        stdout = stdout.decode('utf8')
        stderr = stderr.decode('utf8')
    finally:
        timer.cancel()
    return stdout, stderr, process.returncode, process.pid

def tess_img_to_string(temp_image_name, scaling_factor, lang='eng', psm=3):
    """
        Extract text from image
    Args:
        temp_image_name (str) : The path of image
        scaling_factor (str) : The scaling factor for image scaling
        lang (str) : The language of text
        psm (int) : The page segmentation key
    Returns:
        str : The text extracted from image
    """
    out_txt=''
    tes_exe = os.path.abspath(os.path.dirname(__file__) + '/tesseract.exe')
    file_name = os.path.abspath(temp_image_name)
    out_file_name = os.path.abspath(os.path.dirname(__file__) + '/ocr_out_{}'.format(scaling_factor))
    cmd = [tes_exe, file_name, out_file_name, "-l", lang, "--psm", str(psm)]
    stdout, stderr, return_code, pid = run_cmd(cmd)
    time.sleep(2)
    if return_code == 0:
        with open(out_file_name + '.txt',encoding='utf8') as file:
            out_txt = file.read().replace('\x0c', '').strip()
        os.remove(out_file_name + '.txt')
    else:
        print('Failed - Image : {}\n Scaling :{}'.format(temp_image_name, scaling_factor))
        print('Process Id : {} \tReturn Code :{}\tOutput : {}'.format(pid, return_code, stdout))
    return out_txt


class TextExtract:
    def __init__(self, lang):
        """
            Init language,scaling constants and thread
        Args:
            lang (str) : The language of text
        """
        self.scaling_factors = [0, 1, 2, 4, 8, 16]
        self.result_text = []
        self.OCR_Thread = Queue()
        self.image_path = None
        self.lang = lang

    def tes_extract_thread(self, scaling_factor):
        """
            Thread for extracting text from image
        Args:
            scaling_factor (str) : The scaling factor for image scaling
        Returns:
            list : The total extracted result from tesseract
        """
        if scaling_factor is not 0:
            img_path = self.image_path
            temp_image_name = os.path.abspath("./temp_{}.png".format(scaling_factor))
            cv_img = cv2.imread(img_path, 0)
            cv_img = cv2.resize(cv_img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_LANCZOS4)
            kernel = np.ones((1, 1), np.uint8)
            cv_img = cv2.erode(cv_img, kernel, iterations=1)
            cv_img = cv2.dilate(cv_img, kernel, iterations=1)
            cv_img = cv2.GaussianBlur(cv_img, (5, 5), 0)

            ret, cv_img = cv2.threshold(cv_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            cv2.imwrite(temp_image_name, cv_img)
            img_pil = Image.open(temp_image_name)
            img_pil.save(temp_image_name, dpi=(300, 300))
            result_text_thread = tess_img_to_string(temp_image_name, scaling_factor, lang=self.lang)
            self.result_text.append(result_text_thread)

        else:
            result_text_thread = tess_img_to_string(self.image_path, scaling_factor='NA', lang=self.lang)
            self.result_text.append(result_text_thread)

    def tesseract_worker(self):
        """
             Worker thread for tesseract
        """
        while True:
            x = self.OCR_Thread.get()
            if x is None:
                break
            self.tes_extract_thread(x)
            self.OCR_Thread.task_done()

    def clean_temp_img(self):
        """
            Clear Temp image from path
         """
        [os.remove(os.path.abspath('./' + temp_file)) for temp_file in
         os.listdir(os.path.abspath('./')) if
         'temp_' in temp_file]

    def image_to_string(self, image_path, expected_text=''):
        """
            Image to string with expected text matching
        Args:
            image_path (str) : Path of image
            expected_text (str) : Expected text
        Returns:
            (tuple): tuple containing:
                str : The highest matching text (final_text)
                str : Highest percent (highest_per)
                list : The total extracted result from tesseract (self.result_text)

         """
        threads = []
        thread_count = 5
        self.image_path = image_path
        for x in range(0, thread_count):
            t = threading.Thread(target=self.tesseract_worker)
            threads.append(t)
            t.start()
        for x in self.scaling_factors:
            self.OCR_Thread.put(x)
        self.OCR_Thread.join()

        for _ in threads:
            self.OCR_Thread.put(None)
        for t in threads:
            t.join()

        final_result_percent = {}
        for index, res in enumerate(self.result_text):
            seq = SequenceMatcher(None, res, expected_text)
            final_result_percent[index] = {'Text': res, "Match": seq.ratio() * 100}
        highest_per = -1.0
        final_text = ''
        for final_res in final_result_percent.values():
            result_per = final_res['Match']
            if highest_per < result_per and final_res['Text'] != '':
                final_text = final_res['Text']
                highest_per = result_per
        self.clean_temp_img()
        return final_text, highest_per, self.result_text


class TesseractOCR:
    def __init__(self, lang):
        """
            Init lang
        Args:
            lang (str) : The language of text
         """
        self.lang = lang

    def scaling_factor_result(self, img_path, scaling_factor):
        """
            Extract result from image based on scaling factor
        Args:
            img_path (str) : The path of image
            scaling_factor (str) : The scaling factor of image
        Returns:
            str : The result text of image (result)
         """
        cv_img = cv2.imread(img_path, 0)
        cv_img = cv2.resize(cv_img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_LANCZOS4)
        kernel = np.ones((1, 1), np.uint8)
        cv_img = cv2.erode(cv_img, kernel, iterations=1)
        cv_img = cv2.dilate(cv_img, kernel, iterations=1)
        cv_img = cv2.GaussianBlur(cv_img, (5, 5), 0)

        ret, cv_img = cv2.threshold(cv_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        cv2.imwrite("temp_only_text.png", cv_img)
        img_pil = Image.open("temp_only_text.png")
        img_pil.save("temp_only_text.png", dpi=(300, 300))
        result = tess_img_to_string("temp_only_text.png", scaling_factor=scaling_factor, lang=self.lang)
        os.remove("temp_only_text.png")
        return result

    def image_to_string(self, img_path, pre_process_img=True):
        """
            Pre-process image and provide text
        Args:
             img_path (str) : The path of image
             pre_process_img (bool) : Pre-process image or not
        Returns:
            (tuple): tuple containing:
                 str : Result text (result),
                 int : Original scale (x_scale),
                 int : Adjusted scale (x_scale,x_up,x_down,'NA')
         """
        x_scale_up = None
        x_scale_down = None
        if pre_process_img:
            x_scale_values = [1, 2, 4, 8, 16, 32]
            im = Image.open(img_path)
            w, h = im.size
            if w > h:
                if 0 <= w / h <= 1:
                    x_scale = 4
                else:
                    x_scale = float(w) / float(h)
            else:
                if 0 <= h / w <= 1:
                    x_scale = 4
                else:
                    x_scale = float(h) / float(w)

            if x_scale <= 2:
                x_scale = 2
            elif 2 <= x_scale <= 4:
                x_scale = 4
            elif 4 <= x_scale <= 8:
                x_scale = 8
            elif 8 <= x_scale <= 16:
                x_scale = 16
            elif 16 <= x_scale <= 32:
                x_scale = 32
            return_scale = 'x_scale'
            result = self.scaling_factor_result(img_path, x_scale)

            def_scale_index = x_scale_values.index(x_scale)
            for i in range((def_scale_index + 1), len(x_scale_values)):
                if result == '':
                    x_scale_up = x_scale_values[i]
                    result = self.scaling_factor_result(img_path, x_scale_up)
                    return_scale = 'x_up'
                else:
                    break

            for i in range((def_scale_index - 1), -1, -1):
                if result == '':
                    x_scale_down = x_scale_values[i]
                    result = self.scaling_factor_result(img_path, x_scale_down)
                    return_scale = 'x_down'
                else:
                    break

            if result == '':
                result = tess_img_to_string(img_path, scaling_factor='NA', lang=self.lang)
                return_scale = 'NA'

            if return_scale == 'x_scale':
                return result, x_scale, x_scale
            elif return_scale == 'x_up':
                return result, x_scale_up, x_scale
            elif return_scale == 'x_down':
                return result, x_scale_down, x_scale
            elif return_scale == 'NA':
                return result, 'NA', x_scale
        else:
            result = tess_img_to_string(img_path, scaling_factor='NA', lang=self.lang)
            return result, 'NA', 'NA'


class TextExtractFunctions:
    def __init__(self):
        pass

    @classmethod
    def image_to_string_only(cls, image_path, lang):
        """
            Extract result from image without matching expected text
        Args:
            image_path (str) : The path of image
            lang (str) : The Language of text
        Returns:
            (tuple): tuple containing:
                str : The result text of image (result)
                int : The scale of image (scale)
         """
        ocr_object = TesseractOCR(lang)
        result, NA, scale = ocr_object.image_to_string(image_path)
        return result, scale

    @classmethod
    def image_to_string_matched(cls, image_path, expected_text, lang='eng',all_results=False):
        """
            Extract result from image with matching expected text
            Args:
                 image_path (str) : The path of image
                 expected_text (str) : Expected text
                 lang (str) : The Language of text
                 all_results (bool) : Return all result list or not
            Returns:
                tuple : The result text and match percent (result) and lis of all text found after scaling images

         """

        ocr_object = TextExtract(lang)
        if os.path.isfile(os.path.abspath(image_path)):
            final_text, highest_per, result_text = ocr_object.image_to_string(image_path, expected_text)
            result = [final_text, highest_per]
            if result[1] <= 0.0:
                res = tess_img_to_string(image_path, 'NA', psm=7, lang=lang)
                seq = SequenceMatcher(None, res, expected_text)
                match = seq.ratio() * 100
                # result[2].append(res)
                result = [res, match]

            if all_results:
                return result,ocr_object.result_text
            else:
                return result
        else:
            raise Exception("Image Not found",)

