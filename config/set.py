import os

from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import  String,DateTime,func
from fastapi import FastAPI,Depends
from  sqlalchemy.sql import  select

# app = FastAPI()

ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

#创建异步引擎
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True,pool_size = 10,max_overflow = 5 )

# #创建Base类
# class Base(DeclarativeBase):
#     create_time: Mapped [DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(),comment="创建时间")
#     update_time: Mapped [DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(),comment="更新时间")
# #创建模型类，对应数据库表
# class News(Base):
#     __tablename__ = "news"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     title: Mapped[str] = mapped_column(String(255),comment="新闻标题")
#     content: Mapped[str] = mapped_column(String(505),comment="新闻内容")


#创建session工厂
async_session = async_sessionmaker(bind=async_engine,class_= AsyncSession, expire_on_commit=False)

#依赖注入：每次请求给一个数据库session
async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()

# #项目启动时自动建表
# @app.on_event("startup")
# async def startup():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
# @app.get("/news")
# async def get_news(db:AsyncSession = Depends(get_db)):
#     news = await db.execute(select(News))
#     return news.scalars().all()
