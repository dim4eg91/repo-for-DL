import pandas as pd

st = {}
product_name = []
count_and_price = []
count = []
price = []
total_price = []
od = []
shop = []


def transform_data_vkusvill():
    """
    Функция обработки письма от Vkusvill.
    Подобное письмо имеет свою уникальную структуру html - важно для парсера!
    :return:
    """
    with open(r'D:/Mail_read_files/email_body.txt', 'r', encoding='utf-8') as f:
        line = f.readline()  # считываем первую строку
        while line != '':  # пока не конец файла
            if 'АО "Вкусвилл"<br />' in line:
                shop_name = 'АО "Вкусвилл"'
                for i in range(14):
                    line = f.readline()
                order_date = line[:line.find('<')].strip()
            if 'width="40%"' in line:
                od.append(order_date)
                shop.append(shop_name)
                for i in range(2):
                    line = f.readline()
                    if ',кг' in line:
                        product = line[:line.find(',кг')].strip('[M] ')
                        product_name.append(product)
                    elif ',шт' in line:
                        product = line[:line.find(',шт')].strip('[M] ')
                        product_name.append(product)
                for i in range(2):
                    line = f.readline().replace(',', '.')
                price.append(float(line.strip()))
                for i in range(2):
                    line = f.readline().replace(',', '.')
                count.append(float(line.strip()))
                line = f.readline()
                a = line[line.find('top') + 5:line.find('colspan')]
                total_price.append(float((a[:a.find('<')]).replace(',', '.')))
            line = f.readline()


transform_data_vkusvill()

# with open('D:/Mail_read_files/email_body.txt', 'r', encoding='utf-8') as f:
#     line = f.readline()  # считываем первую строку
#     while line != '':  # пока не конец файла
#         if 'Приход' in line:
#             for i in range(3):
#                 line = f.readline()
#             order_date = line.strip()
#         if 'product-name' in line:
#             line = f.readline()
#             product_name.append(line.strip())
#             for i in range(5):
#                 line = f.readline()
#             count.append(func.parsing_quantity_and_price_per_one(line.strip())[0])
#             price.append(round(func.parsing_quantity_and_price_per_one(line.strip())[1], 2))
#             count_and_price.append(line.strip())
#             for i in range(8):
#                 line = f.readline()
#             total_price.append(line.strip())
#         line = f.readline()  # читаем новую строку


st.setdefault('product_name', product_name)
st.setdefault('count', count)
st.setdefault('price', price)
st.setdefault('total_price', total_price)
st.setdefault('order_date', od)
st.setdefault('shop_name', shop)

df = pd.DataFrame(st)
print(df)

# Трансформация - необходимо распарсить поле count_and_price. поле total_price сделать int
# df['total_price'] = df['total_price'].astype(float)
# print(df['total_price'].dtype)