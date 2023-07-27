python3 -m venv .venv
.venv/scripts/activate

AIRFLOW_VERSION=2.6.1
PYTHON_VERSION="$(python --version || python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
if [[ "3.11" == $PYTHON_VERSION ]]; then
    PYTHON_VERSION="3.10"
fi
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

cat << EOF > requirements.txt
apache-airflow==${AIRFLOW_VERSION} --constraint ${CONSTRAINT_URL}
EOF