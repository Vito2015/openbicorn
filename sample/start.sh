#!/bin/sh

work_dir=`dirname $0`
BICORN_ENV=${work_dir}/../env
BICORN_HOME=${BICORN_ENV}/lib
echo 'WORK_DIR:'${work_dir}
echo 'BICORN_ENV:'${BICORN_ENV}
echo 'BICORN_HOME:'${BICORN_HOME}
server_name=test
log_dir=${work_dir}

err_log_file=${log_dir}/${server_name}_err.log
out_log_file=${log_dir}/${server_name}_out.log

py_env=/home/mi/.virtualenvs/venv27/bin
#srv_application=serv:app
srv_application=
srv_application_conf=${work_dir}/conf.py

export PATH=$PATH
PATH=${BICORN_HOME}:${py_env}:$PATH
echo 'PY_ENV:'${py_env}

#${BICORN_ENV}/bicornx ${srv_application} -c ${srv_application_conf} --error-logfile  ${err_log_file} --access-logfile ${out_log_file}
${BICORN_ENV}/bicornx ${srv_application} -c ${srv_application_conf}