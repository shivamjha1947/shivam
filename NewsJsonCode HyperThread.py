import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json
import threading

#Recource Declaration
my_url = 'https://www.thehindu.com/sci-tech/technology/?page=1'

#global resources
string=''
pageno=[]
l1=[];l2=[];l3=[]
paragraphs=[]

#holder for thread data
threadsync=[[],[],[],[],[],[],]

#Page index generator
for i in range (0,216):
    string='https://www.thehindu.com/sci-tech/technology/?page='+str(i+1)
    pageno.append(string)

#gets page 1 to n and their contents
def worker(a,b,t_index):
    locallist1=[]
    locallist2=[]
    locallist3=[]
    localpara =[]

    for j in range( a,b):

        
        #get soup in html format of current page index
        page_soup = soup(uReq(pageno[j]).read(),"html.parser")
        headings=page_soup.findAll("h3") 
        
        #Headings and relavant content Scanner for current page index and store in list
        for i in range (14,len(page_soup.findAll("h3"))):   
            #error and exception handler block
            try:
                locallist1.append(headings[i].text)
                locallist2.append(headings[i].a['title'])
                locallist3.append(headings[i].a['href'])
                
                
            except:
                print("entry",i,'of page',j,'not found');
                locallist1.append('entry not found');
                locallist2.append('entry not found');
                locallist3.append('entry not found');

        
        for k in range(len(locallist3)-30):
            lest=''
            try: 
                link_soup=soup(uReq(locallist3[k]).read(),"html.parser")
                container=link_soup.find_all('p');
                for l in range(len(container)-8):
                    lest=lest+container[l].text
                localpara.append(lest)

                print('acqiusition fraction',( k*100/len(locallist3) ) )
            except :
                print('error')
                localpara.append('couldnt find the paragraph')
                    




    #join and merge resources with main

    threadsync[t_index].append(locallist1)
    threadsync[t_index].append(locallist2)
    threadsync[t_index].append(locallist3)
    threadsync[t_index].append(localpara)


#Thread Parallalisation block
thread_man=[]
page_multiplier=1
parallelcount=6
for t in range(parallelcount):
    thread_man.append(threading.Thread(target=worker, args=  (t*page_multiplier, (t+1)*page_multiplier ,t)))
    thread_man[t].start()

#thread joiner loop
thread_man[0].join()
thread_man[1].join()
thread_man[2].join()
thread_man[3].join()
thread_man[4].join()
thread_man[5].join()


for stitch in range(len(threadsync)):
    l1.extend(threadsync[stitch][0])
    l2.extend(threadsync[stitch][1])
    l3.extend(threadsync[stitch][2])
    paragraphs.extend(threadsync[stitch][3])

print (len(l1),len(l2),len(l3),len(paragraphs))



#t2.start()
#t2.join()


#t3.start()
#t3.join()
#t4.start()
#t4.join()

#\n correction  for list 1 to increase readability
lst1=[]
for i in range(len(l1)):
    lst1.append(l1[i].replace('\n',''))

#storing in JSON Usable Dictonary

allinfo={'titles':lst1,
         'date':l2,
         'links':l3,
         'paragraphs':paragraphs }


#OPTIONAL
print(json.dumps(allinfo,indent=4))

#print(threadsync)

with open('alldatathreaded.json','w') as f1:
    json.dump(allinfo,f1,indent=4 )


