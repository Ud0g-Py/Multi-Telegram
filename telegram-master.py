import os
import subprocess
import shutil
from termcolor import colored

def count_profiles_and_running():
    profiles = [name for name in os.listdir('.') if os.path.isdir(name) and name.startswith('TelegramStack_')]
    running_profiles = []
    try:
        for profile in profiles:
            process = subprocess.Popen(['pgrep', '-f', profile], stdout=subprocess.PIPE)
            output, _ = process.communicate()
            if output:
                running_profiles.append(profile)
    except Exception as e:
        print(colored(f"Error al contar los perfiles en ejecución: {e}", 'red'))
    return profiles, running_profiles

def create_profile(profiles_count):
    profile_name = f"TelegramStack_{profiles_count + 1}"
    original_path = "./Telegram"
    destination_path = profile_name

    os.mkdir(destination_path)
    for file_name in os.listdir(original_path):
        shutil.copy(os.path.join(original_path, file_name), destination_path)
    os.mkdir(os.path.join(destination_path, "TelegramForcePortable"))

    print(colored(f"Perfil {profile_name} creado.", 'green'))

def start_profile(profiles, running_profiles):
    for profile in profiles:
        if profile not in running_profiles:
            profile_path = os.path.join(profile, "Telegram")
            subprocess.Popen(['nohup', profile_path, '&'])
            print(colored(f"Iniciando {profile}...", 'green'))
            break
    else:
        print(colored("Todos los perfiles ya están en ejecución.", 'yellow'))

def stop_profiles(profiles):
    for profile in profiles:
        subprocess.call(['pkill', '-f', profile])
    print(colored("Todos los perfiles han sido detenidos.", 'yellow'))

def update_profiles(profiles):
    for profile in profiles:
        updater_path = os.path.join(profile, "Updater")
        subprocess.Popen(['nohup', updater_path, '&'])
    print(colored("Todos los perfiles están siendo actualizados.", 'green'))

def print_menu():
    profiles, running_profiles = count_profiles_and_running()
    print(colored("Menú:", 'cyan'))
    print(colored(f"Perfiles en el directorio: {len(profiles)}", 'yellow'))
    if running_profiles:
        print(colored(f"En ejecución: {', '.join(running_profiles)}", 'green'))
    print("1. Crear un perfil adicional")
    print("2. Iniciar un perfil")
    print("3. Detener todos los perfiles")
    print("4. Actualizar todos los perfiles")
    print("5. Salir")

def main():
    while True:
        print_menu()
        choice = input("Seleccione una opción: ")
        profiles, running_profiles = count_profiles_and_running()
        if choice == '1':
            create_profile(len(profiles))
        elif choice == '2':
            start_profile(profiles, running_profiles)
        elif choice == '3':
            stop_profiles(profiles)
        elif choice == '4':
            update_profiles(profiles)
        elif choice == '5':
            break
        else:
            print(colored("Opción inválida. Intente de nuevo.", 'red'))

if __name__ == "__main__":
    main()