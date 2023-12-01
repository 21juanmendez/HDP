from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Registros
from django.utils.timezone import datetime
from django.utils import timezone
from django.db.models import Q, Sum, Max
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
TEMPLATE_DIRS=(
    'os.path.join(BASE_DIR, "templates")'
)
@login_required
def index2(request):
    return render(request,"index2.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index2')  # Reemplaza 'inicio' con la URL a la página de inicio de tu aplicación
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas.'})
    else:
        return render(request, 'login.html')
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Reemplaza 'login' con la URL a la página de inicio de sesión de tu aplicación
@login_required
def listar(request):   
    if request.method=='POST':
        var="buscar"
        palabra=request.POST.get('keyword')
        lista=Registros.objects.all()

        if palabra is not None:
            resultado_busqueda=lista.filter(
                Q(id__icontains=palabra) |
                Q(discapacidad__icontains=palabra) |
                Q(universidad__icontains=palabra) |
                Q(sexo__icontains=palabra) |
                Q(cantidad__icontains=palabra) |
                Q(f_registro__icontains=palabra)
            )
            datos = {'registros': resultado_busqueda, 'var': var}
            return render(request, "crud_registros/listar.html", datos)
        else:
            datos={ 'registros' : lista }
            return render(request,"crud_registros/listar.html", datos) 
    else:
        registros=Registros.objects.order_by('id')[:10]
        datos={ 'registros' : registros }
        return render(request,"crud_registros/listar.html", datos)  
@login_required
def agregar(request):    
    if request.method=='POST':
        if request.POST.get('discapacidad') and request.POST.get('universidad') and request.POST.get('sexo') and request.POST.get('cantidad'):
            regis=Registros()
            regis.discapacidad=request.POST.get('discapacidad')
            regis.universidad=request.POST.get('universidad')
            regis.sexo=request.POST.get('sexo')
            regis.cantidad=request.POST.get('cantidad')
            regis.save()
            return redirect('listar')
    else:
        return render(request,"crud_registros/agregar.html")                 
@login_required
def actualizar(request, idRegistro):   
    try:
        if request.method=='POST':
            if request.POST.get('id') and request.POST.get('discapacidad') and request.POST.get('universidad') and request.POST.get('sexo') and request.POST.get('cantidad'):
                user_id_old=request.POST.get('id')
                user_old=Registros()
                user_old=Registros.objects.get(id=user_id_old)

                regis=Registros()
                regis.id=request.POST.get('id')
                regis.discapacidad=request.POST.get('discapacidad')
                regis.universidad=request.POST.get('universidad')
                regis.sexo=request.POST.get('sexo')
                regis.cantidad=request.POST.get('cantidad')
                regis.f_registro=timezone.now()
                regis.save()
                return redirect('listar')
        else:
            registros=Registros.objects.all()
            registro=Registros.objects.get(id=idRegistro)
            datos={ 'registros' : registros, 'registro':  registro}             
            return render(request,"crud_registros/actualizar.html", datos)  
        
    except Registros.DoesNotExist:
        registros=Registros.objects.all()
        registro=None
        datos={ 'registros' : registros, 'registro' :  registro}             
        return render(request, "crud_registros/actualizar.html", datos)
    
def visualizar(request):
    universidades = ["Universidad de El Salvador","Universidad Don Bosco","Universidad Cristiana Asambleas de Dios","Universidad Isaac Newton","Universidad Autonoma de Santa Ana","Universidad Catolica de Occidente","Universidad Dr.Andres Bello","Universidad Francisco Gavidia","Universidad Tecnologica","Universidad Pedagogica de El Salvador","Universidad de Oriente","Universidad Capital Gerardo Barrios"]
    discapacidades=["Ceguera","Sordera","Amputaciones","Deambulacion","Silla de ruedas"]
    ultimaActualizacion=Registros.objects.all().aggregate(fecha_maxima=Max('f_registro'))['fecha_maxima']
    cantMasculino=Registros.objects.filter(sexo__contains='Masculino').aggregate(cantM=Sum('cantidad'))['cantM']
    cantFemenino=Registros.objects.filter(sexo__contains='Femenino').aggregate(cantF=Sum('cantidad'))['cantF']
    uni=""
    cantidades=""
    disc=""
    porcentajes=[]
    f=""
    m=""
    cantidadf=[]
    cantidadm=[]
    mastergenero=[]
    masculinoo=[]
    femeninoo=[]
    total=Registros.objects.aggregate(total=Sum('cantidad'))['total']

    for u in universidades:
        r=Registros.objects.filter(universidad__contains=u)
        for d in discapacidades:
            fem=r.filter(discapacidad__contains=d, sexo__contains='Femenino').aggregate(f=Sum('cantidad'))['f']
            mas=r.filter(discapacidad__contains=d, sexo='Masculino').aggregate(m=Sum('cantidad'))['m']
            if fem is None:
                fem = 0
            if mas is None:
                mas = 0  
            masculinoo.append(mas)
            femeninoo.append(fem)
            f=f+str(fem)+","
            m=m+str(mas)+","
        cantidadf.append(f)
        cantidadm.append(m)
        mastergenero.append(zip(discapacidades,masculinoo,femeninoo))
        masculinoo=[]
        femeninoo=[]
        f=""
        m=""
            
    for elemento in universidades:
            uni=uni+"'"+elemento+"',"
            reg=Registros.objects.filter(universidad__contains=elemento)
            suma=reg.aggregate(total=Sum('cantidad'))['total']
            if suma is None:
                suma = 0
            cantidades=cantidades+str(suma)+","

    for discap in discapacidades:
        disc=disc+"'"+discap+"',"
        reg1 = Registros.objects.filter(discapacidad__contains=discap)
        sumaDiscap = reg1.aggregate(total1=Sum('cantidad'))['total1']
        if sumaDiscap is None:
            sumaDiscap = 0
        p = (sumaDiscap / total) * 100
        porcentajes.append(round(p))
        
    matriz=zip(discapacidades,porcentajes)
    infotabla=list(zip(universidades,mastergenero))
    contexto={'tabla': infotabla, 'discp': discapacidades, 'universidades': uni, 'listaUniversidad': universidades, 'discapacidades':disc, 'cantidad': cantidades,"matriz": matriz, "total": total, "fecha": ultimaActualizacion, "masculino": cantMasculino, "femenino":cantFemenino, "listaF": cantidadf, "listaM": cantidadm}
    return render(request, "index.html", contexto)

#copia y pega todo el metodo XD
def visualizar1(request):
    universidades = ["Universidad de El Salvador","Universidad Don Bosco","Universidad Cristiana Asambleas de Dios","Universidad Isaac Newton","Universidad Autonoma de Santa Ana","Universidad Catolica de Occidente","Universidad Dr.Andres Bello","Universidad Francisco Gavidia","Universidad Tecnologica","Universidad Pedagogica de El Salvador","Universidad de Oriente","Universidad Capital Gerardo Barrios"]
    discapacidades=["Ceguera","Sordera","Amputaciones","Deambulacion","Silla de ruedas"]
    ultimaActualizacion=Registros.objects.all().aggregate(fecha_maxima=Max('f_registro'))['fecha_maxima']
    cantMasculino=Registros.objects.filter(sexo__contains='Masculino').aggregate(cantM=Sum('cantidad'))['cantM']
    cantFemenino=Registros.objects.filter(sexo__contains='Femenino').aggregate(cantF=Sum('cantidad'))['cantF']
    uni=""
    cantidades=""
    disc=""
    porcentajes=[]
    f=""
    m=""
    cantidadf=[]
    cantidadm=[]
    mastergenero=[]
    masculinoo=[]
    femeninoo=[]
    total=Registros.objects.aggregate(total=Sum('cantidad'))['total']

    for u in universidades:
        r=Registros.objects.filter(universidad__contains=u)
        for d in discapacidades:
            fem=r.filter(discapacidad__contains=d, sexo__contains='Femenino').aggregate(f=Sum('cantidad'))['f']
            mas=r.filter(discapacidad__contains=d, sexo='Masculino').aggregate(m=Sum('cantidad'))['m']
            if fem is None:
                fem = 0
            if mas is None:
                mas = 0  
            masculinoo.append(mas)
            femeninoo.append(fem)
            f=f+str(fem)+","
            m=m+str(mas)+","
        cantidadf.append(f)
        cantidadm.append(m)
        mastergenero.append(zip(discapacidades,masculinoo,femeninoo))
        masculinoo=[]
        femeninoo=[]
        f=""
        m=""
            
    for elemento in universidades:
            uni=uni+"'"+elemento+"',"
            reg=Registros.objects.filter(universidad__contains=elemento)
            suma=reg.aggregate(total=Sum('cantidad'))['total']
            if suma is None:
                suma = 0
            cantidades=cantidades+str(suma)+","

    for discap in discapacidades:
        disc=disc+"'"+discap+"',"
        reg1 = Registros.objects.filter(discapacidad__contains=discap)
        sumaDiscap = reg1.aggregate(total1=Sum('cantidad'))['total1']
        if sumaDiscap is None:
            sumaDiscap = 0
        p = (sumaDiscap / total) * 100
        porcentajes.append(round(p))
        
    matriz=zip(discapacidades,porcentajes)
    infotabla=list(zip(universidades,mastergenero))
    contexto={'tabla': infotabla, 'discp': discapacidades, 'universidades': uni, 'listaUniversidad': universidades, 'discapacidades':disc, 'cantidad': cantidades,"matriz": matriz, "total": total, "fecha": ultimaActualizacion, "masculino": cantMasculino, "femenino":cantFemenino, "listaF": cantidadf, "listaM": cantidadm}
    return render(request, "index2.html", contexto)


@login_required    
def eliminar(request, idRegistro):  
    try:
        if request.method=='POST':
            if request.POST.get('id'):
                id_a_borrar=request.POST.get('id')
                tupla=Registros.objects.get(id=id_a_borrar)
                tupla.delete()
                return redirect('listar')
        else:
            registros=Registros.objects.all()
            registro=Registros.objects.get(id=idRegistro)
            datos={ 'registros' : registros, 'registro':  registro}             
            return render(request,"crud_registros/eliminar.html", datos)   
        
    except Registros.DoesNotExist:
        registros=Registros.objects.all()
        registro=None
        datos={ 'registros' : registros, 'registro':  registro}                      
        return render(request,"crud_registros/eliminar.html", datos)  