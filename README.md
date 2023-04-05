# ***JD_sl Bot***
## Телеграм-бот написанный на ***PyTelegramBotAPI***.

Собирает товары со скидками с сайта https://www.global.jdsports.com с заранее заданными фильтрами товаров.

# Functions
* Запись данных в ***JSON***:
  * перезапись существующих файлов;
  * архив старых файлов.
* Анализ собранных данных с предыдущим набором данных;
* Вывод товаров:
  * полным набором, которые соответствуют условию;
  * которые отсутствуют в предыдущем наборе;
  * цена которых изменилась.
* Проверка на наличие новых товаров на сайте;
* Планировщик некотрых функций реализованный при помощи ***apscheduler***;
* ~~Асинхронный тайм-аут парсера~~.

# In progress:
* Выбор двух файлов из архива и актуального набора для сравнения 
