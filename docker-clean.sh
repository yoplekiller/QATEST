echo "🔥 Docker 청소 시작..."

docker container prune -f
docker image prune -a -f
docker volume prune -f
docker network prune -f

echo "✅ Docker 청소 완료!"

