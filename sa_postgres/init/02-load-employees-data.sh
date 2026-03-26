# apt update
# apt install wget
# wget https://raw.githubusercontent.com/neondatabase/postgres-sample-dbs/main/employees.sql.gz
# pg_restore -d postgres://sql_agent_user:sql_agent_password@localhost:5432/employees -Fc /tmp/sa_postgres_data/employees.sql.gz --no-owner --no-privileges