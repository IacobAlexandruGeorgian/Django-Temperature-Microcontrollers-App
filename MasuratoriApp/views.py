from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger
import csv
from .models import Tblmasuratori
from .forms import MasuratoriSearchForm, MasuratoriGraficSearchForm
from datetime import datetime, date

# Create your views here.

def is_valid_queryparameter(parameter):
    return parameter != '' and parameter is not None

def home(request):

    masuratori = Tblmasuratori.objects.all() # Colectez toate datele din baza de date
    titlu = 'Tabel: masuratori' # titlu
    form = MasuratoriSearchForm(request.POST or None)

    date_start = request.GET.get('date_start','')
    date_end = request.GET.get('date_end','')
    date_start = str(date_start)
    date_end = str(date_end)
    if is_valid_queryparameter(date_start):
        masuratori = masuratori.filter(data__gte=date_start)
    if is_valid_queryparameter(date_end):
        masuratori = masuratori.filter(data__lt=date_end)

    if request.method == 'POST':
        masuratori_extract = Tblmasuratori.objects.filter(data__range=[form['Start_Date'].value(), form['End_Date'].value()])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Tabel_Masuratori.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID','Umiditate','Temperatura [C]','Presiune [Kpa]','Altitudine [m]','data'])
        for instance in masuratori_extract:
            writer.writerow([instance.id, instance.umiditate, instance.temperatura, instance.presiune, instance.altitudine, instance.data])
        return response

    page_nr = request.GET.get('page',1)
    paginator = Paginator(masuratori, per_page=15)
    try:
        paginator = paginator.page(page_nr)
    except PageNotAnInteger:
        paginator = paginator.page(15)
    except PageNotAnInteger:
        paginator = paginator.page(paginator.num_pages)

    context = {
        "tabel": masuratori,
        "header": titlu,
        "form": form,
        "masPag": paginator,
        "date_start":date_start,
        "date_end":date_end,
    }
    return render(request, "home.html", context)

# def grafic(request):
#     masuratori = Tblmasuratori.objects.all()
#     masuratori_prezente = Tblmasuratori.objects.filter(data__icontains = date.today())
#     form = MasuratoriGraficSearchForm(request.POST or None)
#     header = 'Grafic: masuratori'
#
#     if request.method == 'POST':
#         masuratori_prezente = Tblmasuratori.objects.filter(data__icontains=form['The_Date'].value())
#
#         context = {
#             "form": form,
#             "header": header,
#             "masuratori_prezente": masuratori_prezente,
#         }
#
#     context = {
#         "data": masuratori,
#         "header": header,
#         "form": form,
#         "masuratori_prezente": masuratori_prezente
#     }
#     return render(request, "grafic.html", context)

def grafic(request):
    masuratori = Tblmasuratori.objects.all()
    masuratori_prezente = Tblmasuratori.objects.filter(data__icontains = date.today())

    masuratori_filtrate_categorie = Tblmasuratori.objects.values_list('temperatura')
    masuratori_filtrate_timp = Tblmasuratori.objects.values_list('timp')
    masuratori_filtrate_data = Tblmasuratori.objects.values_list('data', flat=True)
    masuratori_filtrate_categorie = masuratori_filtrate_categorie.filter(data__icontains=date.today())
    masuratori_filtrate_timp = masuratori_filtrate_timp.filter(data__icontains=date.today())
    masuratori_filtrate_data = masuratori_filtrate_data.filter(data__icontains=date.today())

    header = 'Grafic: masuratori'

    mas_cat = []
    timp_fil = []
    masuratoare_categorie = []
    timp_filtrat = []
    data_filtrat = []
    contor = []
    contorizare = 0
    contor.append(contorizare)

    Date = request.GET.get('the_date','')
    if is_valid_queryparameter(Date):
        masuratori_prezente = Tblmasuratori.objects.filter(data__icontains=Date)

    StartDate = request.GET.get('start_date','')
    EndDate = request.GET.get('end_date','')
    Category = request.GET.get('category','')
    Category = str(Category)

    if is_valid_queryparameter(Category):
        masuratori_filtrate_categorie = Tblmasuratori.objects.values_list(Category, flat=True)
        masuratori_filtrate_timp = Tblmasuratori.objects.values_list('timp', flat=True)
        masuratori_filtrate_data = Tblmasuratori.objects.values_list('data', flat=True)
    if is_valid_queryparameter(StartDate):
        masuratori_filtrate_categorie = masuratori_filtrate_categorie.filter(data__gte=StartDate)
        masuratori_filtrate_timp = masuratori_filtrate_timp.filter(data__gte=StartDate)
        masuratori_filtrate_data = masuratori_filtrate_data.filter(data__gte=StartDate)
    if is_valid_queryparameter(EndDate):
        masuratori_filtrate_categorie = masuratori_filtrate_categorie.filter(data__lt=EndDate)
        masuratori_filtrate_timp = masuratori_filtrate_timp.filter(data__lt=EndDate)
        masuratori_filtrate_data = masuratori_filtrate_data.filter(data__lt=EndDate)
        data_filtrat.append(masuratori_filtrate_data[0])

    for i in range(len(masuratori_filtrate_timp)):
        if (i > 0) and (masuratori_filtrate_timp[i] < masuratori_filtrate_timp[i-1]):
            masuratoare_categorie.append(mas_cat)
            timp_filtrat.append(timp_fil)
            mas_cat = []
            timp_fil = []
            data_filtrat.append(masuratori_filtrate_data[i+1])
            contorizare = contorizare + 1
            contor.append(contorizare)
        mas_cat.append(masuratori_filtrate_categorie[i])
        timp_fil.append(masuratori_filtrate_timp[i])

    masuratoare_categorie.append(mas_cat)
    timp_filtrat.append(timp_fil)
    print("masuratoare_categorie: {}".format(masuratoare_categorie))
    print("timp_filtrat: {}".format(timp_filtrat))
    print("Data: {}".format(data_filtrat))
    print("Contor: {}".format(contor))

    context = {
        "data": masuratori,
        "header": header,
        "masuratori_prezente": masuratori_prezente,
        "masuratoare_categorie": masuratoare_categorie,
        "timp_filtrat": timp_filtrat,
        "data_filtrat": data_filtrat,
        "contor": contor,
        "Category": Category,
    }
    return render(request, "grafic.html", context)
