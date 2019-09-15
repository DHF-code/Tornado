import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Float, Date
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
    # sex = Column(Enum,default="男")
    city = Column(String(10), default='杭州')
    birthday = Column(Date)


# 创建表结构
Base.metadata.create_all(checkfirst=True)
# 定义与数据库的会话
session = Session()

# 定义每一个对象，对应数据库里的一行数据
bob = User(name='bob', city='上海', birthday=datetime.date(1996, 1, 24))
tom = User(name='tom', city='北京', birthday=datetime.date(1994, 5, 12))
lucy = User(name='lucy', city='杭州', birthday=datetime.date(1993, 6, 22))
jam = User(name='jam', city='南京', birthday=datetime.date(1999, 6, 10))
alex = User(name='alex', city='深圳', birthday=datetime.date(1998, 5, 2))
eva = User(name='eva', city='成都', birthday=datetime.date(1999, 2, 19))
rob = User(name='rob', city='芜湖', birthday=datetime.date(1995, 1, 12))
ella = User(name='ella', city='合肥', birthday=datetime.date(1990, 12, 3))

# 添加数据
# 在Session中记录操作
session.add_all([bob, tom, lucy, jam, alex, ella, eva, rob])
session.commit()
