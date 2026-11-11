PERFILES_SO = {
    "Windows XP (32-bit)": {
        "placa": "pc", "red": "rtl8139", "sonido": "AC97",
        "ram": "1024 MB (1 GB)", "cpu": "Intel Atom N270", "gpu": "Estándar VGA"
    },
    "Windows Vista / 7": {
        "placa": "pc", "red": "e1000", "sonido": "AC97",
        "ram": "4096 MB (4 GB)", "cpu": "Intel Core 2 Duo", "gpu": "Estándar VGA"
    },
    "Windows 8 / 10 / 11": {
        "placa": "q35", "red": "e1000", "sonido": "ich9-intel-hda",
        "ram": "8192 MB (8 GB)", "cpu": "Intel Core i7 Haswell", "gpu": "VMware SVGA-II"
    },
    "Linux (Ubuntu / Debian / Mint)": {
        "placa": "q35", "red": "e1000", "sonido": "ich9-intel-hda",
        "ram": "4096 MB (4 GB)", "cpu": "AMD EPYC / Ryzen", "gpu": "VirtIO GPU (Linux/Moderno)"
    },
    "macOS (Hackintosh / KVM)": {
        "placa": "q35", "red": "e1000", "sonido": "ich9-intel-hda",
        "ram": "8192 MB (8 GB)", "cpu": "Intel Core i7 Haswell", "gpu": "VMware SVGA-II"
    },
    "Otros (MS-DOS / Retro / BSD)": {
        "placa": "isapc", "red": "ne2k_isa", "sonido": "AC97",
        "ram": "16 MB", "cpu": "Intel 486 (Retro)", "gpu": "Cirrus Logic (Retro)"
    }
}

MODELOS_CPU = {
    "Intel 486 (Retro)": "486",
    "Intel Pentium I": "pentium",
    "Intel Pentium II": "pentium2",
    "Intel Pentium III": "pentium3",
    "Intel Atom N270": "n270",
    "Intel Celeron Conroe": "Conroe",
    "Intel Core Duo (32-bit)": "coreduo",
    "Intel Core 2 Duo": "core2duo",
    "Intel Core 2 Quad (Penryn)": "Penryn",
    "Intel Core i7 Nehalem": "Nehalem",
    "Intel Core i7 Sandy Bridge": "SandyBridge",
    "Intel Core i7 Ivy Bridge": "IvyBridge",
    "Intel Core i7 Haswell": "Haswell",
    "Intel Core i7 Broadwell": "Broadwell",
    "Intel Core i7 Skylake": "Skylake-Client",
    "Intel Xeon Westmere": "Westmere",
    "AMD Athlon 64 (qemu64)": "qemu64",
    "AMD Phenom II X4": "phenom",
    "AMD Opteron G5": "Opteron_G5",
    "AMD EPYC / Ryzen": "EPYC",
    "Procesador Real (Host)": "host"
}

OPCIONES_RAM = {
    "1 MB": "1",
    "2 MB": "2",
    "4 MB": "4",
    "8 MB": "8",
    "16 MB": "16",
    "32 MB": "32",
    "64 MB": "64",
    "128 MB": "128",
    "256 MB": "256",
    "512 MB": "512",
    "1024 MB (1 GB)": "1024",
    "2048 MB (2 GB)": "2048",
    "4096 MB (4 GB)": "4096",
    "6144 MB (6 GB)": "6144",
    "8192 MB (8 GB)": "8192"
}

OPCIONES_VRAM = {
    "1 MB": "1",
    "2 MB": "2",
    "4 MB": "4",
    "8 MB": "8",
    "16 MB": "16",
    "32 MB": "32",
    "64 MB": "64",
    "128 MB": "128"
}

TARJETAS_GRAFICAS = {
    "Estándar VGA": "std",
    "VMware SVGA-II": "vmware",
    "QXL (Gráficos SPICE)": "qxl",
    "VirtIO GPU (Linux/Moderno)": "virtio",
    "Cirrus Logic (Retro)": "cirrus"
}

PLACAS_BASE = {
    "Intel i440FX (Clásica PCI)": "pc",
    "Intel Q35 (Moderna PCI-Express)": "q35",
    "ISA PC (Retro 1980s/90s - Sin PCI)": "isapc"
}
