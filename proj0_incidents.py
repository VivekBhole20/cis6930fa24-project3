import argparse

import urllib.request
import io

import re
import pypdf

import sqlite3

def fetchPDFData(url):
    headers={}
    headers['User-Agent']="Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

    data=urllib.request.urlopen(urllib.request.Request(url,headers=headers)).read();
    data=io.BytesIO(data)
    #print(data)
    return data;

def extractPDFData(incident_data):
    reader=pypdf.PdfReader(incident_data)
    
    ###DEBUG

    #page=reader.pages[2]
    #page_text=page.extract_text(extraction_mode="layout")
    #print(page_text)
    #page_rows=page_text.split('\n')
    #page_rows.pop()
    #page_rows.pop(0)
    #page_rows.pop(0)
    #for i in page_rows:
    #    print(i)
    #print(type(page_rows[3]))
    #fields1=re.split(r'\s{2,}',page_rows[5])
    #fields=re.split(r'\s{2,}',page_rows[6])
    #print(fields1)
    #print(fields)
    #if len(fields)==2:
    #    for field in range(len(fields)):
    #        if fields[field]:
    #            fields1[1+field]+=(' '+fields[field])
    #if len(fields)==3:
    #    fields.insert(2,'')
    #    fields.insert(3,'')
    #print()
    #print(fields)

    #print(fields1)
    #for i in fields:
    #    print(i)
    ###

    formatted_data=[]
    for i in range(len(reader.pages)):
        page=reader.pages[i]
        page_text=page.extract_text(extraction_mode="layout")
        page_rows=page_text.split('\n')
        
        if i == 0:
            page_rows.pop(0)
            page_rows.pop(0)
            page_rows.pop(0)
        if i==len(reader.pages)-1:
            page_rows.pop()

        for row in page_rows:
            if row:
                fields=re.split(r'\s{2,}',row)
                if len(fields)==2:
                    for field in range(len(fields)):
                        if fields[field]:
                            formatted_data[-1][1+field]+=(' '+fields[field]);
                else:
                    if len(fields)==3:
                        fields.insert(2,'')
                        fields.insert(3,'')
                    formatted_data.append(fields)
    
    #print(formatted_data)
    return formatted_data

def createdb():
    con=sqlite3.connect("resources/normanpd.db")
    
    cur=con.cursor()

    cur.execute("CREATE TABLE incidents (incident_time TEXT,incident_number TEXT,incident_location TEXT,nature TEXT,incident_ori TEXT);")

    ###DEBUG
    #res=cur.execute("SELECT name FROM sqlite_master")
    #print(res.fetchone())
    ###

    return con

def populatedb(formatted_data,con):
    cur=con.cursor();

    cur.executemany("INSERT INTO  incidents VALUES(?,?,?,?,?)",formatted_data)
    con.commit()

    ###DEBUG
    #for row in cur.execute("SELECT * FROM incidents"):
    #    print(row)
    ###

def status(con):
    cur=con.cursor();

    for row in cur.execute("SELECT nature,COUNT(nature) FROM incidents GROUP BY nature ORDER BY nature"):
        print(row[0],' | ',row[1])
        #print(type(row))

def query_db(query, db_path="resources/normanpd.db"):
    """Executes a query and returns the result as a DataFrame."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def fetch_all_data():
    # Get the absolute path to the `normanpd.db`
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "resources", "normanpd.db")

    # Query the database
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM incidents", conn)
    conn.close()
    return df

def main(url):
    incident_data=fetchPDFData(url)

    extracted_data=extractPDFData(incident_data)

    db=createdb()

    populatedb(extracted_data,db)

    status(db)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--incidents', type=str,required=True,help='Incident summary url')
    args=parser.parse_args()
    if args.incidents:
        main(args.incidents)
