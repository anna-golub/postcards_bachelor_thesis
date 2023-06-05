[Филателистическая студия Игоря Пугачева](http://pugachev-studio.ru/)

Сбор всех открыток с сайта:

1. `scraping_categories.py` - сбор списка категорий и их url с [главной страницы](http://pugachev-studio.ru/index.php?categoryID=8)
2. `scraping_product_ids.py` - сбор ID открыток со страниц категорий ([пример страницы](http://pugachev-studio.ru/index.php?categoryID=12)). ID используются для формирования url индивидуальных страниц открыток ([пример страницы](http://pugachev-studio.ru/index.php?productID=18830))
3. `scraping_photos.py` - скачивание открыток с индивидуальных страниц
4. `scraping_correction.py` - удаление битых файлов JPEG среди скачанных сканов открыток. Они появляются в случаях, когда на сайте только один скан.

Исключения пишутся в `exceptions.txt`.