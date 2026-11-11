import os, json, subprocess
from hardware import PERFILES_SO, MODELOS_CPU, OPCIONES_RAM, OPCIONES_VRAM, TARJETAS_GRAFICAS, PLACAS_BASE

CARPETA_BASE = r"C:\Mis_Maquinas_Virtuales"
RUTA_QEMU = r"C:\Program Files\qemu\qemu-system-x86_64.exe"
RUTA_IMG = r"C:\Program Files\qemu\qemu-img.exe"
procesos_activos = {}

def preparar_carpetas():
    os.makedirs(CARPETA_BASE, exist_ok=True)

def listar_vms():
    return [d for d in os.listdir(CARPETA_BASE) if os.path.isdir(os.path.join(CARPETA_BASE, d))]

def guardar_config(nombre, datos):
    with open(os.path.join(CARPETA_BASE, nombre, "config.json"), "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)

def leer_config(nombre):
    ruta = os.path.join(CARPETA_BASE, nombre, "config.json")
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def gestionar_snapshot(nombre, accion, tag=""):
    disco = os.path.join(CARPETA_BASE, nombre, "disco.qcow2")
    if not os.path.exists(disco):
        return []
    if accion == "listar":
        res = subprocess.run([RUTA_IMG, "snapshot", "-l", disco], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return [l.split() for l in res.stdout.splitlines()[2:] if len(l.split()) >= 2]
    elif accion == "crear" and tag:
        subprocess.run([RUTA_IMG, "snapshot", "-c", tag, disco], creationflags=subprocess.CREATE_NO_WINDOW)
    elif accion == "restaurar" and tag:
        subprocess.run([RUTA_IMG, "snapshot", "-a", tag, disco], creationflags=subprocess.CREATE_NO_WINDOW)

def arrancar_qemu(nombre, cfg, usar_iso):
    disco = os.path.join(CARPETA_BASE, nombre, "disco.qcow2")
    if not os.path.exists(disco):
        subprocess.run([RUTA_IMG, "create", "-f", "qcow2", disco, f"{cfg['disco']}G"], creationflags=subprocess.CREATE_NO_WINDOW)

    cpu = MODELOS_CPU[cfg["cpu"]]
    if cpu == "host" and not cfg["acel"]:
        cpu = "SandyBridge"

    perfil = PERFILES_SO.get(cfg["perfil"], PERFILES_SO["Windows Vista / 7"])
    placa = PLACAS_BASE[cfg["placa"]]
    cmd = [
        RUTA_QEMU, "-name", nombre, "-machine", placa,
        "-m", OPCIONES_RAM[cfg["ram"]], "-smp", cfg["nucleos"], "-cpu", cpu,
        "-hda", disco, "-vga", TARJETAS_GRAFICAS[cfg["gpu"]]
    ]

    # Carpeta compartida (QEMU la monta como disco secundario FAT virtual)
    carpeta_comp = cfg.get("compartida", "")
    if carpeta_comp and os.path.exists(carpeta_comp):
        cmd.extend(["-hdb", f"fat:rw:{carpeta_comp}"])

    # Disquete o imagen .img
    ruta_img = cfg.get("img", "")
    if ruta_img and os.path.exists(ruta_img):
        cmd.extend(["-fda", ruta_img])

    if placa != "isapc":
        cmd.extend(["-net", f"nic,model={perfil['red']}", "-net", "user"])
    if TARJETAS_GRAFICAS[cfg["gpu"]] in ["std", "vmware"]:
        cmd.extend(["-global", f"VGA.vgamem_mb={OPCIONES_VRAM[cfg['vram']]}"])
    if cfg["sonido"] and placa != "isapc":
        cmd.extend(["-device", "AC97"] if perfil["sonido"] == "AC97" else ["-device", "ich9-intel-hda", "-device", "hda-duplex"])
    if cfg["acel"]:
        cmd.extend(["-accel", "whpx,kernel-irqchip=off"])
    cmd.extend(["-cdrom", cfg["iso"], "-boot", "d"] if usar_iso else ["-boot", "c"])

    procesos_activos[nombre] = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
