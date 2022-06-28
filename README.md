# Demanda de Electricidad en Chile

Scripts para procesar datos de demanda eléctrica horaria a nivel de subestaciones en Chile.

Gracias a estos scripts es posible procesar los archivos de demanda eléctrica entregados por el coordinador, tanto en los formatos anteriores a la unión SIC-SING, como los actuales con un solo sistema, de manera de construir datos de demanda horaria para cada subestación del sistema hasta la actualidad. La fecha de inicio de los datos obtenidos depende de los archivos de entrada obtenidos desde el coordinador.

Para usarlos se requiere como dependencia _numpy_ y _pandas_.

## Nota

Se supone que los archivos con los datos originales ya fueron obtenidos desde el coordinador. Si aún no los ha conseguido, puede descargarlos desde la página del coordinador, en la sección _Mercado_, o pedirlos por ley de transparencia.

## Instrucciones de uso

1. Colocar los archivos de entrada en un directorio, con el formato de nombre siguiente: `balance_AAMM.csv`, con AA el año y MM el mes, para los archivos SING, y `valorizado_AAMM.csv` para los provenientes del SIC o actuales. Por ejemplo, el directorio `entrada` podría tener los siguientes archivos:

```
balance_1001.csv
balance_1002.csv
balance_1003.csv
balance_1004.csv
balance_1005.csv
balance_1006.csv
balance_1007.csv
balance_1008.csv
balance_1009.csv
balance_1010.csv
balance_1011.csv
balance_1012.csv
balance_1101.csv
balance_1102.csv
balance_1103.csv
balance_1104.csv
balance_1105.csv
balance_1106.csv
balance_1107.csv
balance_1108.csv
balance_1109.csv
balance_1110.csv
balance_1111.csv
balance_1112.csv
balance_1201.csv
balance_1202.csv
balance_1203.csv
balance_1204.csv
balance_1205.csv
balance_1206.csv
balance_1207.csv
balance_1208.csv
balance_1209.csv
balance_1210.csv
balance_1211.csv
balance_1212.csv
balance_1301.csv
balance_1302.csv
balance_1303.csv
balance_1304.csv
balance_1305.csv
balance_1306.csv
balance_1307.csv
balance_1308.csv
balance_1309.csv
balance_1310.csv
balance_1311.csv
balance_1312.csv
balance_1401.csv
balance_1402.csv
balance_1403.csv
balance_1404.csv
balance_1405.csv
balance_1406.csv
balance_1407.csv
balance_1408.csv
balance_1409.csv
balance_1410.csv
balance_1411.csv
balance_1412.csv
balance_1501.csv
balance_1502.csv
balance_1503.csv
balance_1504.csv
balance_1505.csv
balance_1506.csv
balance_1507.csv
balance_1508.csv
balance_1509.csv
balance_1510.csv
balance_1511.csv
balance_1512.csv
balance_1601.csv
balance_1602.csv
balance_1603.csv
balance_1604.csv
balance_1605.csv
balance_1606.csv
balance_1607.csv
balance_1608.csv
balance_1609.csv
balance_1610.csv
balance_1611.csv
balance_1612.csv
balance_1701.csv
balance_1702.csv
balance_1703.csv
balance_1704.csv
balance_1705.csv
balance_1706.csv
balance_1707.csv
balance_1708.csv
balance_1709.csv
balance_1710.csv
balance_1711-1.csv
valorizado_1301.csv
valorizado_1302.csv
valorizado_1303.csv
valorizado_1304.csv
valorizado_1305.csv
valorizado_1306.csv
valorizado_1307.csv
valorizado_1308.csv
valorizado_1309.csv
valorizado_1310.csv
valorizado_1311.csv
valorizado_1312.csv
valorizado_1401.csv
valorizado_1402.csv
valorizado_1403.csv
valorizado_1404.csv
valorizado_1405.csv
valorizado_1406.csv
valorizado_1407.csv
valorizado_1408.csv
valorizado_1409.csv
valorizado_1410.csv
valorizado_1411.csv
valorizado_1412.csv
valorizado_1501.csv
valorizado_1502.csv
valorizado_1503.csv
valorizado_1504.csv
valorizado_1505.csv
valorizado_1506.csv
valorizado_1507.csv
valorizado_1508.csv
valorizado_1509.csv
valorizado_1510.csv
valorizado_1511.csv
valorizado_1512-preliminar.csv
valorizado_1601.csv
valorizado_1602.csv
valorizado_1603.csv
valorizado_1604.csv
valorizado_1605.csv
valorizado_1606.csv
valorizado_1607.csv
valorizado_1608.csv
valorizado_1609.csv
valorizado_1610.csv
valorizado_1611.csv
valorizado_1612.csv
valorizado_1701.csv
valorizado_1702.csv
valorizado_1703.csv
valorizado_1704.csv
valorizado_1705.csv
valorizado_1706.csv
valorizado_1707.csv
valorizado_1708.csv
valorizado_1709.csv
valorizado_1710.csv
valorizado_1711-1-preliminar.csv
valorizado_1711-2.csv
valorizado_1712.csv
valorizado_1801.csv
valorizado_1802.csv
valorizado_1803.csv
valorizado_1804.csv
valorizado_1805.csv
valorizado_1806.csv
valorizado_1807.csv
valorizado_1808.csv
valorizado_1809.csv
valorizado_1810.csv
valorizado_1811.csv
valorizado_1812.csv
valorizado_1901.csv
valorizado_1902.csv
valorizado_1903.csv
valorizado_1904.csv
valorizado_1905.csv
valorizado_1906.csv
valorizado_1907.csv
valorizado_1908.csv
valorizado_1909.csv
valorizado_1910.csv
valorizado_1911.csv
valorizado_1912.csv
valorizado_2001.csv
valorizado_2002.csv
valorizado_2003.csv
valorizado_2004.csv
```

2. Utilizar el script `group_substation_data.py`, indicando el directorio de entrada:

```
python group_substation_data.py --directory entrada
```

3. Se generan los siguientes 3 archivos de salida:

+ `all_data_rows.csv`: todos los valores, para todas las subestaciones, en una sola columna, en formato una subestación y una fecha por fila.
+ `all_data_columns.csv`: los valores para cada subestación están en columnas distintas, por lo que el formato es una fecha por fila.
+ `total_data.csv`: la suma de la demanda de todas las subestaciones procesadas, en formato una fecha por fila.

Cada archivo de salida contendrá además las siguientes columnas:

+ : identificador número de línea, no utilizado.
+ DMONTH_1D: mes en posición 2-dimensional de "reloj".
+ DMONTH_2D: mes en posición 2-dimensional de "reloj".
+ DDAY_1D: día del mes en posición 2-dimensional de "reloj".
+ DDAY_2D: día del mes en posición 2-dimensional de "reloj".
+ DHOUR_1D: hora del día en posición 2-dimensional de "reloj".
+ DHOUR_2D: hora del día en posición 2-dimensional de "reloj".
+ DHOUR_IN_MONTH_1D: hora en el mes en posición 2-dimensional de "reloj".
+ DHOUR_IN_MONTH_2D: hora en el mes en posición 2-dimensional de "reloj".
+ DDAY_OF_WEEK_1D: día de la semana en posición 2-dimensional de "reloj".
+ DDAY_OF_WEEK_2D: día de la semana en posición 2-dimensional de "reloj".
+ DDAY_OF_YEAR_1D: día del año en posición 2-dimensional de "reloj".
+ DDAY_OF_YEAR_2D: día del año en posición 2-dimensional de "reloj".
+ DYEAR: año.
+ DMONTH: mes.
+ DDAY: día del mes.
+ DHOUR: hora del día.
+ DHOUR_IN_MONTH: hora en el mes.
+ DDST_ACTIVE: horario de verano activo.
+ DDAY_OF_WEEK: día de la semana.
+ DDAY_OF_YEAR: día del año.
+ DNONNEGOTIABLE_HOLIDAY: es feriado irrenunciable.
+ DCIVIL_HOLIDAY: es feriado civil.
+ DRELIGIOUS_HOLIDAY: es feriado religioso.
+ DPEAK_HOUR: es horario punta (**aún no implementado**).
+ GMT: hora UTC.

## Fuentes

* [Feriados legales de Chile](https://apis.digital.gob.cl/fl/).
* [Días Feriados en Chile](https://www.feriadoschilenos.cl/).
* [Coordinador Eléctrico Nacional](https://www.coordinador.cl/).
