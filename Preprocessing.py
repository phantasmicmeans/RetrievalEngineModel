from konlpy.tag import Twitter
import xml.etree.ElementTree as ET
import sqlite3

twitter=Twitter()

def ConnectDB():
    global cur
    global conn
    conn=sqlite3.connect("test.db")
    cur=conn.cursor()

def ParseFile(docpath):
    query="insert into Textdb (title,content) values(?,?);"
    result=""

    for i in range(2,3):
        document=ET.parse(docpath+str(i)+".xml")
        root=document.getroot()
        for doc in root.iter("DOC"):
            title=doc.findtext("TITLE")
            text=doc.findtext('TEXT')
            cur.execute(query,(title,text))
    conn.commit()
#res=title+text
#            result+=res
        
#    return list(set(twitter.morphs(result)))

def makeVoc(twitterList): #dictionary 
    with open("TwitterVoc.voc",'w') as wf:
        for w in twitterList:
            wf.write(w+'\n')

def Voc_doc():
    voc_list=[]
    global cur
    query="select id,title,content from textdb where id <=10;"
    cur.execute(query)

    rows=cur.fetchall()
    for row in rows:
        twitter_title=twitter.morphs(row[0])
        twitter_text=twitter.morphs(row[1])
        voc_list=twitter_text
        make_dict(voc_list)
    
    print("print_dict_input:",dict_input)
    print("print_voc_dict:",voc_dict)
    

def make_dict(content):

    count=0
    indexcount=0
    dict_list={}
    final_dict_list={}

    for word in content:
        count+=1
        dict_list[count]=word
     
    count=0

    for k in dict_list.keys():
        indexcount=0
        word=dict_list.get(k)
        for j in dict_list.keys():
            if word == dict_list.get(j):
                indexcount+=1
                
        count+=1
        final_dict_list[count]=[indexcount,word]
    
    
    return delete_overlap(final_dict_list)

def delete_overlap(final_dict_list):
    
    delete_list=[]
    for k in final_dict_list.keys():
        word=final_dict_list.get(k)
        for j in {key for key in final_dict_list}:
            if(j>k):
                word2=final_dict_list.get(j)
                if word==word2:
                    delete_list.append(j)
    
    #print("delete",list(set(delete_list)))
    for index in list(set(delete_list)):
        del final_dict_list[index]
    
    #print("fina",final_dict_list)
    return final_dict_list

def Build_voc(content):

    return list(set(twitter.morphs(content)))

def closeDB():
    global cur
    global conn 
    cur.close()
    conn.close()

def main():
    ConnectDB()
    #result=ParseFile("textdata/")
    user_input=input()
    Voc_doc(input) #사용자 입력 받고 그거랑 비교할거임.


    closeDB()
    
if __name__=="__main__":
    main()
