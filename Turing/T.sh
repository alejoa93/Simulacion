#! local/bin/bash


echo "Binvenido a la simulación de los patrones de Turing."
read -p "¿desea cambiar los parámetros de la simulación? [Y/N]"
if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "Por favor ingrese los siguientes valores para continuar."
        echo "a (del orden de 2.8e-4)"
        read a
        echo "b (del orden de 5e-3)"
        read b
        echo "tau (del orden de 0.1)"
        read tau
        echo "k (del orden de -0.005)"
        read k
    elif [[ $REPLY =~ ^[Nn]$ ]]
    then
        a=2.8e-4
        b=5e-3
        tau=0.1
        k=-0.005
    else
        echo "WROOOOONG"
        exit
fi
echo "Muy bien, usaremos: ["$a","$b","$tau","$k"]"
echo "Finalmente, la simulación está programada para 9 s" 
read -p "¿Desea cambiar el tiempo? [Y/N]"
if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "¿Por cuánto tiempo desea simular?"
        read tmax
    else
        tmax=9
fi
echo "Estamos listos para empezar, una vez finalizada la"
echo "simulación, encontrará en la carpeta raíz la gráfica"
echo "del estado final del patrón de turing, así como un"
echo "gif de la evolución temporal"



echo "">>inputs.txt
echo $a","$b","$tau","$k","$tmax>inputs.txt

python Turing.py 

if test -f "Turing.gif"
    then 
    rm Turing.gif
fi
convert T_* -loop 0 -delay 20 Turing.gif

rm T_*
rm inputs.txt


echo "La simulación ha concluido con éxito"
echo "Ha sido un placer acompañarlos hoy. Hasta la próxima."

echo "El código utilizado fue adaptado del obtenido en el enlace"
echo "https://ipython-books.github.io/124-simulating-a-partial-differential-equation-reaction-diffusion-systems-and-turing-patterns/"