#!/bin/sh

set -- $SSH_ORIGINAL_COMMAND
CMD="$1"
IFNAME="$2"


log_cmd() {
    logger -t ha-commands "Command: $CMD, Interface: $IFNAME, From: $SSH_CLIENT"
}

# Validate interface exists before proceeding
check_wireless() {
    uci show wireless."$IFNAME" >/dev/null 2>&1 || {
        logger -t ha-commands "Wireless section '$IFNAME' not found"
        echo "Wireless section '$IFNAME' not found"
        exit 1
    }
}

check_network() {
    uci show network."$IFNAME" >/dev/null 2>&1 || {
        logger -t ha-commands "Network section '$IFNAME' not found"
        echo "Network section '$IFNAME' not found"
        exit 1
    }
}


# Allow only safe interface names: letters, numbers, underscore, hyphen
echo "$IFNAME" | grep -Eq '^[a-zA-Z0-9_-]+$' || {
    echo "Invalid interface name: $1 $2"
    exit 1
}


case "$CMD" in
    wifi-up)
        check_wireless
        log_cmd
        uci set wireless."$IFNAME".disabled=0
        uci commit wireless
        wifi reload
        ;;

    wifi-down)
        check_wireless
        log_cmd
        uci set wireless."$IFNAME".disabled=1
        uci commit wireless
        wifi reload
        ;;

    wifi-status)
        check_wireless
        log_cmd	
        uci get wireless."$IFNAME".disabled 2>/dev/null || echo 0
        ;;

    network-up)
        check_network
        log_cmd
        uci set network."$IFNAME".disabled=0
        uci commit network
        /etc/init.d/network reload
        ;;

    network-down)
        check_network
        log_cmd	
        uci set network."$IFNAME".disabled=1
        uci commit network
        /etc/init.d/network reload
        ;;

    network-status)
        check_network
        log_cmd	
        uci get network."$IFNAME".disabled 2>/dev/null || echo 0
        ;;

    *)
        echo "Command not allowed"
        exit 1
        ;;
esac
