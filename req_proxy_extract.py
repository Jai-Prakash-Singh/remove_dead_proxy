from Queue import Queue
from threading import Thread
import time
import requests
from random import choice
import logging

num_fetch_threads = 50
enclosure_queue = Queue()

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',)


def main2(i, q):

    while True:
        pass_ip, link = q.get()
        
        pass_ip = pass_ip.strip()
        link = link.strip()

        http_proxy = "http://" + pass_ip
        proxyDict = {"http" : http_proxy}

        try:
            r = requests.get(link,  proxies=proxyDict)

            if r.status_code == requests.codes.ok:
                r.cookies.clear()
                r.close()
         
                f = open("mygoodproxy2.txt", "a+")
                print >>f, pass_ip
                f.close()
              
        except:
            pass

        time.sleep(2)
        q.task_done()


def main(link):
    #f = open("/home/user/Desktop/proxy_http_auth.txt")
    f = open("/home/user/mygoodproxy.txt")
    pass_ip_list = f.read().strip().split("\n")
    f.close()


    for i in range(num_fetch_threads):
        worker = Thread(target=main2, args=(i, enclosure_queue,))
        worker.setDaemon(True)
        worker.start()

    for l in pass_ip_list:
        enclosure_queue.put((l, link))


    print '*** Main thread waiting ***'
    enclosure_queue.join()
    print '*** Done ***'



if __name__=="__main__":
    link = "http://www.flipkart.com/bags-wallets-belts/bags/totes/pr?p[]=facets.ideal_for%255B%255D%3DWomen&p[]=sort%3Dpopularity&sid=reh%2Cihu%2Cv57&facetOrder[]=ideal_for&otracker=hp_nmenu_sub_women_0_Totes"
    main(link)
    #print page
    
        
    

