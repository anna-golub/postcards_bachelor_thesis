# Bachelor's thesis by Anna Golub

**Anna Golub**  
Thesis topic: **Automation of a digital postcard database's growth and quality control**  
Intellectual Systems in the Humanitarian Sphere (Bachelor)  
ITMO University, St. Petersburg, Russia  

## Introduction
In preparation of my bachelor’s thesis, I worked as a process automation lead at Pishu Tebe (en. Writing to You) . Pishu tebe is a volunteer-based project aimed at creating a digital corpus of transcribed postcards. In my role as process automation lead, I introduced multiple computerized shortcuts to the tedious manual work on the postcard corpus, which have significantly accelerated the growth of the corpus in size and helped ensure its quality. I describe my contribution in detail below .

## Database Growth
Firstly, Pishu tebe is always in need of new postcard scans: they make up the content of the corpus together with their transcriptions (those include the message from the back of the postcard, send and receive dates, addressee and addresser’s names, etc.) New postcards come in from private collections and museums, but also, for the most part, from collector’s marketplaces and stores online. I wrote a script that allows to automatically scrape postcard scans from open sources on the Internet. From September 2022 to April 2023, using the parser, I scraped almost 240,000 postcards, about 20,000 of which have so far been added to the corpus and transcribed. Such scale would not have been possible without an automated scraping tool.

## Quality Control
Next, a task of high importance is postcard deduplication. It is a crucial step towards ensuring that the data of the corpus is clean and time-consuming manual transcription work will not be done twice on the same postcard. I developed an algorithm which identifies similar postcard scans based on their hash values. For the last 6 months, the algorithm has been utilized to identify duplicates among new additions to the corpus, and thus roughly 800 duplicates have been filtered out.

Furthermore, many scans entering the corpus have large margin, which needs to be cropped for high image quality. I have tested three different automatic cropping methods (an OpenCV-based document scanner, a photo background removal package and an original method by a Pishu tebe colleague) and developed a postcard cropping algorithm that uses all three of them. Despite general high quality of the results, unfortunately, they have to be checked manually, for which Pishu tebe does not have staff. Therefore, the algorithm is currently being improved and will be implemented after a new round of testing.

## Research Corpus
Finally, the postcard corpus is primarily a resource of data for historical and linguistic research. To facilitate researchers’ access to the corpus, I wrote a program for data preparation and preprocessing (for example, unified formatting of dates). My work has allowed historians and linguists to begin working with the postcard corpus and avoid dealing with formatting mistakes.

## Conclusion
To summarize, I have made a worthwhile contribution to the Pishu tebe project. I have automated the scraping of postcards from the web, their deduplication, the cropping of the margin on the scans and the preparation of the corpus for postcard researchers. I presented the work described above as a bachelor’s thesis, which has been regarded highly by the defense committee.
