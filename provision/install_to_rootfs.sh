#!/usr/bin/env bash
set -euo pipefail

: "${SUDO_USER:?Must be run via sudo}"
ROOTFS="/media/$SUDO_USER/rootfs"

if [[ ! -d "$ROOTFS/etc" ]]; then
  echo "Rootfs not found at $ROOTFS"
  exit 1
fi

echo "[*] Installing config.toml"
install -m 644 config.toml \
  "$ROOTFS/etc/pwnagotchi/config.toml"

echo "[*] Installing octopus_swap.py"
install -m 755 octopus_swap.py \
  "$ROOTFS/usr/local/share/pwnagotchi/custom-plugins/octopus_swap.py"

echo "[*] Installing octopus images"
mkdir -p \
  "$ROOTFS/usr/local/share/pwnagotchi/custom-assets/faces"

unzip -o octopus_images.zip \
  -d "$ROOTFS/usr/local/share/pwnagotchi/custom-assets/faces"

echo "[*] Syncing filesystem"
sync

echo "[✓] Rootfs installation complete"

