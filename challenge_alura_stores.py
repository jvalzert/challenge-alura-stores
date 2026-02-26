# Alura Latam G9: Data Science
# Jorge V. Zertuche Rodriguez
# CURSO: Practicando Python para Data Science: Challenge Alura Store
# ==========================================================

'''
ESCENARIO
El señor Juan requiere un analista de datos para tomar una decisión sobre cuál
de sus tiendas debería vender para invertir en un nuevo negocio. Actualmente el
señor Juan es propietario de cuatro tiendas.
Para este análisis se deben considerar los siguientes parámetros:
* Facturación total de cada tienda.
* Categorías más populares.
* Promedio de calificación de los clientes.
* Productos más/menos vendidos.
* Costo promedio de envío.
'''

import pandas as pd
pd.options.display.float_format = '{:.2f}'.format
import matplotlib.pyplot as plt
import numpy as np


# Extracción de datos
nombres_tiendas = ["Tienda 1","Tienda 2","Tienda 3","Tienda 4"]
colores_tiendas = ["#B4C7DC","#FFFFA6","#BF819E","#EC9BA4"]
tiendas = [pd.read_csv(f'data/tienda_{n}.csv') for n in [1,2,3,4]]
print(f"\n0. DATOS INICIALES POR CADA TIENDA\n")
for n in range(len(tiendas)):
	print(f"{nombres_tiendas[n]}:\n{tiendas[n]}")
	print()


# Facturación total por tienda
facturacion = [tienda['Precio'].sum() for tienda in tiendas]
facturacion_total = sum(facturacion)
print(f"\n1. FACTURACIÓN TOTAL POR CADA TIENDA\n")
for n,total in enumerate(facturacion):
	print(f"{nombres_tiendas[n]}:\t$ {total:,.2f}  ({total/facturacion_total*100:.1f}% del total)")
print()
labels_facturacion = [f"{nombre}\n$ {int(total):,}" for nombre,total in zip(nombres_tiendas,facturacion)]
plt.figure(figsize=(14,9))
plt.pie(facturacion,
		labels=labels_facturacion,
		textprops={"fontsize":18,"ha":"center"},
		labeldistance=1.3,
		colors=colores_tiendas,
		startangle=0,
		autopct="%1.1f%%",)
plt.title("Facturación total por tienda",fontsize=16)
plt.tight_layout()
plt.savefig('images/1_facturacion_por_tienda.png',dpi=300)
plt.show()


# Categorías más populares
todas_categorias = sorted(set().union(*[tienda['Categoría del Producto'].unique() for tienda in tiendas]))
cats_venta = [tienda['Categoría del Producto'].value_counts().reindex(todas_categorias,fill_value=0) for tienda in tiendas]
categorias = cats_venta[0].index
y = np.arange(len(categorias))
bar_height = 0.2
plt.figure(figsize=(14,9))
print(f"\n2. CATEGORÍAS DE MAYOR VENTA POR CADA TIENDA\n")
for n,tienda in enumerate(tiendas):
	print(f"{nombres_tiendas[n]}:\n{tienda['Categoría del Producto'].value_counts()}")
	print()
	plt.barh(y+n*bar_height,cats_venta[n].values,
	         height=bar_height,
	         color=colores_tiendas[n],
	         label=nombres_tiendas[n])
plt.yticks(y+bar_height*1.5,categorias,fontsize=12)
plt.xlabel("Cantidad de ventas",fontsize=12)
plt.xlim(0,500)
plt.suptitle("Ventas por categoría",fontsize=16)
plt.legend(fontsize=12)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('images/2_categorias_de_venta.png',dpi=300)
plt.show()


# Calificación de clientes
califs_posibles = [1,2,3,4,5]
califs_venta = [tienda['Calificación'].value_counts().reindex(califs_posibles,fill_value=0)for tienda in tiendas]
prom_califs = [tienda['Calificación'].mean() for tienda in tiendas]
x = np.arange(len(califs_posibles))
bar_width = 0.2
plt.figure(figsize=(14,9))
print(f"\n3. (a) CALIFICACIÓN DE CLIENTES POR CADA TIENDA\n")
for n,tienda in enumerate(tiendas):
	print(f"{nombres_tiendas[n]}:\n{califs_venta[n]}")
	print()
	plt.bar(x+n*bar_width,califs_venta[n].values,
	        width=bar_width,
	        color=colores_tiendas[n],
	        label=nombres_tiendas[n])
plt.xticks(x+bar_width*1.5,califs_posibles)
plt.xlabel("Calificación",fontsize=12)
plt.ylabel("Cantidad de reseñas",fontsize=12)
plt.ylim(0,1400)
plt.suptitle("Calificación de los clientes",fontsize=16)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig('images/3_calificaciones_por_tienda.png',dpi=300)
plt.show()
print(f"\n3. (b) PROMEDIO DE CALIFICACIÓN DE CLIENTES POR CADA TIENDA\n")
for n,calif in enumerate(prom_califs):
	print(f"{nombres_tiendas[n]}:\t{calif:.3f}")
print()


# Productos más vendidos
todos_productos = sorted(set().union(*[tienda['Producto'].unique() for tienda in tiendas]))
prods_vendidos = [tienda['Producto'].value_counts().reindex(todos_productos,fill_value=0) for tienda in tiendas]
y = np.arange(len(todos_productos))
print(f"\n4. VENTA DE PRODUCTOS POR CADA TIENDA\n")
for n,tienda in enumerate(tiendas):
	print(f"{nombres_tiendas[n]}:\n{prods_vendidos[n]}")
	print()
	plt.figure(figsize=(14,9))
	plt.barh(y,prods_vendidos[n].values,
	         color=colores_tiendas[n])
	plt.yticks(y,todos_productos,fontsize=10)
	plt.xlabel("Cantidad de ventas",fontsize=12)
	plt.xlim(0,70)
	plt.ylim(-0.5,len(todos_productos)-0.5)
	plt.gca().invert_yaxis()
	plt.suptitle(f"Ventas por producto - {nombres_tiendas[n]}",fontsize=16)
	plt.tight_layout()
	plt.savefig(f'images/4_ventas_productos_tienda_{n+1}.png',dpi=300)
	plt.show()


# Costo de envío
prom_envio = [tienda['Costo de envío'].mean() for tienda in tiendas]
x = np.arange(len(nombres_tiendas))
print(f"\n5. PROMEDIO DE COSTOS DE ENVÍO POR CADA TIENDA\n")
for n,envio in enumerate(prom_envio):
	print(f"{nombres_tiendas[n]}:\t$ {envio:,.2f}")
print()
plt.figure(figsize=(14,9))
plt.bar(x,prom_envio,
        color=colores_tiendas,
        width=0.6)
for n,valor in enumerate(prom_envio):
    plt.text(x[n],valor+0.5,f"$ {valor:,.2f}",ha='center',va='bottom',fontsize=12)
plt.xticks(x,nombres_tiendas,fontsize=12)
plt.yticks([])
plt.suptitle("Promedio de costos de envío por tienda",fontsize=16)
plt.tight_layout()
plt.savefig('images/5_promedio_costos_envio.png',dpi=300)
plt.show()
