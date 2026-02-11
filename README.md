# Setup


This kit uses the **jayofelony Pwnagotchi firmware**.

Users are responsible for downloading and flashing the firmware themselves.

Firmware installation guide:
[https://github.com/jayofelony/pwnagotchi/wiki/Step-1-Installation-for-raspberry-pi](https://github.com/jayofelony/pwnagotchi/wiki/Step-1-Installation-for-raspberry-pi)

**Hardware:** Raspberry Pi Zero 2 W

Download the **latest 64-bit image** from the jayofelony releases.

---

## Custom plugin installation

After flashing the firmware, insert the SD card into your computer.

The SD card must be mounted at:

```
/media/$USER/
├── bootfs
└── rootfs
```

This is the default mount layout on most Linux systems when flashing Raspberry
Pi images. The install script relies on this layout to place files correctly.

---

### Install steps

Clone this repository and enter the provisioning directory:

```bash
git clone <this-repo>
cd <this-repo>/provision
```

Run the install script **with sudo**:

```bash
sudo ./install_to_rootfs.sh
```

⚠️ **Important:**
The script uses the user that invoked `sudo` to determine the mount path.
Make sure the root filesystem is mounted at:

```
/media/<your-username>/rootfs
```

If this path is incorrect, the script will fail safely.

---

## First boot and AUTO mode

After installation:

1. Insert the SD card into the Pwnagotchi
2. Power it on
3. Open the web UI (usually):

   ```
   http://pwnagotchi.local:8080
   ```

On a **fresh install**, Pwnagotchi may initially boot into **MANU mode**.
This is expected behavior.

To start active operation:

* In the web UI, select **Restart in AUTO mode**

After this restart, AUTO mode should persist across reboots.

---

## Artwork license

All images in the `octopus_images` directory are original artwork.

**License:** CC-BY 4.0

---

## Firmware license

This project uses the **jayofelony Pwnagotchi firmware**, licensed under
the **GNU General Public License v3 (GPL-3.0)**.

This repository **does not** redistribute the firmware or modified binaries.
It contains only:

* documentation
* configuration examples
* provisioning scripts
* original artwork and assets

Firmware source code is available at:
[https://github.com/jayofelony/pwnagotchi](https://github.com/jayofelony/pwnagotchi)

