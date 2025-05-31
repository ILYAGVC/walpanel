#!/bin/bash

REPO_URL="https://github.com/primeZdev/walpanel.git"
INSTALL_DIR="/opt/walpanel"
DONATION_ADDRESS="TWHESbRLWB9ZNoL9vcphY2r56qHeJLwtmZ"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

print_banner() {
    clear
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}${BOLD}                    WALPANEL INSTALLER                     ${NC}${BLUE}║${NC}"
    echo -e "${BLUE}╠════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${BLUE}║${NC}${CYAN} [1] Install Walpanel${NC}${BLUE}                                     ║${NC}"
    echo -e "${BLUE}║${NC}${CYAN} [2] Update Walpanel${NC}${BLUE}                                      ║${NC}"
    echo -e "${BLUE}║${NC}${CYAN} [3] Check Status${NC}${BLUE}                                         ║${NC}"
    echo -e "${BLUE}║${NC}${CYAN} [4] Donate${NC}${BLUE}                                              ║${NC}"
    echo -e "${BLUE}║${NC}${CYAN} [5] Uninstall Walpanel${NC}${BLUE}                                  ║${NC}"
    echo -e "${BLUE}║${NC}${CYAN} [0] Exit${NC}${BLUE}                                               ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo
}

check_dependencies() {
    echo -e "${BLUE}[*] Checking dependencies...${NC}"
    
    # Check if running as root
    if [ "$EUID" -ne 0 ]; then 
        echo -e "${RED}Please run as root (use sudo)${NC}"
        exit 1
    fi

    # Install Docker using official method
    echo -e "${BLUE}[*] Installing Docker...${NC}"
    curl -fsSL https://get.docker.com | sh || {
        echo -e "${RED}[-] Failed to install Docker${NC}"
        exit 1
    }

    # Install other dependencies
    echo -e "${BLUE}[*] Installing other dependencies...${NC}"
    apt update
    apt install -y git curl gnupg2 || {
        echo -e "${RED}[-] Failed to install required packages${NC}"
        exit 1
    }

    # Install Caddy
    echo -e "${BLUE}[*] Installing Caddy web server...${NC}"
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list
    apt update
    apt install -y caddy || {
        echo -e "${RED}[-] Failed to install Caddy${NC}"
        exit 1
    }

    # Start and enable services
    echo -e "${BLUE}[*] Starting services...${NC}"
    systemctl enable docker
    systemctl start docker
    systemctl enable caddy
    systemctl start caddy
    
    echo -e "${GREEN}[+] Dependencies installed successfully${NC}"
}

install() {
    echo -e "${BLUE}[*] Starting installation...${NC}"

    if [ -d "$INSTALL_DIR" ]; then
        echo -e "${YELLOW}[!] Walpanel already installed at $INSTALL_DIR${NC}"
        return
    fi

    git clone "$REPO_URL" "$INSTALL_DIR" || {
        echo -e "${RED}[-] Failed to clone repository${NC}"
        exit 1
    }

    cd "$INSTALL_DIR" || exit 1
    cp .env.example .env

    echo -e "${BLUE}[*] Configuration${NC}"
    read -p "Admin username: " USERNAME
    read -p "Admin password: " PASSWORD
    read -p "Telegram admin chat ID: " ADMIN_CHAT_ID
    read -p "Telegram bot token: " BOT_TOKEN
    read -p "Domain/subdomain (e.g. panel.example.com): " SUBDOMAIN

    PANEL_ADDRESS="https://$SUBDOMAIN/login/"

    sed -i "s|USERNAME=.*|USERNAME=$USERNAME|g" .env
    sed -i "s|PASSWORD=.*|PASSWORD=$PASSWORD|g" .env
    sed -i "s|ADMIN_CHAT_ID=.*|ADMIN_CHAT_ID=$ADMIN_CHAT_ID|g" .env
    sed -i "s|BOT_TOKEN=.*|BOT_TOKEN=$BOT_TOKEN|g" .env
    sed -i "s|PANEL_ADDRESS=.*|PANEL_ADDRESS=$PANEL_ADDRESS|g" .env

    echo -e "${BLUE}[*] Setting up Caddy reverse proxy...${NC}"
    cat > /etc/caddy/Caddyfile <<EOF
$SUBDOMAIN {
    reverse_proxy localhost:8000
}
EOF
    systemctl reload caddy

    echo -e "${BLUE}[*] Starting Walpanel containers...${NC}"
    docker compose up -d --build || {
        echo -e "${RED}[-] Docker compose failed${NC}"
        exit 1
    }

    echo -e "${GREEN}[+] Walpanel installed! Access it at: https://$SUBDOMAIN/login/${NC}"
}

update() {
    echo -e "${BLUE}[*] Updating Walpanel...${NC}"
    if [ ! -d "$INSTALL_DIR" ]; then
        echo -e "${RED}[-] Walpanel not found!${NC}"
        return
    fi
    cd "$INSTALL_DIR" || exit 1
    git pull
    docker compose down
    docker compose up -d --build
    echo -e "${GREEN}[+] Update complete${NC}"
}

uninstall() {
    echo -e "${YELLOW}[!] Uninstalling Walpanel...${NC}"
    if [ ! -d "$INSTALL_DIR" ]; then
        echo -e "${RED}[-] Nothing to uninstall${NC}"
        return
    fi
    cd "$INSTALL_DIR" || exit 1
    docker compose down
    rm -rf "$INSTALL_DIR"
    rm -f /etc/caddy/Caddyfile
    systemctl reload caddy
    echo -e "${GREEN}[+] Walpanel uninstalled${NC}"
}

status() {
    echo -e "${BLUE}[*] Docker containers status:${NC}"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

donate() {
    clear
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}${BOLD}                 SUPPORT WALPANEL DEVELOPMENT              ${NC}${BLUE}║${NC}"
    echo -e "${BLUE}╠════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${BLUE}║${NC} Donate (TRON - TRC20): ${GREEN}$DONATION_ADDRESS${NC}${BLUE}     ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo
}

while true; do
    print_banner
    read -p "Select an option [0-5]: " opt
    case $opt in
        1) check_dependencies && install ;;
        2) update ;;
        3) status ;;
        4) donate ;;
        5) uninstall ;;
        0) echo -e "${GREEN}Goodbye!${NC}"; exit 0 ;;
        *) echo -e "${RED}Invalid choice${NC}" ;;
    esac
    read -p "Press [Enter] to continue..."
done
