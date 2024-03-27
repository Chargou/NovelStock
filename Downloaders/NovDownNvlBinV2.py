import re
from datetime import date
import urllib.request
from toolbox import *

REGEX_CHAPTER_HTML = re.compile(r"0%; margin-top: 15px;\" >(.*)<hr class=\"chr-end\">", re.MULTILINE) #Extracts chapter html from page html
REGEX_NEXT_CHAPTER_LINK = re.compile(r"href=\"([^\"]*)\" class=\"btn btn-success\" id=\"next", re.MULTILINE) #Extracts next chapter's link from //
REGEX_CHAPTER_NUMBER = re.compile(r"/c+hapter-(\d+)") #Extracts chapter number from chapter link
REGEX_AD_REMOVER = re.compile(r"<div id=\"[^\"]*\"><script>window\.pubfuturetag = window\.pubfuturetag \|\| \[];window\.pubfuturetag\.push\({unit: \"[^\"]*\", id: \"[^\"]*\"}\)</script></div>", re.MULTILINE)

file_header = "<!DOCTYPE html> <html> <body style=\"background-color:#242526;color:#FFFDD0;margin:0px 350px\"><a href=\"#ChapterNumber\"><h1>Jump to chapter</h1></a>"
file_closer = "</body> </html>"

def textify(bytes):
    return bytes.read().decode('utf-8').encode('cp1252','replace').decode('cp1252')

def ua(): #returns a somewhat randomified user agent
    return {'User-Agent': 'M'+"abcdefghijklmnopqrstuvwxyz"[entier_aleatoire(25)]+'zilla/6.0 (Macintosh; Intel Mac OS X-'+"abcdefghijklmnopqrstuvwxyz"[entier_aleatoire(25)]+' 10_9_3) Ap'+"abcdefghijklmnopqrstuvwxyz"[entier_aleatoire(25)]+'leWebKit/537.36 (KHTML, like Gecko) '+"abcdefghijklmnopqrstuvwxyz"[entier_aleatoire(25)]+'hrome/35.0.1916.47 Safari/537.'+str(entier_aleatoire(10, 4000))}

def saveto(content, filename, extension=".html"): #Will create file if it doesn't exist
    f = open(filename+extension, "w")             #!!! Will overwrite data if file already exists !!!
    f.write(content)
    f.close()

def openlink(link): #returns byte representation of page linked
    return urllib.request.urlopen(urllib.request.Request(link, data=None, headers=ua()))

def process_match(match):
    if match:
        return match[1]
    return None 

def ch_head(chapter_link):
    chapter_number = process_match(REGEX_CHAPTER_NUMBER.search(chapter_link)) 
    return f"<a id=\"{chapter_number}\" href=\"{chapter_link}\" target=\"_blank\"><small>Chapter {chapter_number}</small></a>"

def getpage(link):
    p = openlink(link)
    p = textify(p)
    p = " ".join(p.split())
    p = remove_ads(p)
    return p

def remove_ads(page):
    return REGEX_AD_REMOVER.sub(" ", page)

def get_novel_chapter(chapter_link):
    """return html of a single chapter and the next chapter's url (both in string format)
    if no next chapter, returns None instead of next chapter's link"""
    p = getpage(chapter_link)
    chapter_html = ch_head(chapter_link)+process_match(REGEX_CHAPTER_HTML.search(p))
    next_chapter_link = process_match(REGEX_NEXT_CHAPTER_LINK.search(p))
    print("Chapter done: "+chapter_link)
    return chapter_html, next_chapter_link

def download_novel_from_chapter(chapter_link, filename="Unnamed"):
    """download entire novel starting from said chapter"""
    last_problem = "None yet"
    chapters_html = file_header
    counter = 0
    while chapter_link:
        try:
            chapter_html, chapter_link = get_novel_chapter(chapter_link)
            chapters_html += chapter_html
            counter += 1
        except Exception as e:
            if last_problem == chapter_link:
                print(e)
                print(f"had 2 problems in a row with \n {chapter_link}")
                exit()
            last_problem = chapter_html
            saveto(chapters_html+file_closer, filename)
            print(f"\n\n\n\n\n!!!!!!!!!!!!! Problem at \n{chapter_link} !!!!!!!!!!!!!\n\n\n\n\n")
            attendre(5000)
    chapters_html += file_closer
    saveto(chapters_html, filename)
    print(f"FINISHED ! ({counter} chapters downloaded)")

def download_novel(novel_link, filename="Unnamed"):
    pass

todayte = date.today().strftime("%d-%m-%Y")

download_novel_from_chapter("https://novelbin.novel-online.org/novel/the-nebulas-civilization/cchapter-1-practice-game-until-now", "The_Nebulas'-Civilization_"+todayte)
