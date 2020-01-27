import pymysql #MYSQL CLIENT
from app import app #Flask RUN
from db_config import mysql #Config DB
from flask import request, jsonify



#Route 
@app.route('/mahasiswa', methods=['GET'])
def mahasiswa():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("Select * from mahasiswa")
        rows = cursor.fetchall()
        res = jsonify(rows)
        res.headers.add('Access-Control-Allow-Origin', '*')
        res.status_code = 200
        if len(rows)==0:
            return jsonify(
                {
                    "Message":"Data Not Found"
                }
            ), 200
        else:
            return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/mahasiswa/<int:id>', methods=['GET'])
def mahasiswa_one(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select * from mahasiswa where id=%s", id)
        row = cursor.fetchone()
        res = jsonify(row)
        res.status_code = 200
        res.headers.add('Access-Control-Allow-Origin', '*')  
        if row is None:
            return jsonify(
                {
                    "Message " : " Data Not Found"
                }
            )
        else:
            return res
    except Exception as e:
         print(e)
    finally:
        cursor.close()
        conn.close()
    
@app.route('/mahasiswa', methods=['POST'])
def mahasiswa_add():
    try:
        _json = request.json
        _nim = _json['nim']
        _rfid_id = _json['rfid_id']
        _nama = _json['nama']

        if request.method=='POST':
            if _nim and _rfid_id:
                sql = "Insert into mahasiswa (nim, rfid_id, nama) values (%s, %s, %s)"
                data = (_nim, _rfid_id, _nama)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql,data)
                conn.commit()
                res = jsonify("Mahasiswa Added Successfully")
                res.status_code = 200
                res.headers.add('Access-Control-Allow-Origin', '*')
                return res
    except Exception as e:
        print (e)
    finally:
        cursor.close()
        conn.close()

@app.route('/mahasiswa/<id>', methods=['PUT'])
def mahasiswa_update(id):
    try:
        _json = request.json
       # _id = _json ['id']
        _nim = _json['nim']
        _rfid_id = _json['rfid_id']
        _nama = _json['nama']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        check_nim = cursor.execute("select * from mahasiswa where nim=%s", _nim)
        check_rfid = cursor.execute("select * from mahasiswa where nim=%s", _rfid_id)

        if request.method=='PUT':
            if check_nim > 0:
                return jsonify(
                    {
                        "Message" : "Data Nim was available"
                    }
                ), 200
            elif check_rfid > 0:
                return jsonify(
                    {
                        "Message" : "Data RFID ID was available"
                    }
                ), 200
            else:
                sql = "update mahasiswa set nim=%s, rfid_id=%s, nama=%s where id=%s"
                data = (_nim, _rfid_id, _nama, id)
                cursor.execute(sql, data)
                conn.commit()
                res = jsonify("Mahasiswa Has Been Updated")
                res.status_code = 200
                res.headers.add('Access-Control-Allow-Origin', '*') 
                return res
            
    except Exception as e:
        print (e)
    finally:
        cursor.close()
        conn.close()

@app.route('/mahasiswa/<id>', methods=['DELETE'])
def mahasiswa_delete(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("delete from mahasiswa where id=%s", id)
        conn.commit()
        res = jsonify('Mahasiswa Has Been Deleted')
        res.status_code=200
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status' : 404,
        'message' : 'Not Found: ' + request.url,
    }
    res = jsonify(message)
    res.status_code= 404
    return res
