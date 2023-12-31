import urllib.request
import re
from toolbox import *
from datetime import date

REGEX_CHAPTER_HTML = re.compile(r"<div id=\"chapter-container\" class=\"chapter-content\" itemprop=\"description\">\n(.*)\n</div>\n<div class=\"chapternav skiptranslate\">", re.MULTILINE | re.DOTALL)
REGEX_NEXT_CHAPTER_LINK = re.compile(r"<a rel=\"next\" class=\"button nextchap \" href=\"/novel/([^\"]*)", re.MULTILINE)
REGEX_CHAPTER_NUMBER = re.compile(r"/chapter-(\d*)")

def ecrire(contenu, nom_fichier, extension=".html"):
    f = open(nom_fichier+extension, "w")
    f.write(contenu)
    f.close()

def get_novel_chapter(chapter_link):
    """return html of a single chapter and the next chapter's url (both in string format)
    if no next chapter, returns None instead of next chapter's link"""
    p = urllib.request.urlopen(urllib.request.Request(chapter_link, data=None, headers={'User-Agent': 'M'+"abcdefghijklmnopqrstuvwxyz"[entier_aleatoire(25)]+'zilla/6.0 (Macintosh; Intel Mac OS X-'+"abcdefghijklmnopqrstuvwxyz"[entier_aleatoire(25)]+' 10_9_3) Ap'+"abcdefghijklmnopqrstuvwxyz"[entier_aleatoire(25)]+'leWebKit/537.36 (KHTML, like Gecko) '+"abcdefghijklmnopqrstuvwxyz"[entier_aleatoire(25)]+'hrome/35.0.1916.47 Safari/537.'+str(entier_aleatoire(10, 4000))}))
    p = p.read().decode('utf-8').encode('cp1252','replace').decode('cp1252') #code is ugly but it works (somewhat)
    chapter_number = REGEX_CHAPTER_NUMBER.search(chapter_link).group(1)
    chapter_html = f"<a id=\"{chapter_number}\" href=\"{chapter_link}\" target=\"_blank\"><small>Chapter {chapter_number}</small></a>"+re.sub("<div class=[^>]*></div>", "", REGEX_CHAPTER_HTML.search(p).group(1), re.MULTILINE)
    next = REGEX_NEXT_CHAPTER_LINK.search(p)
    if next:
        next_chapter_link = "https://www.lightnovelpub.com/novel/"+next.group(1)
    else:
        next_chapter_link = None
    print("Chapter done: "+chapter_link)
    return chapter_html, next_chapter_link

def download_novel_from_chapter(chapter_link, filename): ### To be rewritten
    """download entire novel starting from said chapter"""
    last_problem="no problems yet"
    chapters_html = "<!DOCTYPE html> <html> <body style=\"background-color:#242526;color:#FFFDD0;margin:0px 350px\"><a href=\"#ChapterNumber\"><h1>Jump to chapter</h1></a>"
    while chapter_link:
        try:
            chapter_html, chapter_link = get_novel_chapter(chapter_link)
            chapters_html += chapter_html
        except:
            if chapter_link==last_problem:
                print("had 2 problems in a row with "+chapter_link)
                exit()
            ecrire(chapters_html+"</body> </html>", filename)
            print("\n\n\n\n\nPROBLEM !!!!!!!!!!!!!!!!!!!! \n(at chapter "+chapter_link+" )\n\n\n\n\n")
            last_problem = chapter_link
            attendre(5000)
    chapters_html += "</body> </html>"
    ecrire(chapters_html, filename)

def download_novel(novel_link, filename="Unnamed"):
    """download entire novel, starting from ch 1"""
    p = urllib.request.urlopen(urllib.request.Request(novel_link, data=None, headers={'User-Agent': 'Mozilla/6.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.'+str(entier_aleatoire(10, 400))}))
    p = p.read().decode()#.encode('cp1252','replace').decode('cp1252') #code is ugly but it works (somewhat)
    groups = re.findall("<a id=\"readchapterbtn\" class=\"button\" href=\"/novel/([^\"]*)\"", p)
    chapter_link = "https://www.lightnovelpub.com/novel/"+groups[0]
    download_novel_from_chapter(chapter_link, filename)

todayte = date.today().strftime("%d-%m-%Y")

#download_novel("https://www.lightnovelpub.com/novel/dragon-monarch-system-16091349", "Dragon-monarch-system_"+todayte)
