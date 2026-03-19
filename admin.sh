#!/bin/bash

###############################################################################
#
# ansible deploy script fuer goldfisher (Python)
#
# (c) roberto@programmierer.online
#
###############################################################################



if [ "$USER" == "root" ]; then
	echo "Nicht als 'root' starten"
	exit
fi

help() {
    echo "Parameter 1: update ... Update Parameter 2: -g (Gold), -v (Variety), -r (Rate)"
    echo "Parameter 1: local ... Projekt im Debug Modus"
    echo "Parameter 1: deploy Parameter 2: local|vagrant|live"
    echo "Parameter 1: vagrant Parameter 2: create|prov|start|halt"
}

install_components() {
    apt list --installed | grep virtualbox | wc -l > /dev/null
    if [ $? == 0 ]; then
        echo "Installieren von Virtualbox"
        sudo apt update
        sudo apt install virtualbox
        [ -d /var/run/libvirt/libvirt-sock ] || sudo mkdir -p /var/run/libvirt/libvirt-sock
        sudo chmod ugo+rwx /var/run/libvirt/libvirt-sock
    fi
    apt list --installed | grep ansible | wc -l > /dev/null
    if [ $? == 0 ]; then
        echo "Installieren von Ansible"
        sudo apt update
        sudo apt install ansible
    fi
    apt list --installed | grep vagrant | wc -l > /dev/null
    if [ $? == 0 ]; then
        echo "Installieren von Vagrant"
        sudo apt update -y
        sudo apt upgrade -y
	cd /tmp
	wget https://releases.hashicorp.com/vagrant/2.3.7/vagrant_2.3.7-1_amd64.deb
	sudo dpkg -i vagrant_2.3.7-1_amd64.deb
	vagrant --version
	cd -
    fi
}


inv='ansible/hosts.conf'
yml='ansible/deploy.yml'
db='ansible/database.yml'
case "$1" in
    client)
        cd files
        shift
        source venv/bin/activate
        ./client.py $@
        deactivate
    ;;
    price)
        cd files
        source venv/bin/activate
        ./pricecheck.py $@
        deactivate
    ;;
    update)
        cd files
        source venv/bin/activate
        shift
        ./update.py $@
        deactivate
    ;;
    local)
	date +%s > files/data/timestamp.txt
        cd files
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt        
        ./pack-jss.py
        TEST=True flask --app app run --debug
        deactivate
        cd ..
	;;
    server)	    
        date +%s > files/data/timestamp.txt
        cd files
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt        
        ./files/pack-jss.py
        gunicorn -w 4 -b 0.0.0.0:5000 app:app        
        deactivate
        cd ..
	;;
    deploy)
        date +%s > files/data/timestamp.txt
        case "$2" in
            live)
                ansible-playbook -i $inv --extra-vars "{ \"host_list\":\"live\" }" $yml
            ;;
            vagrant)
                ansible-playbook -i $inv --extra-vars "{ \"host_list\":\"vagrant\" }" $yml
                ansible-playbook -i $inv --extra-vars "{ \"host_list\":\"vagrant\" }" $db
            ;;
            local)
                cd ./files
                [ -d docs ] || mkdir docs
                [ -d data ] || mkdir data
                [ -d .venv ] || python -m venv .venv
                source .venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                deactivate
                cd ..
            ;;
    *)
        help
        ;;
    esac
    ;;
    vagrant)
        case "$2" in
	        install)
		        install_components
            ;;
            create)
                vagrant destroy -f
                vagrant up --provider virtualbox
            ;;
            start)
                vagrant up --provider virtualbox
            ;;
            prov)
                vagrant provision
            ;;
            halt)
                vagrant halt
            ;;
            *)
                help
            ;;
        esac
    ;;
    *)
        help
    ;;

esac

#eof
