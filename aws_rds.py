from flask import Flask, render_template, request
import pymysql
import csv
app = Flask(__name__)


def connectDB():
    return pymysql.connect(host='', port=3306, user='',
                           password='', db='cloud6331')


def cleanDB():
    conn = connectDB()
    cur = conn.cursor()
    query = 'DELETE FROM book WHERE latitude IS NULL OR longitude IS NULL OR magError IS NULL '
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


@app.route('/passenger', methods=['POST','GET'])
def passenger(records=None):
    conn = connectDB()
    cur = conn.cursor()
    if request.method == 'POST':
        lname = request.form['lname']
        fare1 = request.form['fare1']
        fare2 = request.form['fare2']
        if lname:
            lname =' '
        elif not fare1:
            fare1 =' '
        elif not fare2:
            fare2 =' '

        query = 'select * from boat where name like "%'+lname+'" or fare between '+fare1+' and '+fare2
        cur.execute(query)
        result = cur.fetchall()
        records = []
        for row in result:
            tuple = (row[2], row[3], row[4], row[5], row[6])
            records.append(tuple)

        conn.commit()
        cur.close()
        conn.close()
    return render_template('display.html', records=records)


@app.route('/update', methods=['POST','GET'])
def update():
    conn = connectDB()
    cur = conn.cursor()
    if request.method == 'POST':
        dest = request.form['dest']
        fare1 = request.form['fare1']
        fare2 = request.form['fare2']

        sql = 'UPDATE boat SET home_dest = "'+dest+'" WHERE fare between '+fare1+' and '+fare2
        cur.execute(sql)
        query = 'select * from boat WHERE fare between '+fare1+' and '+fare2
        cur.execute(query)
        result = cur.fetchall()
        records = []
        for row in result:
            tuple = (row[2], row[3], row[4], row[6], row[8])
            records.append(tuple)

        conn.commit()
        cur.close()
        conn.close()
    return render_template('display.html', records=records)









@app.route('/age', methods=['POST','GET'])
def cityResult():
    conn = connectDB()
    cur = conn.cursor()
    if request.method == 'POST':
        age1 = request.form['age1']
        age2 = request.form['age2']
        query = 'select sum(survived) from boat where age between '+age1+' and '+age2+''
        cur.execute(query)
        result = cur.fetchone()
        countSurvivors = result[0]
        conn.commit()
        cur.close()
        conn.close()
        return render_template('index.html', survivors=countSurvivors)



@app.route('/')
def hello_world():
    conn = connectDB()
    cur = conn.cursor()
    query = 'select COUNT(*) from boat'
    cur.execute(query)
    result = cur.fetchone()
    count = result[0]
    conn.commit()
    cur.close()
    conn.close()
    return render_template('index.html', count=count)


if __name__ == '__main__':
    app.run()
