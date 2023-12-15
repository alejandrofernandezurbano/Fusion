import numpy as np

# La transformación original
original_transform = np.array([
    [1, 0, 0, -0.118], #X  →-  ←+
    [0, 0, -1, -0.145],           #Y  ↑+  ↓-
    [0, 1, 0, 0.3], #Z  ⬋-  ⬈+
    [0, 0, 0, 1]
])

# Matriz de rotación en X (11 grados)
angle_x = -15.6 * np.pi / 180
R_X = np.array([
    [1, 0, 0, 0],
    [0, np.cos(angle_x), -np.sin(angle_x), 0],
    [0, np.sin(angle_x), np.cos(angle_x), 0],
    [0, 0, 0, 1]
])

# Matriz de rotación en Y (por ejemplo, 30 grados)
angle_y = -4 * np.pi / 180
R_Y = np.array([
    [np.cos(angle_y), 0, np.sin(angle_y), 0],
    [0, 1, 0, 0],
    [-np.sin(angle_y), 0, np.cos(angle_y), 0],
    [0, 0, 0, 1]
])

# Matriz de rotación en Z (por ejemplo, 20 grados)
angle_z = 59* np.pi / 180
R_Z = np.array([
    [np.cos(angle_z), -np.sin(angle_z), 0, 0],
    [np.sin(angle_z), np.cos(angle_z), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

# Realizar las rotaciones multiplicando las matrices en orden X, Y y Z
transform_rotated = np.dot(original_transform, R_X)
transform_rotated = np.dot(transform_rotated, R_Y)
transform_rotated = np.dot(transform_rotated, R_Z)

# Eliminar la última fila que es [0, 0, 0, 1]
transform_rotated = transform_rotated[:-1, :]

# Formatear los valores en una cadena
formatted_values = [f'{value:.5f}' for value in transform_rotated.flatten()]

# Leer el archivo
file_path = "000134.txt"
with open(file_path, "r") as file:
    lines = file.readlines()

# Buscar la línea que comienza con "Tr_velo_to_cam:" y reemplazarla con los nuevos valores
for i, line in enumerate(lines):
    if line.startswith("Tr_velo_to_cam:"):
        lines[i] = "Tr_velo_to_cam: " + " ".join(formatted_values) + "\n"

# Escribir las líneas modificadas de vuelta al archivo
with open(file_path, "w") as file:
    file.writelines(lines)

print(f"Valores de Tr_velo_to_cam han sido actualizados en el archivo {file_path}.")


