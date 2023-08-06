import psutil
import webbrowser
import tkinter as tk
from tkinter import messagebox
import ctypes
import sys

def AskForAdmin():
    # Check if the current process is running with administrator privileges
    if ctypes.windll.shell32.IsUserAnAdmin():
        print("Process is now running in Admin Mode, be careful!.")
        return

    # Create a shell object
    shell = ctypes.windll.shell32.ShellExecuteW

    # Prompt the user to elevate the process
    ret = shell(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    # Check if the user accepted the elevation prompt
    if ret <= 32:
        print('Failed to elevate Python process, either you clicked "No" or you just do not have admin priviledges. ')
        return

    # Exit the current script
    sys.exit()

def list_all_processes():
    processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
    process_list.delete(0, tk.END)
    for process in processes:
        process_list.insert(tk.END, f"PID: {process.info['pid']}, Name: {process.info['name']}, CPU: {process.info['cpu_percent']}%, Memory: {process.info['memory_percent']}%")

def search_process_by_name():
    name = search_entry.get()
    processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
    process_list.delete(0, tk.END)
    for process in processes:
        if name.lower() in process.info['name'].lower():
            process_list.insert(tk.END, f"PID: {process.info['pid']}, Name: {process.info['name']}, CPU: {process.info['cpu_percent']}%, Memory: {process.info['memory_percent']}%")

def terminate_process():
    try:
        selected_process = process_list.get(process_list.curselection())
        pid = int(selected_process.split()[1])
        process = psutil.Process(pid)
        process.terminate()
        messagebox.showinfo("Process Terminated!", f"Process with PID {pid} terminated successfully.")
    except:
        messagebox.showerror("Uh oh!", "No process selected or failed to terminate process. Do you HAVE admin?")

def search_processes_opening_file():
    file_name = search_entry.get()
    processes = psutil.process_iter(['pid', 'name', 'open_files'])
    process_list.delete(0, tk.END)
    for process in processes:
        for file in process.info['open_files']:
            if file_name.lower() in file.path.lower():
                process_list.insert(tk.END, f"PID: {process.info['pid']}, Name: {process.info['name']}")

def list_processes_using_network():
    connections = psutil.net_connections(kind='inet')
    process_list.delete(0, tk.END)
    for conn in connections:
        if conn.pid:
            process = psutil.Process(conn.pid)
            process_list.insert(tk.END, f"PID: {process.pid}, Name: {process.name()}")

def filter_processes_by_socket_port():
    port = search_entry.get()
    connections = psutil.net_connections(kind='inet')
    process_list.delete(0, tk.END)
    for conn in connections:
        if conn.pid and str(conn.laddr.port) == port:
            process = psutil.Process(conn.pid)
            process_list.insert(tk.END, f"PID: {process.pid}, Name: {process.name()}")

def list_processes_accessing_disk():
    processes = psutil.process_iter(['pid', 'name', 'io_counters'])
    process_list.delete(0, tk.END)
    for process in processes:
        if process.info['io_counters']:
            process_list.insert(tk.END, f"PID: {process.info['pid']}, Name: {process.info['name']}")
            
def list_processes_firewall_status():
    processes = psutil.process_iter(['pid', 'name', 'is_running'])
    process_list.delete(0, tk.END)
    for process in processes:
        if process.info['is_running']:
            process_list.insert(tk.END, f"PID: {process.info['pid']}, Name: {process.info['name']}, Firewall: Allowed")
        else:
            process_list.insert(tk.END, f"PID: {process.info['pid']}, Name: {process.info['name']}, Firewall: Blocked")

def search_process_online():
    selected_process = process_list.get(process_list.curselection())
    process_name = selected_process.split()[3]
    url = f"https://www.google.com/search?q={process_name}+virus"
    webbrowser.open_new(url)

def list_top_processes_resource_usage():
    processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'io_counters'])
    sorted_processes = sorted(processes, key=lambda x: x.info['cpu_percent'], reverse=True)[:10]
    process_list.delete(0, tk.END)
    for process in sorted_processes:
        process_list.insert(tk.END, f"PID: {process.info['pid']}, Name: {process.info['name']}, CPU: {process.info['cpu_percent']}%, Memory: {process.info['memory_percent']}%, Disk IO: {process.info['io_counters'].read_bytes}/{process.info['io_counters'].write_bytes}")

# Create the main window
window = tk.Tk()
window.title("Task Manager Plus")

# Create the search bar
search_label = tk.Label(window, text="Search For a PID or Process Name:")
search_label.pack()

search_entry = tk.Entry(window, width=50)
search_entry.pack()

# Create the process list
process_list = tk.Listbox(window, width=100)
process_list.pack()

# Create the buttons
button_frame = tk.Frame(window)
button_frame.pack()

list_all_button = tk.Button(button_frame, text="List All Processes", command=list_all_processes)
list_all_button.grid(row=0, column=0, padx=5, pady=5)

search_button = tk.Button(button_frame, text="Search Process by Name", command=search_process_by_name)
search_button.grid(row=0, column=1, padx=5, pady=5)

terminate_button = tk.Button(button_frame, text="Terminate Process", command=terminate_process)
terminate_button.grid(row=0, column=2, padx=5, pady=5)

search_file_button = tk.Button(button_frame, text="Search Processes Opening File", command=search_processes_opening_file)
search_file_button.grid(row=0, column=3, padx=5, pady=5)

network_button = tk.Button(button_frame, text="List Processes Using Network", command=list_processes_using_network)
network_button.grid(row=1, column=0, padx=5, pady=5)

filter_port_button = tk.Button(button_frame, text="Filter Processes by Socket Port", command=filter_processes_by_socket_port)
filter_port_button.grid(row=1, column=1, padx=5, pady=5)

disk_button = tk.Button(button_frame, text="List Processes Accessing Disk", command=list_processes_accessing_disk)
disk_button.grid(row=1, column=2, padx=5, pady=5)

firewall_button = tk.Button(button_frame, text="List Processes Firewall Status", command=list_processes_firewall_status)
firewall_button.grid(row=1, column=3, padx=5, pady=5)

search_online_button = tk.Button(button_frame, text="Search Process Online", command=search_process_online)
search_online_button.grid(row=2, column=0, padx=5, pady=5)

top_processes_button = tk.Button(button_frame, text="List Top Processes Resource Usage", command=list_top_processes_resource_usage)
top_processes_button.grid(row=2, column=1, padx=5, pady=5)

# Run the main event loop
AskForAdmin() #just to ask for admin to be able to terminate processes
messagebox.showinfo("Credits", "Coded by @developerlaborotory on github, you probably don't care but yeah...") # credits, remove if you want, but I did try hard.
window.mainloop() # to start tkinter, otherwise this program would be useless.
list_all_processes() # just so you can see it when it starts I guess.

