import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os, shutil
from hardware import PERFILES_SO, MODELOS_CPU, OPCIONES_RAM, OPCIONES_VRAM, TARJETAS_GRAFICAS, PLACAS_BASE
import motor

motor.preparar_carpetas()
v = tk.Tk()
v.title("Multi-OS Virtual Machine Manager Pro v2.0")
v.geometry("560x650")
v.configure(bg="#e8f1f5")

def vm_actual():
    return c_vm.get().strip("{}")

def actualizar_lista(sel=None):
    vms = motor.listar_vms()
    c_vm["values"] = vms
    c_vm.set(sel if sel in vms else (vms if vms else ""))
    cargar_datos()

def cargar_datos(e=None):
    nom = vm_actual()
    d = motor.leer_config(nom) if nom else {}
    c_perf.set(d.get("perfil", "Windows Vista / 7"))
    c_cpu.set(d.get("cpu", "Intel Core i7 Haswell"))
    c_ram.set(d.get("ram", "4096 MB (4 GB)"))
    c_nuc.set(d.get("nucleos", "4"))
    c_gpu.set(d.get("gpu", "Estándar VGA"))
    c_vram.set(d.get("vram", "128 MB"))
    c_plac.set(d.get("placa", "Intel i440FX (Clásica PCI)"))
    s_disc.delete(0, "end"); s_disc.insert(0, d.get("disco", "30"))
    v_acel.set(d.get("acel", True)); v_son.set(d.get("sonido", True))
    e_iso.delete(0, tk.END); e_iso.insert(0, d.get("iso", ""))
    e_img.delete(0, tk.END); e_img.insert(0, d.get("img", ""))
    e_comp.delete(0, tk.END); e_comp.insert(0, d.get("compartida", ""))
    actualizar_snaps()

def actualizar_snaps():
    nom = vm_actual()
    snaps = motor.gestionar_snapshot(nom, "listar") if nom else []
    c_snap["values"] = snaps
    c_snap.set(snaps[-1] if snaps else "")

def crear_snap():
    nom = vm_actual()
    if not nom: return
    if nom in motor.procesos_activos and motor.procesos_activos[nom].poll() is None:
        return messagebox.showwarning("Aviso", "Apaga la máquina virtual antes de crear un Snapshot.")
    tag = simpledialog.askstring("Nuevo Snapshot", "Nombre del punto de restauración (sin espacios):")
    if tag:
        motor.gestionar_snapshot(nom, "crear", tag.replace(" ", "_"))
        actualizar_snaps()
        messagebox.showinfo("Snapshot", f"Punto '{tag}' guardado.")

def restaurar_snap():
    nom, tag = vm_actual(), c_snap.get()
    if not nom or not tag: return
    if nom in motor.procesos_activos and motor.procesos_activos[nom].poll() is None:
        return messagebox.showwarning("Aviso", "Apaga la máquina virtual antes de restaurar.")
    if messagebox.askyesno("Restaurar", f"¿Volver al estado '{tag}'?"):
        motor.gestionar_snapshot(nom, "restaurar", tag)
        messagebox.showinfo("Restaurado", f"Máquina restaurada a '{tag}'.")

def aplicar_plantilla(e=None):
    p = PERFILES_SO.get(c_perf.get())
    if p:
        c_cpu.set(p["cpu"]); c_ram.set(p["ram"]); c_gpu.set(p["gpu"])
        for k, val in PLACAS_BASE.items():
            if val == p["placa"]: c_plac.set(k)

def nueva_vm():
    nom = simpledialog.askstring("Nueva VM", "Nombre de la máquina (ej. Ubuntu, WinXP):")
    if nom:
        nom_l = "".join(c for c in nom if c.isalnum() or c in (" ", "-", "_")).strip()
        if nom_l:
            os.makedirs(os.path.join(motor.CARPETA_BASE, nom_l), exist_ok=True)
            actualizar_lista(nom_l)

def borrar_vm():
    nom = vm_actual()
    if nom and messagebox.askyesno("Borrar", f"¿Eliminar '{nom}'?"):
        shutil.rmtree(os.path.join(motor.CARPETA_BASE, nom), ignore_errors=True)
        actualizar_lista()

def iniciar(usar_iso):
    nom = vm_actual()
    if not nom: return messagebox.showwarning("Aviso", "Crea o elige una VM primero.")
    if usar_iso and not os.path.exists(e_iso.get()): return messagebox.showerror("Error", "Selecciona una ISO válida.")
    cfg = {
        "perfil": c_perf.get(), "cpu": c_cpu.get(), "ram": c_ram.get(), "nucleos": c_nuc.get(),
        "gpu": c_gpu.get(), "vram": c_vram.get(), "placa": c_plac.get(), "disco": s_disc.get() or "30",
        "acel": v_acel.get(), "sonido": v_son.get(), "iso": e_iso.get(),
        "img": e_img.get(), "compartida": e_comp.get()
    }
    try:
        motor.guardar_config(nom, cfg)
        motor.arrancar_qemu(nom, cfg, usar_iso)
        lbl_est.config(text=f"Estado: {nom} ejecutándose", fg="green")
    except Exception as err:
        messagebox.showerror("Error", str(err))

def apagar():
    nom = vm_actual()
    if nom in motor.procesos_activos and motor.procesos_activos[nom].poll() is None:
        motor.procesos_activos[nom].terminate()
        lbl_est.config(text=f"Estado: {nom} apagada", fg="red")

f1 = tk.Frame(v, bg="#e8f1f5"); f1.pack(pady=8)
c_vm = ttk.Combobox(f1, state="readonly", width=28); c_vm.pack(side="left", padx=5); c_vm.bind("<<ComboboxSelected>>", cargar_datos)
tk.Button(f1, text="+ Nueva VM", bg="#0078d7", fg="white", command=nueva_vm).pack(side="left", padx=3)
tk.Button(f1, text="Borrar", bg="#d9534f", fg="white", command=borrar_vm).pack(side="left", padx=3)

f_sn = tk.LabelFrame(v, text=" Snapshots (Puntos de Restauración) ", bg="#e8f1f5", padx=8, pady=4)
f_sn.pack(fill="x", padx=25, pady=3)
c_snap = ttk.Combobox(f_sn, state="readonly", width=26); c_snap.pack(side="left", padx=5)
tk.Button(f_sn, text="Guardar Snapshot", bg="#6f42c1", fg="white", command=crear_snap).pack(side="left", padx=4)
tk.Button(f_sn, text="Restaurar", bg="#fd7e14", fg="white", command=restaurar_snap).pack(side="left", padx=4)

def fila_archivo(texto_btn, comando):
    f = tk.Frame(v, bg="#e8f1f5"); f.pack(pady=3, fill="x", padx=25)
    e = tk.Entry(f); e.pack(side="left", expand=True, fill="x", padx=(0, 5))
    tk.Button(f, text=texto_btn, width=16, command=lambda: [e.delete(0, tk.END), e.insert(0, comando())]).pack(side="right")
    return e

e_iso = fila_archivo("Buscar ISO (CD)", lambda: filedialog.askopenfilename(filetypes=[("ISO", "*.iso"), ("Todos", "*.*")]))
e_img = fila_archivo("Disquete (.IMG)", lambda: filedialog.askopenfilename(filetypes=[("Imagen IMG", "*.img;*.ima;*.flp"), ("Todos", "*.*")]))
e_comp = fila_archivo("Carpeta Compartida", lambda: filedialog.askdirectory())

f3 = tk.Frame(v, bg="#e8f1f5"); f3.pack(pady=6)
def fila(txt, vals, r, w=32):
    tk.Label(f3, text=txt, bg="#e8f1f5").grid(row=r, column=0, sticky="w", pady=3)
    cb = ttk.Combobox(f3, values=list(vals), state="readonly", width=w); cb.grid(row=r, column=1, padx=8, pady=3)
    return cb

c_perf = fila("Plantilla Sistema:", PERFILES_SO.keys(), 0); c_perf.bind("<<ComboboxSelected>>", aplicar_plantilla)
c_cpu = fila("Procesador CPU:", MODELOS_CPU.keys(), 1)
c_ram = fila("Memoria RAM:", OPCIONES_RAM.keys(), 2)
c_nuc = fila("Núcleos CPU:", [str(i) for i in range(1, 13)], 3)
c_plac = fila("Placa Base:", PLACAS_BASE.keys(), 4)
c_gpu = fila("Tarjeta Gráfica:", TARJETAS_GRAFICAS.keys(), 5)
c_vram = fila("Memoria VRAM:", OPCIONES_VRAM.keys(), 6)

tk.Label(f3, text="Disco Duro (GB):", bg="#e8f1f5").grid(row=7, column=0, sticky="w", pady=3)
s_disc = tk.Spinbox(f3, from_=1, to=500, width=10); s_disc.grid(row=7, column=1, sticky="w", padx=8)

v_acel = tk.BooleanVar(value=True)
tk.Checkbutton(v, text="Aceleración WHPX (Velocidad rápida)", variable=v_acel, bg="#e8f1f5").pack()
v_son = tk.BooleanVar(value=True)
tk.Checkbutton(v, text="Activar Tarjeta de Sonido", variable=v_son, bg="#e8f1f5").pack()

f4 = tk.Frame(v, bg="#e8f1f5"); f4.pack(pady=10)
tk.Button(f4, text="Arrancar con ISO", bg="#0078d7", fg="white", width=16, height=2, command=lambda: iniciar(True)).pack(side="left", padx=5)
tk.Button(f4, text="Iniciar desde Disco", bg="#28a745", fg="white", width=16, height=2, command=lambda: iniciar(False)).pack(side="left", padx=5)
tk.Button(f4, text="Apagar VM", bg="#d9534f", fg="white", width=12, height=2, command=apagar).pack(side="left", padx=5)

lbl_est = tk.Label(v, text="Estado: Listo", bg="#e8f1f5", font=("Segoe UI", 9, "bold")); lbl_est.pack()
actualizar_lista()
v.mainloop()
