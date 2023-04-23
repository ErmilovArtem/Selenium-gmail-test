import time
import random
import string

import os.path
import quopri

import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio

import numpy as np
import selenium as sl
import unittest

from PIL import Image
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

import imaplib
import email
from email.header import decode_header
import base64
import re

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version

mail_pass = "fjqtachxjtcwmmja"
username = "aermilov756@gmail.com"
imap_server = "imap.gmail.com"
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, mail_pass)

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

mail_pass = "fjqtachxjtcwmmja"
username = "aermilov756@gmail.com"
imap_server = "imap.gmail.com"
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, mail_pass)

class TestGmailChrome(unittest.TestCase):
    def get_driver_Chrom(self):
        opts = Options()
        opts.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
        return sl.webdriver.Chrome(chrome_options=opts)

    def get_driver_Edge(self):
        return sl.webdriver.Edge()

    def attach_file(self, msg, filepath):  # Функция по добавлению конкретного файла к сообщению
        filename = os.path.basename(filepath)  # Получаем только имя файла
        ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
        if ctype is None or encoding is not None:  # Если тип файла не определяется
            ctype = 'application/octet-stream'  # Будем использовать общий тип
        maintype, subtype = ctype.split('/', 1)  # Получаем тип и подтип
        if maintype == 'text':  # Если текстовый файл
            with open(filepath) as fp:  # Открываем файл для чтения
                file = MIMEText(fp.read(), _subtype=subtype)  # Используем тип MIMEText
                fp.close()  # После использования файл обязательно нужно закрыть
        elif maintype == 'image':  # Если изображение
            with open(filepath, 'rb') as fp:
                file = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
        elif maintype == 'audio':  # Если аудио
            with open(filepath, 'rb') as fp:
                file = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
        else:  # Неизвестный тип файла
            with open(filepath, 'rb') as fp:
                file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
                file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
                fp.close()
                encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
        file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
        msg.attach(file)  # Присоединяем файл к сообщению


    def process_attachement(self, msg, files):  # Функция по обработке списка, добавляемых к сообщению файлов
        for f in files:
            if os.path.isfile(f):  # Если файл существует
                self.attach_file(msg, f)  # Добавляем файл к сообщению
            elif os.path.exists(f):  # Если путь не файл и существует, значит - папка
                dir = os.listdir(f)  # Получаем список файлов в папке
                for file in dir:  # Перебираем все файлы и...
                    self.attach_file(msg, f + "/" + file)  # ...добавляем каждый файл к сообщению

    def send_email(self, addr_to, msg_subj, msg_text, files):
        addr_from = "aermilov756@gmail.com"  # Отправитель
        password = "fjqtachxjtcwmmja"  # Пароль

        msg = MIMEMultipart()  # Создаем сообщение
        msg['From'] = addr_from  # Адресат
        msg['To'] = addr_to  # Получатель
        msg['Subject'] = msg_subj  # Тема сообщения

        body = msg_text  # Текст сообщения
        msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

        self.process_attachement(msg, files)

        # ======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================================
        server = smtplib.SMTP_SSL('smtp.gmail.com')  # Создаем объект SMTP
        # server.starttls()                                      # Начинаем шифрованный обмен по TLS
        # server.set_debuglevel(True)                            # Включаем режим отладки, если не нужен - можно закомментировать
        server.login(addr_from, password)  # Получаем доступ
        server.send_message(msg)  # Отправляем сообщение
        server.quit()  # Выходим
        # ==========================================================================================================================

    def go_to_main_page(self, driver):
        driver.get('https://account.mail.ru/')
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys("witchxxxch12")
        driver.find_element(By.XPATH, '//button[@data-test-id="next-button"]').click()
        time.sleep(0.5)
        driver.find_element(By.NAME, 'password').send_keys("zefirzwWw7770")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-test-id="submit-button"]'))).click()
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-test-id="submit-button"]'))).click()
        try:
            time.sleep(1.5)
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//div[starts-with(@class, "ph-project-promo-container")]//div[starts-with(@class, "ph-project-promo-close-icon__container")]'))).click()
        except Exception:
            pass

    def give_last_message(self):
        time.sleep(4)
        res, msg = imap.fetch(imap.select("INBOX")[1][0], '(RFC822)')
        msg = email.message_from_bytes(msg[0][1])
        header = decode_header(msg["Subject"])[0][0].decode()
        for part in msg.walk():
            if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                message = base64.b64decode(part.get_payload()).decode()
        return header, message

    def encoded_words_to_text(self, encoded_words):
        try:
            encoded_word_regex = r'=\?{1}(.+)\?{1}([B|Q])\?{1}(.+)\?{1}='
            charset, encoding, encoded_text = re.match(encoded_word_regex, encoded_words).groups()
            if encoding is 'B':
                byte_string = base64.b64decode(encoded_text)
            elif encoding is 'Q':
                byte_string = quopri.decodestring(encoded_text)
            return byte_string.decode(charset)
        except:
            return encoded_words

    def give_attachment(self):
        counter = 0
        res, msg = imap.fetch(imap.select("INBOX")[1][0], '(RFC822)')
        print(decode_header(email.message_from_bytes(msg[0][1])["Subject"])[0][0].decode())
        msg = email.message_from_bytes(msg[0][1])
        for part in msg.walk():
            counter += 1
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()
            fileName = self.encoded_words_to_text(fileName)
            print(fileName)
            if bool(fileName):
                try:
                    filePath = os.path.join('C:\\Users\\march\\PycharmProjects\\GmailTest\\content', fileName)
                    with open(filePath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                except Exception:
                    filePath = os.path.join('C:\\Users\\march\\PycharmProjects\\GmailTest\\content',
                                            str(counter) + '.png')
                    with open(filePath, 'wb') as f:
                        f.write(part.get_payload(decode=True))

    def test_reg(self):
        password = generate_random_string(16)
        driver = self.get_driver_Chrom()
        driver.get('https://mail.ru/')
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, '//a[@data-testid="mailbox-create-link"]'))).click()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, '//label[@data-test-id="gender-male"]'))).click()
        for id_with_keys in [["fname", generate_random_string(8)],
                     ["lname", generate_random_string(8)],
                     ["aaa__input", generate_random_string(16)],
                     ["password", password],
                     ["repeatPassword", password]]:
            driver.find_element(By.ID,
                                id_with_keys[0]).send_keys(id_with_keys[1])
        driver.find_element(By.XPATH, '//a[@data-test-id="phone-number-switch-link"]').click()
        driver.find_element(By.XPATH, '//input[@name="email"]').send_keys("witchxxxch12@mail.ru")
        driver.find_element(By.XPATH, '//div[@data-test-id="birth-date__day"]').click()
        driver.find_element(By.XPATH, '//div[@data-test-id="select-menu-wrapper"]').find_element(By.XPATH, '//div[@data-test-id="select-value:11"]').click()
        driver.find_element(By.XPATH, '//div[@data-test-id="birth-date__month"]').click()
        driver.find_element(By.XPATH, '//div[@data-test-id="select-menu-wrapper"]').find_element(By.XPATH, '//div[@data-test-id="select-value:11"]').click()
        driver.find_element(By.XPATH, '//div[@data-test-id="birth-date__year"]').click()
        driver.find_element(By.XPATH, '//div[@data-test-id="select-menu-wrapper"]').find_element(By.XPATH, '//div[@data-test-id="select-value:2003"]').click()
        driver.find_element(By.XPATH, '(//button[@data-test-id="first-step-submit"])[2]').click()
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, '//input[@id="phone-number__phone-input"]'))).send_keys("9187832536")
        driver.find_element(By.XPATH, '(//button[@data-test-id="first-step-submit"])[2]').click()
        try:
            WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.XPATH, '//*[@data-test-id="verification-step-header-recaptcha"]')))
            driver.find_element(By.XPATH, '//*[@data-test-id="verification-step-header-recaptcha"]')
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)

    def test_auth(self):
        driver = self.get_driver_Chrom()
        driver.get('https://account.mail.ru/')
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys("witchxxxch12")
        driver.find_element(By.XPATH, '//button[@data-test-id="next-button"]').click()
        time.sleep(0.5)
        driver.find_element(By.NAME, 'password').send_keys("zefirzwWw7770")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-test-id="submit-button"]'))).click()
        try:
            WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'portal-menu-logo__image-wrapper')))
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)

    def test_auth_vk(self): #не хочу тратить деньги на сервис с телефонами
        driver = self.get_driver_Chrom()
        driver.get('https://account.mail.ru/')
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, '//button[@data-test-id="social-vk"]'))).click()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.NAME, 'phone'))).send_keys("9187838236")
        try:
            WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.ID, 'otp')))
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)

    def test_email_send_simple(self):
        driver = self.get_driver_Chrom()
        self.go_to_main_page(driver)
        time.sleep(0.1)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'compose-button__wrapper'))).click()
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-name="to"]//input'))).send_keys("aermilov756@gmail.com")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.NAME, 'Subject'))).send_keys("Test of email sender 1")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-signature-widget="content"]'))).send_keys("\b" * 100 + "Tested Data")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-test-id="send"]'))).click()
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        header, message = self.give_last_message()
        self.assertEqual(header, 'Test of email sender 1')
        self.assertEqual(message, '\nTested Data')

    def test_email_send_to_me(self):
        driver = self.get_driver_Chrom()
        self.go_to_main_page(driver)
        time.sleep(0.1)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'compose-button__wrapper'))).click()
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-name="to"]//input'))).send_keys("witchxxxch12@mail.ru")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.NAME, 'Subject'))).send_keys("Test of email sender 1.1")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-signature-widget="content"]'))).send_keys("\b" * 100 + "Tested Data")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-test-id="send"]'))).click()
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//a[starts-with(@class, "llc ")][1]'))).click()
        elem = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="letter__body"]//div[starts-with(@id, "style")]//div//div')))
        header = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//h2[@class="thread-subject"]')))

        self.assertEqual(header.text, 'Test of email sender 1.1')
        self.assertEqual(elem.text, 'Tested Data')

    def test_email_send_emoji(self):
        driver = self.get_driver_Chrom()
        self.go_to_main_page(driver)
        time.sleep(0.1)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'compose-button__wrapper'))).click()
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-name="to"]//input'))).send_keys("aermilov756@gmail.com")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.NAME, 'Subject'))).send_keys("Test of email sender 2")
        time.sleep(0.5)
        driver.execute_script("arguments[0].innerHTML = '{}'".format("👺🤡🤡🤡👺"), driver.find_element(By.XPATH, '//div[@data-signature-widget="content"]'))
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-test-id="send"]'))).click()
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        header, message = self.give_last_message()
        self.assertEqual(header, 'Test of email sender 2')
        self.assertTrue('\n👺🤡🤡🤡👺' in message)

    def test_email_send_big_email(self):
        driver = self.get_driver_Chrom()
        self.go_to_main_page(driver)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'compose-button__wrapper'))).click()
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-name="to"]//input'))).send_keys("aermilov756@gmail.com")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.NAME, 'Subject'))).send_keys("Test of email sender 3")
        time.sleep(1.5)
        WebDriverWait(driver, 6).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-signature-widget="content"]'))).send_keys("\b" * 100 + "test" * 50)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-test-id="send"]'))).click()
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        header, message = self.give_last_message()
        self.assertEqual(header, 'Test of email sender 3')
        self.assertTrue(("test" * 50) in message)

    def test_email_sender_many(self):
        driver = self.get_driver_Chrom()
        self.go_to_main_page(driver)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'compose-button__wrapper'))).click()
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-name="to"]//input'))).send_keys("aermilov756@gmail.com artemerm20012003@gmail.com")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.NAME, 'Subject'))).send_keys("Test of email sender 4")
        WebDriverWait(driver, 6).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-signature-widget="content"]'))).send_keys("\b" * 100 + "test")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-test-id="send"]'))).click()
        time.sleep(2)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        mail_pass = "fjqtachxjtcwmmja"
        username = "aermilov756@gmail.com"
        imap_server = "imap.gmail.com"
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(username, mail_pass)
        res, msg = imap.fetch(imap.select("INBOX")[1][0], '(RFC822)')
        msg = email.message_from_bytes(msg[0][1])
        header = decode_header(msg["Subject"])[0][0].decode()
        for part in msg.walk():
            if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                message = base64.b64decode(part.get_payload()).decode()
        self.assertEqual(header, 'Test of email sender 4')
        self.assertTrue(("test") in message)
        imap.close()
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login("artemerm20012003@gmail.com", "ffrpuhzsmtqupbqm")
        res, msg = imap.fetch(imap.select("INBOX")[1][0], '(RFC822)')
        msg = email.message_from_bytes(msg[0][1])
        header = decode_header(msg["Subject"])[0][0].decode()
        for part in msg.walk():
            if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                message = base64.b64decode(part.get_payload()).decode()
        self.assertEqual(header, 'Test of email sender 4')
        self.assertTrue(("test") in message)

    def test_email_sender_jpg(self):
        driver = self.get_driver_Chrom()
        self.go_to_main_page(driver)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'compose-button__wrapper'))).click()
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-name="to"]//input'))).send_keys("aermilov756@gmail.com")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.NAME, 'Subject'))).send_keys("Test of email sender 5")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//input[starts-with(@class, "inline_input")]'))).send_keys("C:\\Users\\march\\Downloads\\Telegram Desktop\\photo_2023-01-15_23-49-55.jpg")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-test-id="send"]'))).click()
        time.sleep(4)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        header, msg = self.give_last_message()
        self.give_attachment()
        self.assertEqual(header, 'Test of email sender 5')
        self.assertEqual(np.array_equal(np.asarray(Image.open('C:\\Users\\march\\Downloads\\Telegram Desktop\\photo_2023-01-15_23-49-55.jpg'), dtype='uint8'),
                                        np.asarray(Image.open('C:\\Users\\march\\PycharmProjects\\GmailTest\\content\\photo_2023-01-15_23-49-55.jpg'), dtype='uint8')), True)

    def test_email_sender_files(self):
        driver = self.get_driver_Chrom()
        self.go_to_main_page(driver)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'compose-button__wrapper'))).click()
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-name="to"]//input'))).send_keys("aermilov756@gmail.com")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.NAME, 'Subject'))).send_keys("Test of email sender 6")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//input[starts-with(@class, "desktopInput")]'))).send_keys("C:\\Users\\march\\Downloads\\Telegram Desktop\\db.accdb")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//input[starts-with(@class, "desktopInput")]'))).send_keys("C:\\Users\\march\\Downloads\\Telegram Desktop\\NuT (2).pptx")
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-test-id="send"]'))).click()
        time.sleep(4)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        header, msg = self.give_last_message()
        self.give_attachment()
        for elem in ["db.accdb", "NuT (2).pptx"]:
            with open("C:\\Users\\march\\Downloads\\Telegram Desktop\\" + elem, "rb") as file1:
                with open("C:\\Users\\march\\PycharmProjects\\GmailTest\\content\\" + elem, "rb") as file2:
                    self.assertEqual(header, 'Test of email sender 6')
                    self.assertEqual(file1.read(), file2.read())

    def test_email_reader_simple_text(self):
        server = 'smtp.gmail.com'

        recipients = ['witchxxxch12@mail.ru']
        sender = username
        subject = 'Test of email reader'
        text = 'tested data'
        html = '<html><head></head><body><p>' + text + '</p></body></html>'

        filepath = "C:\\Users\\march\\PycharmProjects\\GmailTest\\content\\photo_2023-01-15_23-49-55.jpg"
        basename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = 'Python script <' + sender + '>'
        msg['To'] = ', '.join(recipients)
        msg['Reply-To'] = sender
        msg['Return-Path'] = sender
        msg['X-Mailer'] = 'Python/' + (python_version())

        part_text = MIMEText(text, 'plain')
        part_html = MIMEText(html, 'html')
        part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
        part_file.set_payload(open(filepath, "rb").read())
        part_file.add_header('Content-Description', basename)
        part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
        encoders.encode_base64(part_file)

        msg.attach(part_text)
        msg.attach(part_html)
        #msg.attach(part_file)

        mail = smtplib.SMTP_SSL(server)#IMAP4_SSL
        mail.login(username, mail_pass)
        mail.sendmail(sender, recipients, msg.as_string())
        mail.quit()

        time.sleep(3)

        driver = self.get_driver_Chrom()
        self.go_to_main_page(driver)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//a[starts-with(@class, "llc ")][1]'))).click()
        elem = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="letter__body"]//div[starts-with(@id, "style")]//p')))
        header = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//h2[@class="thread-subject"]')))

        self.assertEqual(header.text, 'Test of email reader')
        self.assertEqual(elem.text, 'tested data')

    def test_email_reader_with_img(self):
        addr_to = "witchxxxch12@mail.ru"  # Получатель
        files = ["C:\\Users\\march\\PycharmProjects\\GmailTest\\content\\photo_2023-01-15_23-49-55.jpg"]  # Если нужно отправить все файлы из заданной папки, нужно указать её
        time.sleep(3)
        self.send_email(addr_to, "Test of email reader 2", "", files)
        driver = self.get_driver_Chrom()
        self.go_to_main_page(driver)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//a[starts-with(@class, "llc ")][1]'))).click()
        header = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//h2[@class="thread-subject"]')))
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[@data-name="download-link"]'))).click()
        time.sleep(3)

        with open("C:\\Users\\march\\Downloads\\Telegram Desktop\\photo_2023-01-15_23-49-55.jpg", "rb") as file1:
            with open("C:\\Users\\march\\Downloads\\photo_2023-01-15_23-49-55.jpg", "rb") as file2:
                self.assertEqual(header.text, 'Test of email reader 2')
                self.assertEqual(file1.read(), file2.read())

    def test_email_reader_with_file(self):
        addr_to = "witchxxxch12@mail.ru"  # Получатель
        files = ["C:\\Users\\march\\Downloads\\Telegram Desktop\\NuT (2).pptx"]  # Если нужно отправить все файлы из заданной папки, нужно указать её
        self.send_email(addr_to, "Test of email reader 3", "", files)
        time.sleep(3)

        driver = self.get_driver_Chrom()
        self.go_to_main_page(driver)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//a[starts-with(@class, "llc ")][1]'))).click()
        header = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//h2[@class="thread-subject"]')))
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[@data-name="download-link"]'))).click()
        time.sleep(3)

        with open("C:\\Users\\march\\Downloads\\Telegram Desktop\\NuT (2).pptx", "rb") as file1:
            with open("C:\\Users\\march\\Downloads\\NuT (2).pptx", "rb") as file2:
                self.assertEqual(header.text, 'Test of email reader 3')
                self.assertEqual(file1.read(), file2.read())


    def test_email_reader_with_files(self):
        addr_to = "witchxxxch12@mail.ru"  # Получатель
        files = ["C:\\Users\\march\\PycharmProjects\\GmailTest\\content\\photo_2023-01-15_23-49-55.jpg",
                 "C:\\Users\\march\\Downloads\\Telegram Desktop\\NuT (2).pptx"]
        self.send_email(addr_to, "Test of email reader 4", "", files)
        time.sleep(3)

        driver = self.get_driver_Chrom()
        self.go_to_main_page(driver)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//a[starts-with(@class, "llc ")][1]'))).click()
        header = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//h2[@class="thread-subject"]')))#; time.sleep(1000)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located(
                (By.XPATH, '(//a[@data-test-id="download"])[1]'))).click()
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located(
                (By.XPATH, '(//a[@data-test-id="download"])[2]'))).click()

        time.sleep(3)

        for elem in ["photo_2023-01-15_23-49-55.jpg", "NuT (2).pptx"]:
            with open("C:\\Users\\march\\Downloads\\Telegram Desktop\\" + elem, "rb") as file1:
                with open("C:\\Users\\march\\PycharmProjects\\GmailTest\\content\\" + elem, "rb") as file2:
                    self.assertEqual(header.text, 'Test of email reader 4')
                    self.assertEqual(file1.read(), file2.read())

    def test_email_reader_num_of_mails(self):
        driver = self.get_driver_Chrom()
        self.go_to_main_page(driver)
        elem = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="nav-folders"]//a[starts-with(@title, "Входящие,")]')))
        header = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, '//h2[@class="thread-subject"]')))#; time.sleep(1000)
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located(
                (By.XPATH, '(//a[@data-test-id="download"])[1]'))).click()
        WebDriverWait(driver, 6).until(
            EC.presence_of_element_located(
                (By.XPATH, '(//a[@data-test-id="download"])[2]'))).click()

        time.sleep(3)

        for elem in ["photo_2023-01-15_23-49-55.jpg", "NuT (2).pptx"]:
            with open("C:\\Users\\march\\Downloads\\Telegram Desktop\\" + elem, "rb") as file1:
                with open("C:\\Users\\march\\PycharmProjects\\GmailTest\\content\\" + elem, "rb") as file2:
                    self.assertEqual(header.text, 'Test of email reader 4')
                    self.assertEqual(file1.read(), file2.read())
