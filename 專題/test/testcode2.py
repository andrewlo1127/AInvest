from flask import Flask, request, session, jsonify, send_from_directory
import os
import mysql.connector
from flask_session import Session

app = Flask(__name__)
app.config['FILE_FOLDER'] = os.getenv('FILE_FOLDER', 'codefile')
# session配置
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

# 初始化Flask-Session
Session(app)

# 確保codefile資料夾存在
if not os.path.exists(app.config['FILE_FOLDER']):
    os.makedirs(app.config['FILE_FOLDER'])

# 連接mysql(可放到其他檔案再import)
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': '專題'
}

@app.route('/set_session', methods=['POST'])  # 測試用finction,之後做成登入用的session取得取得member_id
def set_session():
    session['member_id'] = request.form.get('member_id')
    return jsonify({'message': 'Session values set.',
                    'member_id': session['member_id']
                    })

#讀取字串或檔案
@app.route('/receive', methods=['POST'])
def receive():
    try:
        m_id = session.get('member_id')
        if not m_id:
            return jsonify({'message': 'Member ID not found in session.'}), 400
        
        data = request.form.get('data')
        file = request.files.get('file')

        filename = f't_code_{m_id}.txt'
        filepath = os.path.join(app.config['FILE_FOLDER'], filename)

        if data:  #字串
            with open(filepath, 'w') as f:  #建一個新檔案儲存
                f.write(data)
            return jsonify({'message': 'String received and saved.'})
        elif file:  # 文字檔案
            file.save(filepath)
            return jsonify({'message': 'File received and saved.'})
        else:
            return jsonify({'message': 'No data received.'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

#編輯內容(用表單)
@app.route('/edit', methods=['GET'])
def edit():
    m_id = session.get('member_id')
    filename = request.args.get('filename', f't_code_{m_id}.txt')
    filepath = os.path.join(app.config['FILE_FOLDER'], filename)
    if not os.path.isfile(filepath):
        return jsonify({'message': 'File not found.'}), 404
    try:
        with open(filepath, 'r') as f:
            data = f.read()
        return jsonify({
        'memberID': m_id,
        'strategyName': '',
        'filename': filename,
        'code': data,
        'public': 0,
        'description': ''
    })
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 表單submit後儲存
@app.route('/save', methods=['POST'])
def save():
    m_id = request.form.get('memberID')
    s_name = request.form.get('strategyName')
    f_name = request.form.get('filename')
    p_num = request.form.get('public')
    desc = request.form.get('description')
    original_filepath = os.path.join(app.config['FILE_FOLDER'], f_name)

    if not os.path.isfile(original_filepath):
        return jsonify({'message': 'Original file not found.'}), 404

    #自動產生檔案名稱
    base_filename = 'code'
    ext = '.txt'
    i = 1

    if not m_id:
        return jsonify({'message': 'Member ID not found in session.'}), 400
    
    while os.path.isfile(os.path.join(app.config['FILE_FOLDER'], f'{base_filename}_{m_id}_{i}{ext}')):
        i += 1
    new_filename = f'{base_filename}_{m_id}_{i}{ext}'
    new_filepath = os.path.join(app.config['FILE_FOLDER'], new_filename)

    try:
        with open(original_filepath, 'r') as f:
            data = f.read()
        with open(new_filepath, 'w') as f:
            f.write(data)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO code (strategy, member_id, FileName, public, description) VALUES (%s, %s, %s, %s, %s)",
            (s_name, m_id, new_filename, p_num, desc)
        )
        conn.commit()
        code_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            'message': f'File saved as {new_filename}.',
            'code_id': code_id,
            'strategy_name': s_name,
            'member_id': m_id,
            'file_name': new_filename,
            'public': p_num,
            'description': desc
        })
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 查看自己策略清單和查看公開的策略清單
@app.route('/list', methods=['GET'])
def list():
    try:
        m_id = session.get('member_id')
        public = request.args.get('public')

        # 連接資料庫
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        if public: #用是否公開來決定查看哪個
            #查詢公開的策略
            cursor.execute("SELECT strategy, member_id, FileName, description FROM code WHERE public = 1")
        else:
            #不公開只能查看自己的策略
            if not m_id:
                return jsonify({'message': 'Member ID not found in session.'}), 400
            cursor.execute("SELECT strategy, member_id, FileName, description FROM code WHERE member_id = %s",
                (m_id,)
            )

        strategies = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify([
            {
                'strategy_name': strategy,
                'member_id': member_id,
                'file_name': filename, #應設成使用者看不到
                'description': description
            } for (strategy, member_id, filename, description) in strategies
        ])
    except Exception as e:
        return jsonify({'message': str(e)}), 500

#查看已公開的code,以'member_id'和'策略名稱'查詢
@app.route('/get_file', methods=['POST'])
def get_file():
    try:
        data = request.get_json() #AJAX方式
        s_name = data.get('strategy_name')
        m_id = data.get('member_id')

        if not s_name or not m_id:
            return jsonify({'message': 'Strategy name or member ID not found in request or session.'}), 400
        # 連接資料庫
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # 查詢file_name
        cursor.execute(  
            "SELECT FileName FROM code WHERE strategy = %s AND member_id = %s",  # strategy_name, member_id
            (s_name, m_id)
        )
        result = cursor.fetchone()
        # 關閉連結
        cursor.close()
        conn.close()
        if not result:
            return jsonify({'message': 'File not found for the given strategy name and member ID.'}), 404
        filename = result[0]  #只有一個欄位'filename'
        return send_from_directory(app.config['FILE_FOLDER'], filename)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
