import numpy as np
import tkinter as tk
from tkinter import Scale, Button

# Función para actualizar el archivo de calibración con los nuevos valores
def actualizar_calibracion(event):
    # Obtener los valores de rotación y traslación desde los sliders
    rotacion_x = rot_x_slider.get()* np.pi / 180
    rotacion_y = rot_y_slider.get()* np.pi / 180
    rotacion_z = rot_z_slider.get()* np.pi / 180
    traslacion_x = trans_x_slider.get()
    traslacion_y = trans_y_slider.get()
    traslacion_z = trans_z_slider.get()

    # Crear las matrices de rotación
    R_X = np.array([
        [1, 0, 0, 0],
        [0, np.cos(rotacion_x), -np.sin(rotacion_x), 0],
        [0, np.sin(rotacion_x), np.cos(rotacion_x), 0],
        [0, 0, 0, 1]
    ])
    
    R_Y = np.array([
        [np.cos(rotacion_y), 0, np.sin(rotacion_y), 0],
        [0, 1, 0, 0],
        [-np.sin(rotacion_y), 0, np.cos(rotacion_y), 0],
        [0, 0, 0, 1]
    ])
    
    R_Z = np.array([
        [np.cos(rotacion_z), -np.sin(rotacion_z), 0, 0],
        [np.sin(rotacion_z), np.cos(rotacion_z), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    # Realizar las rotaciones multiplicando las matrices en orden X, Y y Z
    transform_rotated = np.dot(original_transform, R_X)
    transform_rotated = np.dot(transform_rotated, R_Y)
    transform_rotated = np.dot(transform_rotated, R_Z)

    # Aplicar la traslación
    transform_rotated[0, 3] += traslacion_x
    transform_rotated[1, 3] += traslacion_y
    transform_rotated[2, 3] += traslacion_z

    # Eliminar la última fila que es [0, 0, 0, 1]
    transform_rotated = transform_rotated[:-1, :]

    # Formatear los valores en una cadena
    formatted_values = [f'{value:.5f}' for value in transform_rotated.flatten()]

    # Escribir los valores en el archivo de calibración
    with open(file_path, "w") as file:
        for i, line in enumerate(lines):
            if line.startswith("Tr_velo_to_cam:"):
                file.write("Tr_velo_to_cam: " + " ".join(formatted_values) + "\n")
            else:
                file.write(line)

    print(f"Valores de Tr_velo_to_cam han sido actualizados en el archivo {file_path}.")

# Función para aumentar el valor del slider
def aumentar_slider(slider):
    valor_actual = slider.get()
    slider.set(valor_actual + 0.05)

# Función para disminuir el valor del slider
def disminuir_slider(slider):
    valor_actual = slider.get()
    slider.set(valor_actual - 0.05)

# Crear la ventana de la interfaz gráfica
root = tk.Tk()
root.title("Ajuste de Calibración")

# La transformación original
original_transform = np.array([
    [0, -1, 0, 0],
    [0, 0, -1, 0],
    [1, 0, 0, 0],
    [0, 0, 0, 1]
])

# Leer el archivo de calibración
file_path = "000134.txt"
with open(file_path, "r") as file:
    lines = file.readlines()

# Sliders para ajustar los valores de rotación y traslación
rot_x_slider = Scale(root, label="Rotación X (grados)", from_=-310, to=310, orient="horizontal",resolution=0.05, length=300)
rot_x_slider.pack()

rot_y_slider = Scale(root, label="Rotación Y (grados)", from_=-35, to=35, orient="horizontal",resolution=0.05, length=300)
rot_y_slider.pack()

rot_z_slider = Scale(root, label="Rotación Z (grados)", from_=-360, to=360, orient="horizontal",resolution=0.05, length=300)
rot_z_slider.pack()

trans_x_slider = Scale(root, label="Traslación X", from_=-1, to=1, orient="horizontal", resolution=0.001, length=300)
trans_x_slider.pack()

trans_y_slider = Scale(root, label="Traslación Y", from_=-1, to=1, orient="horizontal", resolution=0.001, length=300)
trans_y_slider.pack()

trans_z_slider = Scale(root, label="Traslación Z", from_=-1, to=1, orient="horizontal", resolution=0.001, length=300)
trans_z_slider.pack()

# Botones para aumentar y disminuir los valores de los sliders
aumentar_rot_x_button = Button(root, text="Aumentar Rot X", command=lambda: aumentar_slider(rot_x_slider))
aumentar_rot_x_button.pack()

disminuir_rot_x_button = Button(root, text="Disminuir Rot X", command=lambda: disminuir_slider(rot_x_slider))
disminuir_rot_x_button.pack()

aumentar_rot_y_button = Button(root, text="Aumentar Rot Y", command=lambda: aumentar_slider(rot_y_slider))
aumentar_rot_y_button.pack()

disminuir_rot_y_button = Button(root, text="Disminuir Rot Y", command=lambda: disminuir_slider(rot_y_slider))
disminuir_rot_y_button.pack()

aumentar_rot_z_button = Button(root, text="Aumentar Rot Z", command=lambda: aumentar_slider(rot_z_slider))
aumentar_rot_z_button.pack()

disminuir_rot_z_button = Button(root, text="Disminuir Rot Z", command=lambda: disminuir_slider(rot_z_slider))
disminuir_rot_z_button.pack()

aumentar_trans_x_button = Button(root, text="Aumentar Trans X", command=lambda: aumentar_slider(trans_x_slider))
aumentar_trans_x_button.pack()

disminuir_trans_x_button = Button(root, text="Disminuir Trans X", command=lambda: disminuir_slider(trans_x_slider))
disminuir_trans_x_button.pack()

aumentar_trans_y_button = Button(root, text="Aumentar Trans Y", command=lambda: aumentar_slider(trans_y_slider))
aumentar_trans_y_button.pack()

disminuir_trans_y_button = Button(root, text="Disminuir Trans Y", command=lambda: disminuir_slider(trans_y_slider))
disminuir_trans_y_button.pack()

aumentar_trans_z_button = Button(root, text="Aumentar Trans Z", command=lambda: aumentar_slider(trans_z_slider))
aumentar_trans_z_button.pack()

disminuir_trans_z_button = Button(root, text="Disminuir Trans Z", command=lambda: disminuir_slider(trans_z_slider))
disminuir_trans_z_button.pack()

# Asociar la función de actualización a los eventos de cambio en los sliders
rot_x_slider.bind("<Motion>", actualizar_calibracion)
rot_y_slider.bind("<Motion>", actualizar_calibracion)
rot_z_slider.bind("<Motion>", actualizar_calibracion)
trans_x_slider.bind("<Motion>", actualizar_calibracion)
trans_y_slider.bind("<Motion>", actualizar_calibracion)
trans_z_slider.bind("<Motion>", actualizar_calibracion)
aumentar_rot_x_button.bind("<Button-1>", actualizar_calibracion)
aumentar_rot_y_button.bind("<Button-1>", actualizar_calibracion)
aumentar_rot_z_button.bind("<Button-1>", actualizar_calibracion)
disminuir_rot_x_button.bind("<Button-1>", actualizar_calibracion)
disminuir_rot_y_button.bind("<Button-1>", actualizar_calibracion)
disminuir_rot_z_button.bind("<Button-1>", actualizar_calibracion)
aumentar_trans_x_button.bind("<Button-1>", actualizar_calibracion)
aumentar_trans_y_button.bind("<Button-1>", actualizar_calibracion)
aumentar_trans_z_button.bind("<Button-1>", actualizar_calibracion)
disminuir_trans_x_button.bind("<Button-1>", actualizar_calibracion)
disminuir_trans_y_button.bind("<Button-1>", actualizar_calibracion)
disminuir_trans_z_button.bind("<Button-1>", actualizar_calibracion)
# Iniciar la ventana principal
root.mainloop()



