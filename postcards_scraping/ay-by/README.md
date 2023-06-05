[Аукционы Беларуси Ay-by](http://ay.by/)

Сбор открыток одного продавца:

1. `scraping_urls_seller.py` - сбор url индивидуальных страниц открыток со [страницы продавца](http://ay.by/whoiswho.phtml?id=6479956&topic=1102916) (отдельно открытки и почтовые карточки)
2. `scraping_photos.py` - скачивание открыток с индивидуальных страниц ([пример страницы](http://ay.by/lot/sssr-dmpk-1968-s-prazdnikom-moskva-krasnaya-ploschad-5028508937.html))

Сбор всех открыток с сайта:

1. `scraping_urls_all.py` - сбор url индивидуальных страниц открыток с [главной страницы](http://collect.ay.by/otkrytki-konverty-kalendari/otkrytki/do-1990/))
2. `drop_duplicates.py` - удаление из получившейся базы открыток, которые уже были скачаны при сборе у конкретного продавца
2. `scraping_photos.py` - скачивание открыток с индивидуальных страниц ([пример страницы](http://ay.by/lot/sssr-dmpk-1968-s-prazdnikom-moskva-krasnaya-ploschad-5028508937.html))

Исключения пишутся в `exceptions.txt`.