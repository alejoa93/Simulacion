#! local/bin/bash

echo "Binvenido a la simulación del algoritmo Doob-Gillespie."
echo "Por favor ingrese los valores para: Número de células"
echo "Sugerimos utilizar valores entre 100 y 1000"
read numcel
while ! [[ "$numcel" =~ ^[0-99999]+$ ]]
    do
    echo "Solo puede haber células completas"
    read numcel
    done
echo "La simulación se realizará con "$numcel" células;"
echo "El programa está diseñado para un gen constitutivo de"
echo "E. coli sin represión ni activación."
read -p "¿desea cambiar los parámetros de la simulación? [Y/N]"
if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "Necesitamos cuatro valores, ingréselos por favor:"
        echo "Tasa de degeneración del RNAm (γr), incial es 0.25"
        read yr
        echo "Tasa de producción del RNAm (kr), incial es 1"
        read kr
        echo "Tasa de degeneración de Proteínas (γp), incial es 0.033"
        read yp
        echo "Tasa de producción de Proteínas (kp), incial es 50"
        read kp
    else
        yr=0.25
        kr=1
        yp=0.033
        kp=50
fi
echo "Muy bien, usaremos: ["$yr","$kr","$yp","$kp"]"
echo "Finalmente, la simulación está programada para 100" 
echo "unidades arbitrarias de tiempo (UA)"
read -p "¿Desea cambiar el tiempo? [Y/N]"
if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "¿Por cuánto tiempo desea simular?"
        read tmax
    else
        tmax=100
fi
echo "Estamos listos para empezar, una vez finalizada la"
echo "simulación, encontrará en la carpeta raíz las gráficas"
echo "correspondientes al comportamiento de la expresión génica."
echo "">>inputs.txt
echo $numcel","$yr","$kr","$yp","$kp","$tmax>inputs.txt

python Simulacion.py

rm inputs.txt

echo "La simulación ha concluido con éxito"
echo "Ha sido un placer acompañarlos hoy. Hasta la próxima."
