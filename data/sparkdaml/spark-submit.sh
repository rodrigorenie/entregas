#!/bin/bash

export HADOOP_USER_NAME=hadoop
export HADOOP_CONF_DIR=data/sparkdaml
export YARN_CONF_DIR=data/sparkdaml

for cls in $(python -c "import sparkdaml;print(*sparkdaml.__all__)"); do
  echo "import sparkdaml"             >   sparkjob_${cls}.py
  echo "sparkdaml.__dict__['${cls}']()" >>  sparkjob_${cls}.py
done

zip -q -x '*__pycache__*' -r sparkdaml.zip sparkdaml

for sparkjob in sparkjob_*; do
  spark-submit --properties-file=data/sparkdaml/spark-defaults.conf "${sparkjob}"
done

rm -f sparkjob_*.py sparkdaml.zip