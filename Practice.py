from konlpy.tag import Twitter
import xml.etree.ElementTree as ET
import sqlite3
import math

twitter=Twitter()

def ConnectDB():
    global cur
    global conn
    conn=sqlite3.connect("test.db")
    cur=conn.cursor()
    
def closeDB():
    global cur
    global conn 
    cur.close()
    conn.close()
    
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

    

def Voc_doc(input):
    
    dict_input=make_dict(twitter.morphs(input))
    #print(dict_input)
    voc_list=[]
    voc_dict=[]
    doc_list=[]
    global cur
    query="select id,title,content from textdb where id <=3;"
    cur.execute(query)
    
    rows=cur.fetchall()
    for row in rows:
        twitter_title=twitter.morphs(row[1])
        twitter_text=twitter.morphs(row[2])
        voc_list=twitter_text
        voc_dict=make_dict(voc_list)
        doc_list.append(voc_dict)
    
    #print("doc_list:" ,doc_list)
    #print("print_dict_input:" ,dict_input)
    #print("print_voc_dict:",voc_dict)

    return makeQueryNorm(dict_input) , makeDocNorm(doc_list)
    
        
def make_dict(content):
    #cotent가 리스트임. ['ㅁ','asds','dsfdf,'asd']
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
    
    return final_dict_list

def makeQueryNorm(dict_input):
    
    word_vec=[]
    Length=1

    for k in dict_input.keys():
        word_vec.extend([dict_input.get(k)])
    #print('word_vec:',word_vec)
    
    for _list in word_vec:
        Length+=math.pow(_list[0],2)
    
    #print("%.3f" %d math.sqrt(Length),4)
    
    return round(math.sqrt(Length),4)

def makeDocNorm(doc_list):
    
    word_vec=[]
    word_list=[]
    Length=1
    TotalDoc=DocCount()
    idf_List=countDoc(doc_list)#idf 역문서 빈도 벡터
    
    for _dict in doc_list:
        word_vec=[]
        for _list in _dict.keys():
            word_vec.extend([_dict.get(_list)])
        word_list.append(word_vec)
    
    
    for _index in range(len(word_vec)):
        count=0
        Legth+= word_vec[_index][0] * math.log10(TotalDoc/idf_List[_index][++count])

    
def countDoc(doc_list):
    
    doc_list_copy=doc_list
    count_List=[]
    count=0
    for _Dict in doc_list_copy:
        count=0
        count_list=[]
        for K in _Dict.keys():
            count=0
            #print("Dict:" , _Dict)
            #print("\n")
            word=_Dict.get(K)
            #print(word)
            for _dict in doc_list : #위에서 안한 리스트로만 해야한다
                if(_Dict!=_dict):
                    for k in _dict.keys():
                        word2=_dict.get(k)
                        if(word[1]==word2[1]):
             #               print("_dict : ")
             #               print(_dict)
             #               print("Word and Word2",word,word2)
                            count+=1
                            break
                    count_list.extend(str(count))
        count_List.append(count_list)
        #for ele in count_List:
        #    print("count: ")
        #    print(ele)

        #print()
                
    return count_list

def DocCount():
    
    global cur
    query="select count(*) from Textdb;"
    cur.execute(query)
    rows=cur.fetchall()
    DocCount=0
    
    for row in rows:
        DocCount=row[0]
        
    return DocCount
    
def CosineSimirarity(dict_input,voc_dic):
    
    input_length=makeNorm(dict_input)
    doc_length=make_Norm(voc_dic)
    
    

def main():
    ConnectDB()
    user_input=input()
    ParseFile("textdata/")
    length1,length2 =Voc_doc(user_input)
    print("length1: ",length1)
    print("length2: ",length2)
    closeDB()
    
    
    
    #ParseFile("textdata/")
    #ConnectDB()
    #result=ParseFile("textdata/")
    #makeVoc(result)
    
    #print(result)
    
if __name__=="__main__":
    main()
 
