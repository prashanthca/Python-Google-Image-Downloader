# Python Google Image Downloader

import time 
import sys
import os
import urllib2 

search_keyword = []
keywords = []

def menu():
	version = (3,0)
	cur_version = sys.version_info
	if cur_version >= version:
		print("==== GOOGLE IMAGE DOWNLOADER ====\n\n")
		print("1. Download Images\n")
		print("2. Exit\n\n")
		choice = int(input("Enter Your Choice >> "))

		if choice == 1:
			key_word()
			user_searchterms()
			main()
		elif choice == 2:
			sys.exit(0)
		else:
			print("Invalid Input!")
			sys.exit(0)
	else:
		print "==== GOOGLE IMAGE DOWNLOADER ====\n\n"
		print "1. Download Images\n"
		print "2. Exit\n\n"
		choice = int(raw_input("Enter Your Choice >> "))

		if choice == 1:
			key_word()
			user_searchterms()
			main()
		elif choice == 2:
			sys.exit(0)
		else:
			print "Invalid Input"
			sys.exit(0)

def key_word():
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:
        try:
            word = str(input("Enter a keyword [EX: high resolution] >> "))
            keywords.append(word)
        except Exception as e:
            print(str(e))
    else:
        try:
            word = str(raw_input("Enter a keyword [EX: high resolution] >> "))
            keywords.append(word)
        except Exception as e:
            print "ERROR: Some error occured!"

def user_searchterms():
    version = (3,0) 
    cur_version = sys.version_info
    if cur_version >= version:
        try:
            maxterms = int(input("Enter Maximum Terms By You[EX: 1/2/3] >> ")) 
            maxlist = maxterms
            while len(search_keyword) < int(maxlist):
                item = str(input("Enter Your Item >> "))
                search_keyword.append(str(item))
        except Exception as e:
            print(str(e))
    else:
        try:
            maxterms = int(raw_input("Enter Maximum Terms By You[EX: 1/2/3] >> "))
            maxlist = maxterms
            while len(search_keyword) < int(maxlist):
                item = str(raw_input("Enter Your Items >> "))
                search_keyword.append(str(item))
        except Exception as e:
            print "ERROR: Exception Occured!"

def download_page(url):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:    
        import urllib.request    
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:                        
        import urllib2
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
            req = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:
            return"Page Not found"

def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content

def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)     
            time.sleep(0.1)        
            page = page[end_content:]
    return items


def main():
	t0 = time.time()  

	i= 0
	while i<len(search_keyword):
	    items = []
	    iteration = "Item no.: " + str(i+1) + " -->" + " Item name = " + str(search_keyword[i])
	    print (iteration)
	    print ("Evaluating...")
	    search_keywords = search_keyword[i]
	    search = search_keywords.replace(' ','%20')
	    
	    try:
	        os.makedirs(search_keywords)
	    except OSError, e:
	        if e.errno != 17:
	            raise   
	        pass
	   
	    j = 0
	    while j<len(keywords):
	        pure_keyword = keywords[j].replace(' ','%20')
	        url = 'https://www.google.com/search?q=' + search + pure_keyword + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
	        raw_html =  (download_page(url))
	        time.sleep(0.1)
	        items = items + (_images_get_all_items(raw_html))
	        j = j + 1
	    print ("Total Image Links = "+str(len(items)))
	    print ("\n")


	    
	    info = open('output.txt', 'a')        
	    info.write(str(i) + ': ' + str(search_keyword[i-1]) + ": " + str(items) + "\n\n\n")         
	    info.close()                            

	    t1 = time.time() 
	    total_time = t1-t0
	    print("Total time taken: "+str(total_time)+" Seconds")
	    print ("Starting Download...")

	    k=0
	    errorCount=0
	    while(k<len(items)):
	        from urllib2 import Request,urlopen
	        from urllib2 import URLError, HTTPError

	        try:
	            req = Request(items[k], headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
	            response = urlopen(req,None,15)
	            output_file = open(search_keywords+"/"+str(k+1)+".jpg",'wb')
	            
	            data = response.read()
	            output_file.write(data)
	            response.close();

	            print("completed ====> "+str(k+1))

	            k=k+1;

	        except IOError:

	            errorCount+=1
	            print("IOError on image "+str(k+1))
	            k=k+1;

	        except HTTPError as e:

	            errorCount+=1
	            print("HTTPError"+str(k))
	            k=k+1;
	        except URLError as e:

	            errorCount+=1
	            print("URLError "+str(k))
	            k=k+1;

	    i = i+1

	print("\n")
	print("Downloads Completed!")
	print("\n"+str(errorCount)+" ----> total Errors")
menu()