"""
Database Utilities

MySQL 데이터베이스 연결 및 쿼리 실행을 담당하는 유틸리티 클래스입니다.
APIEnv 패턴을 따라 DBEnv 클래스로 구성되어 있습니다.

사용 예:
    from utils.db_utils import DBEnv

    db = DBEnv()
    db.connect()
    results = db.execute_query("SELECT * FROM movies")
    db.close()
"""
import os
import allure
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class DBEnv:
    """MySQL 데이터베이스 연결 및 쿼리 실행 유틸리티"""

    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.connection = None

    @allure.step("MySQL 데이터베이스 연결")
    def connect(self):
        """MySQL 서버에 연결"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            allure.attach(
                f"Host: {self.host}:{self.port}, DB: {self.database}",
                name="DB 연결 정보",
                attachment_type=allure.attachment_type.TEXT
            )
            return self.connection
        except mysql.connector.Error as e:
            allure.attach(str(e), name="DB 연결 에러", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("SQL 쿼리 실행: {query}")
    def execute_query(self, query, params=None):
        """SELECT 쿼리 실행 후 결과 반환"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            allure.attach(
                f"쿼리: {query}\n결과 행 수: {len(results)}",
                name="쿼리 실행 결과",
                attachment_type=allure.attachment_type.TEXT
            )
            return results
        except mysql.connector.Error as e:
            allure.attach(str(e), name="쿼리 실행 에러", attachment_type=allure.attachment_type.TEXT)
            raise
        finally:
            cursor.close()

    @allure.step("SQL INSERT 실행")
    def execute_insert(self, query, params=None):
        """INSERT/UPDATE/DELETE 쿼리 실행"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount
        except mysql.connector.Error as e:
            self.connection.rollback()
            allure.attach(str(e), name="INSERT 실행 에러", attachment_type=allure.attachment_type.TEXT)
            raise
        finally:
            cursor.close()

    @allure.step("다중 INSERT 실행")
    def execute_many(self, query, data_list):
        """여러 행을 한 번에 INSERT"""
        cursor = self.connection.cursor()
        try:
            cursor.executemany(query, data_list)
            self.connection.commit()
            allure.attach(
                f"삽입 행 수: {cursor.rowcount}",
                name="다중 INSERT 결과",
                attachment_type=allure.attachment_type.TEXT
            )
            return cursor.rowcount
        except mysql.connector.Error as e:
            self.connection.rollback()
            allure.attach(str(e), name="다중 INSERT 에러", attachment_type=allure.attachment_type.TEXT)
            raise
        finally:
            cursor.close()

    @allure.step("DDL 실행")
    def execute_ddl(self, query):
        """CREATE/DROP/ALTER 등 DDL 쿼리 실행"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as e:
            allure.attach(str(e), name="DDL 실행 에러", attachment_type=allure.attachment_type.TEXT)
            raise
        finally:
            cursor.close()

    @allure.step("MySQL 연결 종료")
    def close(self):
        """데이터베이스 연결 종료"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
