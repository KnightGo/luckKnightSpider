# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from operator import index
from itemadapter import ItemAdapter
import csv
import pandas as pd
import numpy as np

class LuckknightspiderPipeline:

    def __init__(self): 
        self.data_excel=[]

    def process_item(self, item, spider):
        li_temp = np.array(list(dict(item).values()))
        li_data = []
        for i in range(len(li_temp)):
            li_data.append(str(li_temp[i]))
        self.data_excel.append(li_data)

        return item                  

    def close_spider(self,spider):
        print(spider)
        self.item_list = ['image','url','title','upc','coupon_price','price','original_price','on_sale','inventory'] 
        self.f_excel = pd.ExcelWriter("bird-feeding.xlsx")
        self.data_df = pd.DataFrame(self.data_excel)
        self.data_df.columns = self.item_list
        self.data_df.to_excel(self.f_excel, float_format='%.5f',index=False)
        self.f_excel.save()
