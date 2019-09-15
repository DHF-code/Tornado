import os

import tornado.web
import tornado.ioloop
from tornado.options import parse_command_line, define, options

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

# 建立与数据库的连接
engine = create_engine('mysql+pymysql://feng:123456@localhost:3306/demo')

# 创建模型的基础类
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class User(Base):
    '''User模型'''
    # 该模型对应的表名
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    city = Column(String(10), default='杭州')
    birthday = Column(Date)


# 定义与数据库的会话
session = Session()


# 业务处理类——主页
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("主页")


class GetHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument('id', 1)
        u = session.query(User)
        user = u.get(id)
        user = [user.id, user.name, user.city, user.birthday]
        self.render('get.html', user=user)


class PostHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('post.html')

    def post(self):
        id = self.get_argument('id')
        name = self.get_argument('name')
        city = self.get_argument('city')
        b_date = self.get_argument('date')
        u = session.query(User)
        user = u.get(id)
        user.name = name
        user.city = city
        user.birthday = b_date
        session.commit()
        self.write("修改成功")


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        # content里面显示的内容
        id = self.get_argument('id',1)
        u = session.query(User)
        content= u.get(id)

        # sidebar显示的内容（姓名）
        uses = u.filter(User.id > 0)
        self.render('test.html', uses=uses, content=content)

def make_app():
    routes = [
        (r'/', IndexHandler),
        (r'/get', GetHandler),
        (r'/post', PostHandler),
        (r'/test', TestHandler),
    ]

    # 获取模版目录和静态文件目录的绝对路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'jingtai')

    return tornado.web.Application(routes,
                                   template_path=template_dir,
                                   static_path=static_dir)


if __name__ == '__main__':
    # 定义默认主机地址和默认端口号
    define("host", default='0.0.0.0', help='主机地址')
    define("port", default=8000, help="主机端口")

    # 解析命令行
    parse_command_line()

    app = make_app()

    # 绑定监听地址和端口
    app.listen(options.port, options.host)
    # 启动IOLoop实例的I/O循环
    tornado.ioloop.IOLoop.current().start()
