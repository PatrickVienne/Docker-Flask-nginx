from project import app


with open('postgres.env', 'w') as postgres_env:
    postgres_env.write('POSTGRES_USER = ' + app.config['POSTGRES_USER'])
    postgres_env.write('\nPOSTGRES_PASSWORD = ' + app.config['POSTGRES_PASSWORD'])
    postgres_env.write('\nPOSTGRES_DB = ' + app.config['POSTGRES_DB'])
