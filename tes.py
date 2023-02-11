import os
import main
import arrow
# scr = main.return_html('https://www.global.jdsports.com/men/brand/adidas-originals,nike,the-north-face,polo-ralph-lauren,jordan,champion,new-balance,napapijri/sale/?jd_sort_order=price-low-high&max=204')

# def write_html():
#     with open ('in.html', 'w', encoding='utf-8') as file:
#         file.write(scr.text)
#         print('File writed!')

# data = arrow.utcnow().format('HH:mm:ss')
# print(data)

def change_json_name(path, new_file, was_file):
    file_path = os.path.join(path, new_file)
    if os.path.isfile(file_path):
        new_file_path = os.path.join(path, was_file)
        old_data = os.path.join(path,'old_dat')
        if not os.path.isdir(old_data):
            os.mkdir(old_data)
        os.rename(new_file_path, os.path.join(old_data, was_file))
        os.rename(file_path, new_file_path)
    else:
        print('No file for change')

# change_json_name('json_data', 'NEW_products.json', 'WAS_products.json') 
# os.mkdir(os.path.join('json_data','old_data'))

import asyncio
import time

async def fun1(x):
    print(x**2)
    await asyncio.sleep(3)
    print('fun1 завершена')

async def fun2(x):
    print(x**0.5)
    await asyncio.sleep(3)
    print('fun2 завершена')

async def main():
    task1 = asyncio.create_task(fun1(4))
    task2 = asyncio.create_task(fun2(4))

    await task1
    await task2

print(time.strftime('%X'))
asyncio.run(main())
print(time.strftime('%X'))