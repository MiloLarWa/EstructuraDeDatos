import java.util.Scanner;

public class Ventas {
    private static final int MESES = 12;
    private static final int DEPARTAMENTOS = 3;

    private Double[][] ventas = new Double[MESES][DEPARTAMENTOS];

    private String[] nombresMeses = {
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    };

    private String[] nombresDeptos = {
        "Farmacia", "Salchichonería", "Panadería"
    };

    public void insertarVenta(int mes, int departamento, double valor) {
        if (mes < 0 || mes >= MESES || departamento < 0 || departamento >= DEPARTAMENTOS) {
            System.out.println("Error: Mes (0-11) o departamento (0-2) fuera de rango.");
            return;
        }

        if (valor < 0) {
            System.out.println("Error: El valor de la venta no puede ser negativo.");
            return;
        }

        ventas[mes][departamento] = valor;

        System.out.println("--> Venta registrada con éxito en "
                + nombresMeses[mes] + " (" + nombresDeptos[departamento] + "): $" + valor);
    }

    public void buscarVentaPorValor(double valor) {
        boolean encontrado = false;
        double tolerancia = 0.001;

        for (int i = 0; i < MESES; i++) {
            for (int j = 0; j < DEPARTAMENTOS; j++) {
                if (ventas[i][j] != null && Math.abs(ventas[i][j] - valor) < tolerancia) {
                    System.out.println("--> Encontrado: $" + ventas[i][j]
                            + " en el mes de " + nombresMeses[i]
                            + ", departamento de " + nombresDeptos[j]);
                    encontrado = true;
                }
            }
        }

        if (!encontrado) {
            System.out.println("--> No se encontró ninguna venta cercana al valor de: $" + valor);
        }
    }

    public void buscarPorCoordenada(int mes, int departamento) {
        if (mes >= 0 && mes < MESES && departamento >= 0 && departamento < DEPARTAMENTOS) {
            Double val = ventas[mes][departamento];

            if (val != null) {
                System.out.println("--> Venta en " + nombresMeses[mes]
                        + " - " + nombresDeptos[departamento] + ": $" + val);
            } else {
                System.out.println("--> No hay registros en "
                        + nombresMeses[mes] + " para " + nombresDeptos[departamento]);
            }
        } else {
            System.out.println("Error: Índices fuera de rango.");
        }
    }

    public void eliminarVenta(int mes, int departamento) {
        if (mes >= 0 && mes < MESES && departamento >= 0 && departamento < DEPARTAMENTOS) {
            ventas[mes][departamento] = null;

            System.out.println("--> Venta eliminada para "
                    + nombresMeses[mes] + " en " + nombresDeptos[departamento]);
        } else {
            System.out.println("Error: Índices fuera de rango.");
        }
    }

    public void calcularTotales() {
        System.out.println("\n--- Reporte de Totales ---");

        for (int i = 0; i < MESES; i++) {
            double totalMes = 0;

            for (int j = 0; j < DEPARTAMENTOS; j++) {
                if (ventas[i][j] != null) {
                    totalMes += ventas[i][j];
                }
            }

            System.out.println("Total en " + nombresMeses[i] + ": $" + totalMes);
        }

        System.out.println();

        for (int j = 0; j < DEPARTAMENTOS; j++) {
            double totalDepto = 0;

            for (int i = 0; i < MESES; i++) {
                if (ventas[i][j] != null) {
                    totalDepto += ventas[i][j];
                }
            }

            System.out.println("Total en departamento "
                    + nombresDeptos[j] + ": $" + totalDepto);
        }
    }

    public void mostrarMatriz() {
        System.out.println("\n--- Tabla de Ventas ---");

        System.out.printf("%-12s | %-12s | %-18s | %-12s\n",
                "Mes", "Farmacia", "Salchichonería", "Panadería");

        for (int i = 0; i < MESES; i++) {
            String f = ventas[i][0] != null ? "$" + ventas[i][0] : "-";
            String s = ventas[i][1] != null ? "$" + ventas[i][1] : "-";
            String p = ventas[i][2] != null ? "$" + ventas[i][2] : "-";

            System.out.printf("%-12s | %-12s | %-18s | %-12s\n",
                    nombresMeses[i], f, s, p);
        }

        System.out.println("-------------------------------------------------------------");
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Ventas tienda = new Ventas();
        int opcion = 0;

        do {
            System.out.println("\n=== MENÚ GESTIÓN DE VENTAS ===");
            System.out.println("1. Insertar / Actualizar venta");
            System.out.println("2. Buscar venta por valor");
            System.out.println("3. Buscar venta por mes y departamento");
            System.out.println("4. Eliminar venta");
            System.out.println("5. Mostrar matriz completa");
            System.out.println("6. Ver totales");
            System.out.println("7. Salir");
            System.out.print("Seleccione una opción: ");

            if (scanner.hasNextInt()) {
                opcion = scanner.nextInt();

                switch (opcion) {
                    case 1:
                        System.out.print("Ingrese mes (0: Enero ... 11: Diciembre): ");
                        int m = scanner.nextInt();

                        System.out.print("Ingrese departamento (0: Farmacia, 1: Salchichonería, 2: Panadería): ");
                        int d = scanner.nextInt();

                        System.out.print("Ingrese el valor de la venta ($): ");
                        double v = scanner.nextDouble();

                        tienda.insertarVenta(m, d, v);
                        break;

                    case 2:
                        System.out.print("Ingrese el valor a buscar: ");
                        double valBuscar = scanner.nextDouble();

                        tienda.buscarVentaPorValor(valBuscar);
                        break;

                    case 3:
                        System.out.print("Ingrese mes (0-11): ");
                        int mesB = scanner.nextInt();

                        System.out.print("Ingrese departamento (0-2): ");
                        int depB = scanner.nextInt();

                        tienda.buscarPorCoordenada(mesB, depB);
                        break;

                    case 4:
                        System.out.print("Ingrese mes a eliminar (0-11): ");
                        int mesE = scanner.nextInt();

                        System.out.print("Ingrese departamento a eliminar (0-2): ");
                        int depE = scanner.nextInt();

                        tienda.eliminarVenta(mesE, depE);
                        break;

                    case 5:
                        tienda.mostrarMatriz();
                        break;

                    case 6:
                        tienda.calcularTotales();
                        break;

                    case 7:
                        System.out.println("Saliendo del programa...");
                        break;

                    default:
                        System.out.println("Opción inválida.");
                }

            } else {
                System.out.println("Por favor, ingrese un número válido.");
                scanner.next();
            }

        } while (opcion != 7);

        scanner.close();
    }
}