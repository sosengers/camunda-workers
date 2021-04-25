#!/bin/sh

echo "Waiting for camunda_acmesky"
while ! nc -z camunda_acmesky 8080; do
  sleep 0.1
done
echo "camunda_acmesky is reachable"

echo "Uploading BPMN camunda diagram"
curl -X POST -F "upload=@/camunda_diagram/NotificaVoliLastMinute.bpmn" -F "deployment-name=NotificaVoliLastMinute" -F "enable-duplicate-filtering=true" http://camunda_acmesky:8080/engine-rest/deployment/create
curl -X POST -F "upload=@/camunda_diagram/AcquistoOfferta.bpmn" -F "deployment-name=AcquistoOfferta" -F "enable-duplicate-filtering=true" http://camunda_acmesky:8080/engine-rest/deployment/create
curl -X POST -F "upload=@/camunda_diagram/RegistrazioneInteresseUtente.bpmn" -F "deployment-name=RegistrazioneInteresseUtente" -F "enable-duplicate-filtering=true" http://camunda_acmesky:8080/engine-rest/deployment/create
curl -X POST -F "upload=@/camunda_diagram/VerificaGiornaliera.bpmn" -F "deployment-name=VerificaGiornaliera" -F "enable-duplicate-filtering=true" http://camunda_acmesky:8080/engine-rest/deployment/create

echo "Waiting for acmesky_backend"
while ! nc -z acmesky_backend 8080; do
  sleep 0.1
done
echo "acmesky_backend is reachable"

echo "Waiting for acmesky_middleware"
while ! nc -z acmesky_middleware 8080; do
  sleep 0.1
done
echo "acmesky_middleware is reachable"

echo "Waiting for acmesky_mq"
while ! nc -z acmesky_mq 5672; do
  sleep 0.1
done
echo "acmesky_mq is reachable"

echo "Waiting for acmesky_db"
while ! nc -z acmesky_db 5432; do
  sleep 0.1
done
echo "acmesky_db is reachable"

echo "Waiting for acmesky_redis"
while ! nc -z acmesky_redis 6379; do
  sleep 0.1
done
echo "acmesky_redis is reachable"

python3 -m camundaworkers
