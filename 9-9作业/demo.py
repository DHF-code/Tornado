import tornado.web
import tornado.ioloop
from tornado.options import parse_command_line, define, options
import pymysql

# 定义默认主机地址和默认端口号
define("host", default='0.0.0.0', help='主机地址')
define("port", default=8000, help="主机端口")


# 业务处理类——主页
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("主页")


class TestGetHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument('id')

        # 连接数据库
        db = pymysql.connect(host='localhost',
                             user='feng',
                             passwd='123456',
                             db='demo9_4',
                             charset='utf8')

        try:
            # 查找
            with db.cursor() as cursor:
                sql = "select * from student where id = %s"
                cursor.execute(sql, id)
                result = cursor.fetchone()
                get_result = '''
                <table border="1" width="400" align="center" cellpadding="10"cellspacing="5">
                   <tr>
                       <td>id</td>
                       <td>name</td>
                       <td>sex</td>
                       <td>city</td>
                       <td>text</td>
                       <td>date</td>
                       <td>only-child</td>
                   </tr>
                   <tr>
                       <td>{}</td>
                       <td>{}</td>
                       <td>{}</td>
                       <td>{}</td>
                       <td>{}</td>
                       <td>{}</td>
                       <td>{}</td>
                   </tr>
                </table>
                '''
                get_result = get_result.format(*result)
                self.write(get_result)
        finally:
            db.close()


# post请求
class TestPostHandler(tornado.web.RequestHandler):
    def get(self):
        html = '''
        <form action="/post" method="post">
            <table>
                <tr>
                    <td>id</td>
                    <td><input type="text" name="id"></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td><input type="text" name="name"></td>
                </tr>
                <tr>
                    <td>sex</td>
                    <td><input type="text" name="sex"></td>
                </tr>
                <tr>
                    <td>city</td>
                    <td><input type="text" name="city"></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td><input type="text" name="text"></td>
                </tr>
                <tr>
                    <td>date</td>
                    <td><input type="text" name="date"></td>
                </tr>
                <tr>
                    <td>only-child</td>
                    <td><input type="text" name="only-child"></td>
                </tr>
                <tr>
                    <td><input type="submit"></td>
                </tr>
            </table>
        </form>
        '''
        self.write(html)

    def post(self):
        id = self.get_argument('id')
        name = self.get_argument('name')
        sex = self.get_argument('sex')
        city = self.get_argument('city')
        text = self.get_argument('text')
        date = self.get_argument('date')
        child = self.get_argument('only-child')

        # 连接数据库
        db = pymysql.connect(host='localhost',
                             user='feng',
                             passwd='123456',
                             db='demo9_4',
                             charset='utf8')
        try:
            with db.cursor() as cursor:
                sql = "update student set name=%s,sex=%s, city=%s,description=%s,birthday=%s,only_child=%s where id = %s"
                cursor.execute(sql, (name, sex, city, text, date, child, id))
                self.write("<h1>修改成功</h1>")
            db.commit()
        finally:
            db.close()


if __name__ == '__main__':
    # 解析命令行
    parse_command_line()

    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/get", TestGetHandler),
        (r"/post", TestPostHandler),
    ])

    # 绑定监听地址和端口
    app.listen(options.port, options.host)
    # 启动IOLoop实例的I/O循环
    tornado.ioloop.IOLoop.current().start()