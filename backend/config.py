# 数据库配置
DB_CONFIG = {
	"dbname": "WebGISDB",
	"user": "postgres",
	"password": "Jyc159753852$",      
	"host": "localhost",
	"port": "5432"
}

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
