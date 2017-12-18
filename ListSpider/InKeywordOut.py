#-*- coding:utf-8 -*-


class InKeywordOutData:
	def __init__(self, keywords):
        self.keywords=keywords
    def keywords_item(keywords):
       	keywordsList=[]
  		for item in self.keywords:
    		keyword_item=item
    		keywordsList.append(keyword_item)  
  			#print(keywordsList)
  		return  keywordsList       
  	def selectModel(keywords):
  	"""
  	查询单条数据时，生成查询条件的元组
  	"""
  		selectmodel=(self.keywords,)
  		return selectmodel