#!/bin/bash

REPO_URL="https://github.com/primeZdev/walpanel.git"
INSTALL_DIR="/opt/walpanel"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_banner() {
    echo -e "${BLUE}==== Walpanel Installer ====${NC}"
    echo -e "${YELLOW}1) Install"
    echo -e "2) Uninstall"
    echo -e "3) Update"
    echo -e "4) Status"
    echo -e "0) Exit${NC}"
    echo -e "${BLUE}=============================${NC}"
}

check_dependencies() {
    echo -e "${BLUE}[+] Checking dependencies...${NC}"
    apt update
    apt install -y docker.io docker-compose certbot nginx git || {
        echo -e "${RED}[-] Failed to install dependencies.${NC}"
        exit 1
    }
    systemctl enable docker && systemctl start docker
}

install() {
    echo -e "${BLUE}[+] Installing Walpanel...${NC}"
    if [ -d "$INSTALL_DIR" ]; then
        echo -e "${YELLOW}[!] $INSTALL_DIR already exists. Skipping clone...${NC}"
    else
        git clone "$REPO_URL" "$INSTALL_DIR" || {
            echo -e "${RED}[-] Git clone failed.${NC}"
            exit 1
        }
    fi

    cd "$INSTALL_DIR" || exit 1

    [ ! -f .env ] && cp .env.example .env

    echo -e "${BLUE}[+] Configuring environment...${NC}"
    read -p "Enter USERNAME: " USERNAME
    read -p "Enter PASSWORD: " PASSWORD
    read -p "Enter ADMIN_CHAT_ID: " ADMIN_CHAT_ID
    read -p "Enter BOT_TOKEN: " BOT_TOKEN
    read -p "Enter your subdomain (e.g. panel.example.com): " SUBDOMAIN
    read -p "Enter the port to expose (default 443): " PORT
    PORT=${PORT:-443}

    sed -i "s|USERNAME=.*|USERNAME=$USERNAME|g" .env
    sed -i "s|PASSWORD=.*|PASSWORD=$PASSWORD|g" .env
    sed -i "s|ADMIN_CHAT_ID=.*|ADMIN_CHAT_ID=$ADMIN_CHAT_ID|g" .env
    sed -i "s|BOT_TOKEN=.*|BOT_TOKEN=$BOT_TOKEN|g" .env

    echo -e "${BLUE}[+] Stopping Nginx temporarily to free port 80...${NC}"
    systemctl stop nginx

    echo -e "${BLUE}[+] Obtaining SSL certificate for $SUBDOMAIN...${NC}"
    certbot certonly --standalone -d "$SUBDOMAIN" --non-interactive --agree-tos -m admin@$SUBDOMAIN || {
        echo -e "${RED}[-] SSL failed. Make sure port 80 is free.${NC}"
        systemctl start nginx
        exit 1
    }

    echo -e "${GREEN}[✔] SSL Certificate obtained.${NC}"
    echo -e "${BLUE}[+] Starting Nginx again...${NC}"
    systemctl start nginx

    echo -e "${BLUE}[+] Setting up Nginx reverse proxy...${NC}"
    cat <<EOF > /etc/nginx/sites-available/walpanel
server {
    listen $PORT ssl;
    server_name $SUBDOMAIN;

    ssl_certificate /etc/letsencrypt/live/$SUBDOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$SUBDOMAIN/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

    ln -sf /etc/nginx/sites-available/walpanel /etc/nginx/sites-enabled/walpanel
    nginx -t && systemctl restart nginx

    echo -e "${BLUE}[+] Launching application with Docker...${NC}"
    docker-compose up -d --build || {
        echo -e "${RED}[-] Docker-compose failed.${NC}"
        exit 1
    }

    echo -e "${GREEN}[✔] Walpanel installed successfully! Access it at: https://$SUBDOMAIN${PORT:+:$PORT}/login/${NC}"
}

uninstall() {
    echo -e "${YELLOW}[!] Uninstalling Walpanel...${NC}"
    cd "$INSTALL_DIR" || exit
    docker-compose down
    rm -f /etc/nginx/sites-enabled/walpanel /etc/nginx/sites-available/walpanel
    systemctl restart nginx
    echo -e "${GREEN}[✔] Uninstalled successfully.${NC}"
}

update() {
    echo -e "${BLUE}[+] Updating Walpanel...${NC}"
    cd "$INSTALL_DIR" || exit
    git pull
    docker-compose up -d --build
    echo -e "${GREEN}[✔] Update complete.${NC}"
}

status() {
    docker ps --filter name=walpanel
}

# Menu loop
while true; do
    print_banner
    read -p "$(echo -e ${BLUE}Select an option:${NC} ) " opt
    case $opt in
        1) check_dependencies && install ;;
        2) uninstall ;;
        3) update ;;
        4) status ;;
        0) echo -e "${GREEN}Bye!${NC}"; exit 0 ;;
        *) echo -e "${RED}Invalid option.${NC}" ;;
    esac
done
