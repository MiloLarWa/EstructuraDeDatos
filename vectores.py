def mostrar_vector(datos):
    print(*datos, sep='\n')

def media(datos):
    return sum(datos) / len(datos)

if __name__ == "__main__":
    for datos in ([2, 4, 6, 8, 10], [1, 3, 5, 7, 9]):
        mostrar_vector(datos)
        print(f"Media = {media(datos)}")