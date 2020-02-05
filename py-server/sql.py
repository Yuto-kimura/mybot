import glob, json
import sqlite3 as sql

# dummy_record = [
#     {
#         'ID':'_231489509_-1463812096',
#         'USER_NAME':'kimura',
#         'KEYWORD':'daab'
#     },
#     {
#         'ID':'_231493067_1694498816',
#         'USER_NAME':'inoue',
#         'KEYWORD':'daab'
#     },
#     {
#         'ID':'_231489514_-1723858944',
#         'USER_NAME':'kiyasu',
#         'KEYWORD':'javascript'
#     },
#     {
#         'ID':'_231478384_251658240',
#         'USER_NAME':'matsumoto',
#         'KEYWORD':'nodejs'
#     }
# ]

class SQLExceptionError(Exception):
    pass

class SearchRequests:
    def __init__(self):
        self.database_path = "./yurubot_user.db"
        self.user_table = "yurubot_user"
        self.table_index = '("ID", "USER_NAME", "KEYWORD")'

    def delete_table(self):
        conn=sql.connect(self.database_path)
        cur=conn.cursor()
        query = "DROP TABLE IF EXISTS %s" % self.user_table
        cur.execute(query)
        conn.commit()
        conn.close()

    def creat_table(self):
        conn=sql.connect(self.database_path)
        cur=conn.cursor()
        query = "CREATE TABLE IF NOT EXISTS " + self.user_table + " " + self.table_index
        cur.execute(query)
        conn.commit()
        conn.close()

    def setup_dummy_table(self):
        dummy = dummy_record
        conn=sql.connect(self.database_path)
        cur=conn.cursor()
        for record in dummy:
            query = "INSERT INTO %s (%s, %s, %s) VALUES ('%s', '%s', '%s')" % (self.user_table, 'ID', 'USER_NAME', 'KEYWORD', record['ID'], record['USER_NAME'], record['KEYWORD'])
            cur.execute(query)
            conn.commit()
        conn.close()

    ### 上　ダミーデータ

    def request_get_user(self, keyword):
        try:
            conn=sql.connect(self.database_path)
            cur=conn.cursor()
            query = "SELECT %s FROM %s where KEYWORD='%s'" % ('ID', self.user_table, keyword)
            cur.execute(query)
            results = cur.fetchall()
            conn.commit()
            conn.close()

            # 重複(を除いた)検索結果
            key_list = list(set(results))
            result = []
            for id in key_list:
                result.append(id[0])

            response = {
                'code': 1,
                'data': result
            }
        except Exception as e:
            response = {
                'code': 0,
                'data': []
            }
        finally:
            return response

    def request_check_user(self, record):
        try:
            conn=sql.connect(self.database_path)
            cur=conn.cursor()
            query = "SELECT %s FROM %s where ID='%s'" % ('KEYWORD', self.user_table, record['ID'])
            cur.execute(query)
            results = cur.fetchall()
            conn.commit()
            conn.close()

            # 重複(を除いた)検索結果
            key_list = list(set(results))
            result = []
            for item in key_list:
                result.append(item[0])

            response = {
                'code': 1,
                'data': result
            }
        except Exception as e:
            response = {
                'code': 0,
                'data': []
            }
        finally:
            return response


    def request_update_user(self, record):
        try:
            for index in range(len(record['KEYWORD'])):
                conn=sql.connect(self.database_path)
                cur=conn.cursor()
                query = "INSERT INTO %s (%s, %s, %s) VALUES ('%s', '%s', '%s')" % (self.user_table, 'ID', 'USER_NAME', 'KEYWORD', str(record['ID']), record['USER_NAME'], record['KEYWORD'][index])
                print(query)
                cur.execute(query)
                results = cur.fetchall()
                conn.commit()
            conn.close()

            response = {
                'code': 1,
                'data': 1
            }
        except Exception as e:
            response = {
                'code': 0,
                'data': 0
            }
        finally:
            return response


    def request_delete_user(self, record):
        try:
            for index in range(len(record['KEYWORD'])):
                conn=sql.connect(self.database_path)
                cur=conn.cursor()
                query = "DELETE FROM %s WHERE ID='%s' AND KEYWORD='%s'" % (self.user_table, record['ID'], record['KEYWORD'][index])
                cur.execute(query)
                results = cur.fetchall()
                conn.commit()
            conn.close()

            response = {
                'code': 1,
                'data': 1
            }
        except Exception as e:
            response = {
                'code': 0,
                'data': 0
            }
        finally:
            return response

    def request_regist_user(self, record):
        try:
            for index in range(len(record['KEYWORD'])):
                conn=sql.connect(self.database_path)
                cur=conn.cursor()
                query = "INSERT INTO %s (%s, %s, %s) VALUES ('%s', '%s', '%s')" % (self.user_table, 'ID', 'USER_NAME', 'KEYWORD', record['ID'], record['USER_NAME'], record['KEYWORD'][index])
                cur.execute(query)
                results = cur.fetchall()
                conn.commit()
            conn.close()

            response = {
                'code': 1,
                'data': 1
            }
        except Exception as e:
            response = {
                'code': 0,
                'data': 0
            }
        finally:
            return response


    def check(self):
        conn=sql.connect(self.database_path)
        cur=conn.cursor()

        query = "SELECT * FROM %s" % (self.user_table,)
        cur.execute(query)

        results = cur.fetchall()
        conn.commit()
        conn.close()

        print("######### table status")
        # 重複(を除いた)検索結果
        # result = list(set(results))
        result = results
        for item in result:
            print(item)
        print("######### #########")


def create_dummy(req_search):
    ### dummy データベースセット
    req_search.delete_table()
    req_search.creat_table()
    ### dummy レコードの追加
    # req_search.setup_dummy_table()

def exec_post_sql(record):
    req_search = SearchRequests()
    # create_dummy(req_search) ### dummy データベースセット
    if record['REQUEST'] == "NEWUSER":
        response_data = req_search.request_regist_user(record)
    elif record['REQUEST'] == "DELETE":
        response_data = req_search.request_delete_user(record)
    elif record['REQUEST'] == "ADD":
        response_data = req_search.request_update_user(record)
    elif record['REQUEST'] == "CHECK":
        response_data = req_search.request_check_user(record)
    elif record['REQUEST'] == "GET":
        response_data = req_search.request_get_user(record['KEYWORD'])
    elif record['REQUEST'] == "CLEAR":
        create_dummy(req_search)
        response_data = {
            'code': 1,
            'data': 1
        }
    else:
        # raise SQLExceptionError([500, "Unexpected error."])
        response_data = {
            'code': 0,
            'data': []
        }
    print(response_data)

    req_search.check()
    return response_data
