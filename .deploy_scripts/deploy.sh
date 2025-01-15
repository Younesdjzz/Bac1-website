set -x
pkill -9 python
pkill -9 flask
rm -r venv
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
site=${1:0:3}
group_number=${1: -2}
index="x"

if [ "$site" = "UCL" ]; then
    index="0"
elif [ "$site" = "CRL" ]; then
    index="1"
elif [ "$site" = "ULB" ]; then
    index="2"
elif [ "$site" = "o10" ]; then
    index="3"
else
    echo "Did not managed to parse the group name"
fi
rm log.out 2>/dev/null
rm log.err 2>/dev/null
(flask --app=mobility run -p 5${index}${group_number} > log.out 2>&1 &) ; sleep 15

if [ -s log.err ]; then
    echo "Your server encountered an error :"
    echo "stdout : "
    cat log.out
    echo "=========="
    echo "stderr : "
    cat log.err
    exit 1
else
    echo "Your server is running"
    echo "stdout : "
    cat log.out
fi
