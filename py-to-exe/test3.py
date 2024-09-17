import pymysql
def find_tempt_code(file_name, connection):
    with connection.cursor() as cursor:
        sql = """
        SELECT tempt_code
        FROM code
        WHERE file_name = %s
        """
        cursor.execute(sql, (file_name,))
        code = cursor.fetchone()[0]
    return code

def test3_main(m_id, strategy_name):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'aiinvest'
    }
    connection = pymysql.connect(**db_config)
    with(open('./' + str(m_id) + '_' + strategy_name + '.py', 'w', encoding='utf-8')) as f:
        code = find_tempt_code(str(m_id) + '_' + strategy_name, connection)
        for i in code:
            # if i == '\n':
            #     f.write('')
            # else:
            #     f.write(i)
            f.write(i)
    f.close()
    connection.close()

if __name__ == "__main__":
    test3_main()