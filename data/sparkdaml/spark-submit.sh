#!/bin/bash
export HADOOP_USER_NAME=hadoop
export HADOOP_CONF_DIR=data/sparkdaml
export YARN_CONF_DIR=data/sparkdaml

cat << EOF > sparkjob.py
import sparkdaml
sparkdaml.run()
EOF

zip -x '*__pycache__*' -r sparkdaml.zip sparkdaml

# spark.archives
#
spark-submit --properties-file=data/sparkdaml/spark-defaults.conf sparkjob.py

rm -f sparkjob.py
rm -f sparkdaml.zip