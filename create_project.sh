# usage:
# bash create_project.sh [project_name] [PROJECT_NAME]

echo "create project $1 | $2"
git clone https://github.com/QthCN/wsgi-basic.git
mv wsgi-basic $1
cd $1
sed -i "s/wsgi_basic/$1/g" `grep wsgi_basic -rl .`
sed -i "s/wsgi-basic/$1/g" `grep wsgi-basic -rl .`
sed -i "s/WSGI_BASIC/$2/g" `grep WSGI_BASIC -rl .`
mv wsgi_basic $1
oslo-config-generator --config-file=config-generator/wsgi-basic.conf
cp etc/wsgi-basic.conf.sample etc/$1.conf
cp etc/wsgi-basic-paste.ini etc/$1-paste.ini
sudo python setup.py develop