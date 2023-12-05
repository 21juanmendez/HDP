# HDP115
 Proyecto hdp115-2023

ESTO ES PARA EL QUE ESTA EN DRIVE

 ABRIR EN VISUAL ESTUDIO: LA CARPETA "WEB ADMIN" QUE ESTA 
 ADENTRO DE LA CARPETA "HDP" Y DE AHI CORRRER: "python manage.py runserver"

 NO CORRER LA CARPETA HDP SINO QUE LA DE "WEB ADMIN"
_____________________________________________________________________________________________________
ESTO PARA EL QUE ESTA EN GITHUB

Debido a que la url de la bd es en linea tiene una duracion de 90 dias, asi que es posible
que cuando quieras usarlo ya no sirva, tendrias que crear otra bd en render y usar el comando
para migrar a la nueva bd, aqui un ejemplo del actual: 

$env:DATABASE_URL = "postgres://agora_pv07_user:QxiiSg5cH1xkrRaYd9CE4w6Bl7YXaSb7@dpg-clkqgv6aov6s738jldqg-a.oregon-postgres.render.com/agora_pv07"

Como te digo cambiaria el link x la nueva que vayas a crear. Por ultimo, este comando lo tenes que poner 
cada vez que creas una terminal nueva, por ejemplo si tenes una terminal y pones el comando te va a funcionar, pero si cerras esa terminal, abris una nueva y queres correrlo de nuevo te dara error. Tenes que ponerlo de nuevo en la nueva terminal que abristes  para que te funcione.