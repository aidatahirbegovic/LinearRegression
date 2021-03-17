# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
#import mysql.connector
import MySQLdb
from scrapy.exceptions import NotConfigured


class RealestateScrapyPipeline:

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host
        

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
           raise NotConfigured
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host)

    def open_spider(self, spider):
       self.conn = MySQLdb.connect(db=self.db, user=self.user, passwd=self.passwd,  host=self.host, charset='utf8', use_unicode=True)
       self.cursor = self.conn.cursor()
       self.delete_items()

    def delete_items(self):
        self.cursor.execute("TRUNCATE TABLE realestate")
        self.conn.commit()

    def process_item(self, item, spider): #, pl %s, , condition
        sql = "INSERT INTO realestate (type, typeOfOffer, city, municipality, squareFootage, constructionYear, landArea, floorInfo, registration, heatingType, roomNo, bathroomNo, price, country, con, pl, pumpaIliKalorimetri) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        #try:
        self.cursor.execute(sql,
                                (
                                    item.get("type"),
                                    item.get("typeOfOffer"),
                                    item.get("city"),
                                    item.get("municipality"),
                                    item.get("squareFootage"),
                                    item.get("constructionYear"),
                                    item.get("lanArea"),
                                    item.get("floorInfo"),
                                    item.get("registration"),
                                    item.get("heatingType"),
                                    item.get("roomNo"),
                                    item.get("bathroomNo"),
                                    item.get("price"),
                                    item.get("country"),
                                    item.get("con"),
                                    item.get("pl"),
                                    item.get("pumpaIliKalorimetri")
                                )
                        )
        self.conn.commit()
        return item

    def close_spider(self, spider):
        #self.cursor.close()
        self.conn.close()
        # except mysql.connector.Error as e:
        #     print('***************')
        #     print(e.msg)
        #     self.cursor.close()
        #     self.connection.close()
        #     self.connection = mysql.connector.connect(host='localhost', user='root', password='280495', database='realestate_db')
        #     self.cursor = self.connection.cursor()
        
        
    
