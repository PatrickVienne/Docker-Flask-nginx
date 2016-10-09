import os
import shutil
from project import app


# Postgres Initialization Files
create_user_file = 'create_user.sh'
create_db_file = 'create_db.sh'
source_dir = os.path.abspath(os.curdir)
destination_dir = os.path.join(source_dir, '../postgresql')

# Create the 'create_user.sh' file for initializing the Postgres Docker image
with open('create_user.sh', 'w') as postgres_create_user:
    postgres_create_user.write('#!/bin/bash')
    postgres_create_user.write('\nset -e')
    postgres_create_user.write('\n')
    postgres_create_user.write('\nPOSTGRES="psql --username {}"'.format(app.config['POSTGRES_DEFAULT_USER']))
    postgres_create_user.write('\n')
    postgres_create_user.write('\necho "Creating database role: {}"'.format(app.config['POSTGRES_USER']))
    postgres_create_user.write('\n')
    postgres_create_user.write('\n$POSTGRES <<-EOSQL')
    postgres_create_user.write("\nCREATE USER {} WITH CREATEDB PASSWORD '{}';".format(app.config['POSTGRES_USER'], app.config['POSTGRES_PASSWORD']))
    postgres_create_user.write('\nEOSQL')

# Create the 'create_db.sh' file for initializing the Postgres Docker image
with open('create_db.sh', 'w') as postgres_create_db:
    postgres_create_db.write("#!/bin/bash")
    postgres_create_db.write('\nset -e')
    postgres_create_db.write('\n')
    postgres_create_db.write('\nPOSTGRES="psql --username {}"'.format(app.config['POSTGRES_DEFAULT_USER']))
    postgres_create_db.write('\n')
    postgres_create_db.write('\necho "Creating database: {}"'.format(app.config['POSTGRES_DB']))
    postgres_create_db.write('\n')
    postgres_create_db.write('\n$POSTGRES <<EOSQL')
    postgres_create_db.write('\nCREATE DATABASE {} OWNER {};'.format(app.config['POSTGRES_DB'], app.config['POSTGRES_USER']))
    postgres_create_db.write('\nEOSQL')

# Move the files created ('create_user.sh' and 'create_db.sh') to the ../postgres directory
shutil.move(os.path.join(source_dir, create_user_file), os.path.join(destination_dir, create_user_file))
shutil.move(os.path.join(source_dir, create_db_file), os.path.join(destination_dir, create_db_file))