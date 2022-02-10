#/bin/bash
version=$1

echo "Set Version ${version}"

echo "Build Start"
docker build -t "byun618/auto-trade:${version}" .

echo "Push Start"
docker push "byun618/auto-trade:${version}"

echo "Rolling Update Start"
kubectl set image -n auto-trade deployment/auto-trade-vbs-btc auto-trade-vbs-btc=byun618/auto-trade:${version}

echo "END "