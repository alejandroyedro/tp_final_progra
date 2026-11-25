"""Autenticación y gestión de usuarios."""

from .archivos_csv import escribir_registro, leer_registros, ruta_archivo
from .funciones import recortar


USUARIO_INICIAL = "Pedro"  
CONTRASENIA_INICIAL = "1234"  


def validar_contrasenia(contra_usu: str, contra_regis: str) -> bool:
    '''
    Valida si la contraseña de usuario es igual a la registrada
    
    Args: 
    contra_usu (str): Recibe la contraseña de usuario
    contra_regis (str): Recibe la contraseña a comparar

    Returns:
    bool: True si las contraseñas coinciden, False si no
    '''
    return contra_usu == contra_regis

def validar_usuario(nombre_usuario: str, usuario_registrado: str) -> bool:

    """Compara el nombre ingresado con el nombre registrado.

    Args:
        nombre_usuario (str): Nombre de usuario ingresado.
        usuario_registrado (str): Nombre del usuario registrado con el que se compara.

    Returns:
        bool: True si se cumple la condición indicada; False en caso contrario.
    """

    return (nombre_usuario) == (usuario_registrado)


def guardar_usuarios(usuarios: list) -> None:  
    """Guarda usuarios a usuarios.csv con encabezados.

    Args:
        usuarios (list): Lista de usuarios registrados.

    Returns:
        No devuelve un valor.
    """

    archivo = open(ruta_archivo("usuarios.csv"), "w", encoding="utf-8", newline="")    
    escribir_registro(archivo, ["usuario", "contrasenia"])    
    i = 0

    while i < len(usuarios):        
        escribir_registro(archivo, usuarios[i])        
        i = i + 1

    archivo.close()


def cargar_usuarios() -> list | None:  
    """Carga usuarios de usuarios.csv o crea archivo con usuario inicial.

    Returns:
        list | None: Usuarios leídos, o None si el archivo CSV no es válido.
    """

    archivo = open(ruta_archivo("usuarios.csv"), "a")

    archivo.close()

    archivo = open(ruta_archivo("usuarios.csv"), "r", encoding="utf-8", newline="")
    
    registros = leer_registros(archivo)

    usuarios = []

    if registros != None:
        for registro in registros[1:]:
            if len(registro) == 2:
                usuarios += [registro]
    else:
        usuarios = None
    
    archivo.close()

    if usuarios != None and len(usuarios) == 0:

        usuarios = [[USUARIO_INICIAL, CONTRASENIA_INICIAL]]

        guardar_usuarios(usuarios)
    
    return usuarios


def registrar_usuario(usuario: str, contrasenia: str) -> tuple:  
    """Crea tupla con datos de nuevo usuario.

    Args:
        usuario (str): Nombre del usuario.
        contrasenia (str): Contraseña del usuario.

    Returns:
        tuple: Tupla con el nombre y la contraseña.
    """
    
    return (usuario, contrasenia)


def buscar_usuario(usuarios: list, nombre: str) -> int:  
    """Busca usuario y retorna índice (-1 si no existe).

    Args:
        usuarios (list): Lista de usuarios registrados.
        nombre (str): Nombre que se utiliza en la operación.

    Returns:
        int: Índice del usuario, o -1 si no se encuentra.
    """

    i = 0
    resultado = -1

    while i < len(usuarios) and resultado == -1:

        if validar_usuario(usuarios[i][0], nombre):
            resultado = i

        i = i + 1

    return resultado


def autenticar(usuarios: list) -> None:  
    """Gestiona registro/login completo del usuario.

    Args:
        usuarios (list): Lista de usuarios registrados.

    Returns:
        No devuelve un valor.
    """

    autenticado = False

    while autenticado == False:
        print("--- REGISTRO O INICIO DE SESIÓN ---")

        nombre_usuario = recortar(input("Ingrese su nombre de usuario: "))
        posicion = buscar_usuario(usuarios, nombre_usuario)
        
        if posicion != -1:

            print("--- INICIO DE SESIÓN ---")

            contraseña = input("Ingrese su contraseña: ")

            if validar_contrasenia(contraseña, usuarios[posicion][1]):
                
                print(f"Bienvenido, {nombre_usuario}.")
                
                autenticado = True
        
        else:
            
            print("--- REGISTRO ---")
            
            nueva_contrasenia = input("Ingrese su contraseña: ")
            
            datos = list(registrar_usuario(nombre_usuario, nueva_contrasenia))
            
            usuarios += [datos]
            
            guardar_usuarios(usuarios)
        
            print("Usuario registrado correctamente.")
            
            print("--- INICIO DE SESIÓN ---")
            
            
            login_exitoso = False
            
            while login_exitoso == False:
                
                nombre_usuario_login = recortar(input("Ingrese su nombre de usuario: "))
                
                contraseña_login = input("Ingrese su contraseña: ")
                
                posicion_login = buscar_usuario(usuarios, nombre_usuario_login)
                
                if posicion_login != -1 and validar_contrasenia(contraseña_login, usuarios[posicion_login][1]):                    
                    print(f"Bienvenido, {nombre_usuario_login}.")                    
                    login_exitoso = True                    
                    autenticado = True
                else:
                    print("Usuario o contraseña incorrectos.")
