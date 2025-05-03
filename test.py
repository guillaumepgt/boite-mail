import tkinter as tk
from tkinter import ttk
import asyncio
import threading
import queue
from fonction.recevoir_mail import *
import json


# Création de la file de communication
update_queue = queue.Queue()

# Simulation d'une tâche asynchrone (ex: récupération de mails)
async def receive_messages():
    data = recevoir_email()
    os.makedirs('mail', exist_ok=True)
    # Écriture fichier de manière "bloquante" dans un thread séparé
    json.dump(data, open(f"mail/mail.json", "w"))
    update_queue.put("True")

# Traitement dans l'interface Tkinter à intervalles réguliers
def process_queue():
    try:
        while True:
            message = update_queue.get_nowait()
            # Mettre à jour l'interface ici
            messages_list.insert(tk.END, message)
    except queue.Empty:
        pass
    root.after(100, process_queue)  # continuer à vérifier la queue

# Lancement de l'event loop asyncio dans un thread séparé
def start_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(receive_messages())

# Interface graphique Tkinter
root = tk.Tk()
messages_list = tk.Listbox(root)
messages_list.pack()

# Démarrer le thread asyncio
threading.Thread(target=start_async_loop, daemon=True).start()

# Démarrer la vérification régulière de la file
root.after(100, process_queue)

root.mainloop()
