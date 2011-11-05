#encoding=utf-8
from smallseg import SEG
import MySQLdb


seg = SEG()

def cuttest(text):
    wlist = seg.cut(text)
    wlist.reverse()
    tmp = ",".join(wlist)
    return tmp


if __name__=="__main__":
    conn = MySQLdb.connect(host='localhost',user='root',passwd='chensi',\
            db='weibo_add')
    cur = conn.cursor()
    cur1 = conn.cursor()
    sql = "select id,content from choose where chop_content is null LIMIT 100"
    cur.execute(sql)
    cur1.execute(sql)
    num = len(cur1.fetchall())
    print num
    while num > 0:
        try:
            raw_content = cur.fetchone()
            l_id = int(raw_content[0])
            content = raw_content[1]
            chop_content = cuttest(content)
            print chop_content
        except Exception,e:
            pass
        num = num - 1
        try:
            sql = "update `choose` set `chop_content` = '" + chop_content + "' \
                    where `id` = "+ str(l_id) 
            cur1.execute(sql)
            conn.commit()
        except Exception,E:
            sql = "update `choose` set `chop_content` = '" + "error" + "' \
                    where `id` = "+ str(l_id) 
            cur1.execute(sql)
            conn.commit()
