import imaplib
import email
from email.header import decode_header
import base64
import mail_config

# Параметры для подключения к почтовому серверу

mail_pass = mail_config.mail_pass
username = mail_config.username


def parsing_list_unseen_email(unseen_emails: str):
    """
    Функция принимает на вход строку непрочитанных писем и возвращает список ID таких писем
    :param unseen_emails: объект, который содержит непрочитанные письма
    :return: список ID непрочитанных писем
    """

    lst_id_unseen_emails = []
    digit_char = ''
    for i in range(len(unseen_emails)):
        if unseen_emails[i].isdigit():
            digit_char += unseen_emails[i]
        else:
            if digit_char != '':
                lst_id_unseen_emails.append(digit_char)
                digit_char = ''
    lst_id_unseen_emails.append(digit_char)
    lst_id_unseen_emails.pop()
    return lst_id_unseen_emails


def parsing_list_unseen_email_to_bytes(unseen_emails: str):
    """
    Функция принимает на вход строку непрочитанных писем и возвращает список ID таких писем
    :param unseen_emails: объект, который содержит непрочитанные письма
    :return: список ID непрочитанных писем
    """

    lst_id_unseen_emails = []
    digit_char = ''
    for i in range(len(unseen_emails)):
        if unseen_emails[i].isdigit():
            digit_char += f"b'{unseen_emails[i]}"
        else:
            if digit_char != '':
                lst_id_unseen_emails.append(digit_char)
                digit_char = ''
    lst_id_unseen_emails.append(digit_char)
    lst_id_unseen_emails.pop()
    return lst_id_unseen_emails


def extract_multipart(msg):
    """
    Функция принимает на вход тело письма и говорит, есть ли вложенность письма
    :return: Записывает тело письма в файл D:/Mail_read_files/email_body.txt
    """
    if msg.is_multipart():
        with open('D:/Mail_read_files/email_body.txt', 'w', encoding='utf-8') as f:
            for part in msg.walk():
                if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'html':
                    f.write(base64.b64decode(part.get_payload()).decode())
            print('[INFO] Файл email_body.txt создан')
    else:
        body = base64.b64decode(msg.get_payload()).decode('utf-8')  # тело (содержимое) письма
        with open('D:/Mail_read_files/email_body.txt', 'w', encoding='utf-8') as f:
            f.write(body)
            print('[INFO] Файл email_body.txt создан')


# Блок 1 - подключение к почтовому серверу и получение списка непрочитанных писем

imap_server = "imap.mail.ru"
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, mail_pass)
imap.select("INBOX")  # выбор папки Входящие в почте
unseen_mails = imap.search(None, 'UNSEEN')  # поиск непрочитанных писем
unseen_mails_str = str(unseen_mails[1])

print('Непрочитанные письма: ',
      parsing_list_unseen_email(unseen_mails_str))  # формирование списка непрочитанных писем

res, msg = imap.fetch(b'3123', '(RFC822)')  # Для метода search по порядковому номеру письма
msg = email.message_from_bytes(msg[0][1])
print('\nЗаголовок письма:\n', decode_header(msg["Subject"])[0][0].decode(), '\n')  # чтение заголовка письма

extract_multipart(msg)
