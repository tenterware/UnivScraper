import os
from bs4 import BeautifulSoup

FILE_NAME = "face.html"
gDictFaceLink = {}

cmd = "wget http://web.humoruniv.com/board/humor/list.html?table=face -q -O " + FILE_NAME
#cmd = "http://web.humoruniv.com/board/humor/list.html?table=pdswait"
os.system(cmd)

fResult = open(FILE_NAME, 'r') 
txtResult = fResult.read() 

soup = BeautifulSoup(txtResult, 'html.parser')
arrSubjects = soup.findAll('div', attrs={'class': 'w_text'})

for item in arrSubjects:
	print item.span.a.span['id']
	print item.find('span', attrs={'class':'hu_nick_txt'})
