#!/bin/sh

set -- $SSH_ORIGINAL_COMMAND
CMD="$1"
IFNAME="$2"


# Allow only safe interface names: letters, numbers, underscore, hyphen
echo "$IFNAME" | grep -Eq '^[a-zA-Z0-9_-]+$' || {
    echo "Invalid interface name: $1 $2"
    exit 1
}


case "$CMD" in
    wifi-up)
        uci set wireless."$IFNAME".disabled=0
        uci commit wireless
        wifi reload
        ;;

    wifi-down)
        uci set wireless."$IFNAME".disabled=1
        uci commit wireless
        wifi reload
        ;;

    wifi-status)
        uci get wireless."$IFNAME".disabled 2>/dev/null || echo 0
        ;;

    *)
        echo "Command not allowed"
        exit 1
        ;;
esac
