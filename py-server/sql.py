import configparser
import glob, json
import sqlite3 as sql

config = configparser.ConfigParser()
config.read('config.ini')

dummy_record = [
    {
        'ID':'_231489509_-1463812096',
        'USER_NAME':'kimura',
        'KEYWORD':'daab'
    },
    {
        'ID':'_231493067_1694498816',
        'USER_NAME':'inoue',
        'KEYWORD':'daab'
    },
    {
        'ID':'_231489514_-1723858944',
        'USER_NAME':'kiyasu',
        'KEYWORD':'javascript'
    },
    {
        'ID':'_231478384_251658240',
        'USER_NAME':'matsumoto',
        'KEYWORD':'nodejs'
    }
]

class SQLExceptionError(Exception):
    pass

class SearchRequests:
    def __init__(self):
        self.database_path = "./yurubot_user.db"
        self.user_table = "yurubot_user"
        self.table_index = '("ID", "USER_NAME", "KEYWORD")'
        # self.dbpath = config.get('database_path', 'database')
        # self.datasets = datasets
        # self.service_type = service_type
        # self.input_value = str(input_value)

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

    # def request_service_count(self):
    #     conn=sql.connect(self.dbpath)
    #     cur=conn.cursor()
    #     query = "SELECT count(*) FROM %s WHERE %s=?" % (self.datasets, self.service_type)
    #     cur.execute(query, (self.input_value,))
    #     results = cur.fetchall()
    #     conn.commit()
    #     conn.close()
    #     return results
    #
    # def request_service_record(self, record):
    #     conn=sql.connect(self.dbpath)
    #     cur=conn.cursor()
    #     query = "SELECT %s FROM %s WHERE %s=?" % (str(record), self.datasets, self.service_type)
    #     cur.execute(query, (self.input_value,))
    #     results = cur.fetchall()
    #     conn.commit()
    #     conn.close()
    #     return results

    def request_get_user(self, keyword):
        conn=sql.connect(self.database_path)
        cur=conn.cursor()
        query = "SELECT %s, %s FROM %s where KEYWORD='%s'" % ('ID', 'USER_NAME', self.user_table, keyword)
        cur.execute(query)
        results = cur.fetchall()
        conn.commit()
        conn.close()
        return results

    def request_check_user(self, record):
        pass

    def request_edit_user(self, record):
        pass

    def request_delete_user(self, record):
        pass

    def request_regist_user(self, record):
        conn=sql.connect(self.database_path)
        cur=conn.cursor()

        query = "INSERT INTO %s (%s, %s, %s) VALUES (%s, %s, %s)" % (self.user_table, 'ID', 'USER_NAME', 'KEYWORD', record['id'], record['user_name'], record['keyword'])
        # query = "SELECT %s FROM %s WHERE %s=?" % (str(record), self.datasets, self.service_type)
        # query = "SELECT %s FROM %s WHERE %s=?" % (self.user_table, str(columun), self.service_type)
        cur.execute(query, (self.input_value,))

        results = cur.fetchall()
        conn.commit()
        conn.close()

        return results

# def get_db_config(datasets):
#     table_index_list = []
#     conf = config.get('datasets_db_conf', 'datasets_conf')
#     try:
#         with open(conf, 'r') as rf:
#             db_config = json.load(rf)
#             for dataset_name in db_config:
#                 if dataset_name['datasets'] == datasets:
#                     return dataset_name['style_table_index'], dataset_name['field_name_label']
#
#         raise SQLExceptionError([500, "Unexpected error."])
#     except Exception as e:
#         raise SQLExceptionError([500, str(e)])

# def load_table_lable(datasets):
#     table_index, field_name = get_db_config(datasets)
#     field_label = []
#     field_index = ""
#     for field in table_index:
#         index = field.split(' ')[0]
#         if index == "id":
#             continue
#         field_index = field_index + index + ", "
#         field_label.append(field_name[index])
#     return field_index[0:-2], field_label

# def perse_request(req_search):
#     try:
#         data = []
#         count = req_search.request_service_count()
#
#         data.append({"件数":str(count[0][0])})
#         if count[0][0] > 0:
#             record, field_label = load_table_lable(req_search.datasets)
#             result = req_search.request_service_record(record)
#             for num in range(0, len(result[0])):
#                 data.append({str(field_label[num]):str(result[0][num])})
#
#         output = {'service': req_search.datasets, 'data': data}
#         return output
#     except Exception as e:
#         raise SQLExceptionError([500, str(e)])


def exec_sql(keyword):
    ### class __init__
    req_search = SearchRequests()
    ### dummy データベースセット
    req_search.delete_table()
    req_search.creat_table()
    req_search.setup_dummy_table()
    ###
    response_data = req_search.request_get_user(keyword)
    return response_data
