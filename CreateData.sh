
how_many=10000000
for x in $(seq 0 1 $how_many); do
(&>/dev/null curl 0.0.0.0:8080/err &)
done