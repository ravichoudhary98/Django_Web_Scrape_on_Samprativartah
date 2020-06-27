from django.shortcuts import render
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup as soup
from pathlib import Path

def button(request):
    return render(request, 'home.html')

def San_text(request):
    
    values = []
    
    url = [request.POST.get("param")]
          
    for i in range(len(url)):
    
        data = requests.get(url[i])
    
        html = soup(data.text, 'html.parser')
        values += [div.text.strip() for div in html.find_all('div', { 'class': 'post-body entry-content'},{'style':'text-align:center'})]
    l1 = []
    l2 = []
    data = []
    title = []
    body = []
    df = pd.DataFrame()
    for i in range(len(values)):
    
        data = re.findall(r".*", values[i])
        while("" in data) : 
            data.remove("")
        if len(data)>=2:
            l1 = data[0]
            l2 = data[1:]
        title += [l1];
        body += [l2];
    df=pd.DataFrame(list(zip(title, body)), columns =['title', 'body'])

    df['title']=df["title"].apply(lambda x: ",".join(x) if isinstance(x, list) else x)
    df['body']=df["body"].apply(lambda x: ",".join(x) if isinstance(x, list) else x)
    df['body'][2]
    j=30000

    for i in range(len(df)):
        title = df['title'][i]
        body = df['body'][i]+'\n'
        home = str(Path.home())
        filename = home + '/Downloads/'+ str(j) +'.trec.txt'
        file = open(filename, 'w')
        file.write("<DOC>\n")
        file.write("<DOCNO>")
        file.write(str(j))
        j=j+1
        file.write("<\DOCNO>\n")
        file.write("<HEAD>")
        file.write(title)
        file.write("<\HEAD>\n")
        file.write("<BODY>\n")
        file.write(body)
        file.write("<\BODY>\n")
        file.write("<\DOC>\n")
        file.close()
    inp1 = "Data saved to Your DOwnloads Folder."
    return render(request,'output.html',{'data1':inp1})
