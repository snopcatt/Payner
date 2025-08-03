#!/bin/bash

# Палаво Око - Network Scanner
INTERFACE="eth0"

# Меню с опции
function show_menu() {
    clear
    echo "==========================================="
    echo "    ____        __                 ____  __           "
    echo "   / __ \____ _/ /___ __   ______  / __ \/ /___  ____  "
    echo "  / /_/ / __ \`/ / __ \`/ | / / __ \/ / / / //_/ \/ /   "
    echo " / ____/ /_/ / / /_/ /| |/ / /_/ / /_/ / ,< / /_/ /    "
    echo "/_/    \__,_/_/\__,_/ |___/\____/\____/_/|_|\____/     "
    echo "==========================================="
    echo "         🕵️  NETWORK SCANNER 🕵️           "
    echo "==========================================="
    echo "1. 🌐 Сканирай локална мрежа"
    echo "2. 🔍 Сканирай портове на IP"
    echo "3. 📡 Покажи мрежови интерфейси"
    echo "4. 🎯 Ping test на IP"
    echo "5. 📊 Покажи мрежова информация"
    echo "6. 🚪 Изход"
    echo "==========================================="
    echo
}

# Сканирай локалната мрежа
function scan_network() {
    echo "🔍 Сканирам локалната мрежа..."
    # Получаваме IP адреса на интерфейса
    LOCAL_IP=$(ip route get 1 | sed -n 's/.*src \([0-9.]*\).*/\1/p')
    NETWORK=$(echo $LOCAL_IP | cut -d. -f1-3).0/24
    echo "📍 Сканирам мрежа: $NETWORK"
    echo "🕐 Това може да отнеме няколко секунди..."
    
    # Проверяваме дали nmap е инсталиран
    if ! command -v nmap &> /dev/null; then
        echo "📦 Инсталирам nmap..."
        sudo apt-get update && sudo apt-get install -y nmap
    fi
    
    echo "=== АКТИВНИ УСТРОЙСТВА ==="
    nmap -sn $NETWORK | grep -E "Nmap scan report|MAC Address" | sed 's/Nmap scan report for /📱 /'
    echo "========================="
}

# Сканирай портове
function scan_ports() {
    echo -n "🎯 Въведи IP адрес за сканиране: "
    read target_ip
    echo "🔍 Сканирам портове на $target_ip..."
    nmap -F $target_ip
}

# Покажи мрежови интерфейси
function show_interfaces() {
    echo "📡 Мрежови интерфейси:"
    ip addr show
    echo
    echo "Press Enter to continue..."
    read
}

# Ping test
function ping_test() {
    echo -n "🎯 Въведи IP адрес за ping: "
    read target_ip
    echo "📡 Ping тест към $target_ip..."
    ping -c 4 $target_ip
    echo
    echo "Press Enter to continue..."
    read
}

# Покажи мрежова информация
function network_info() {
    echo "📊 Мрежова информация:"
    echo "====================================="
    echo "🔗 Активни връзки:"
    netstat -tuln
    echo
    echo "🌐 Routing таблица:"
    ip route
    echo
    echo "📈 Мрежова статистика:"
    cat /proc/net/dev
    echo
    echo "Press Enter to continue..."
    read
}

while true; do
    show_menu
    echo -n "Избери опция (1-6): "
    read choice

    case $choice in
        1) scan_network
           echo
           echo "Press Enter to continue..."
           read ;;
        2) scan_ports
           echo
           echo "Press Enter to continue..."
           read ;;
        3) show_interfaces ;;
        4) ping_test ;;
        5) network_info ;;
        6) break ;;
        *) echo "❌ Невалидна опция! Избери 1-6"
           sleep 2 ;;
    esac
done

echo "👋 Чао от Палаво Око! Мрежата е под контрол! 🕵️"
