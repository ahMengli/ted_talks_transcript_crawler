'''
Created on Apr 9, 2016

@author: mmli
'''
import urllib2
#import BeautifulSoup
import sys
from bs4 import BeautifulSoup

def ted_talks_crawler(src_url):
    
    talk_text = ''
    resp = urllib2.urlopen(src_url)
    web_src = resp.read().replace('\r','').replace('\n', '')
    text_seg = BeautifulSoup(web_src, 'lxml')
    spans = text_seg.find_all("span", class_= "talk-transcript__fragment")
    for ws in spans:
        parsed_html = BeautifulSoup(str(ws), 'lxml')
        text = parsed_html.get_text()
        talk_text = talk_text + text + ' '
        
    return talk_text

def get_url_from_topic(topic_url):
    
    links = []
    host = 'http://www.ted.com'
    resp = urllib2.urlopen(topic_url)
    web_src = resp.read().replace('\r','').replace('\n', '')
    text_seg = BeautifulSoup(web_src, 'lxml')
    spans = text_seg.find_all("a", class_= "playlist-talks__play")
    for ws in spans:
        ws = host + ws.get('href')
        if ws not in links:
            links.append(ws)
    return links

def get_trans(url_links):
    
    trans = '/transcript?language=en'
    trans_url = []
    for url in url_links:
        trans_url.append(url + trans)
    return trans_url

def get_topic_from_playlist(playlist_url):
    
    links = []
    host = 'http://www.ted.com'
    resp = urllib2.urlopen(playlist_url)
    web_src = resp.read().replace('\r','').replace('\n', '')
    
    p1 = web_src.find(r'<script>q("index.init"')
    p2 = web_src.find(r'<script>q("browse.init"')
    plists = web_src[p1+len(r'<script>q("index.init"'):p2]
    ps = plists.split(',')
    for item in ps:
        if item.find(r'"url"') <> -1:
            item_pos = item.find(r'"}')
            url = item[7:item_pos] 
            links.append(url)
    return links
            
if __name__ == '__main__':
    
    #src_url = 'https://www.ted.com/talks/lorrie_faith_cranor_what_s_wrong_with_your_pa_w0rd/transcript?language=en'
    #text = ted_talks_crawler(src_url)
    #print text
    playlist_url = 'http://www.ted.com/playlists'
    topic_list = get_topic_from_playlist(playlist_url)
    flag = False
    for topic_url in topic_list:
        print topic_url
        if topic_url.find('9_trippy_ted_talks') <> -1:
            flag = True
        if not flag:
            continue
        #topic_url = 'http://www.ted.com/playlists/10/who_are_the_hackers'
        file_saved = '/Users/mmli/Downloads/speeches_of_ted.txt'
        url_links = get_url_from_topic(topic_url)
        url_trans = get_trans(url_links)
        speeches = []
        for url in url_trans:
            print url
            try:
                speech = ted_talks_crawler(url)
            except:
                print 'url open time out, skip ...'
                continue
            print len(speech)
            if url.find('amy_webb_how_i_hacked_online_dating') <> -1:
                print speech
                print '-----'
                print speech[15432:15436]
            speeches.append(speech)
        f = open(file_saved, 'a')
        for s in speeches:
            f.write(s.encode('ascii', 'ignore').decode('ascii') + '\n\n')
        f.close()
        